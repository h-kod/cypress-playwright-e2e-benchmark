import argparse
import csv
import os
import statistics
import subprocess
import time
from datetime import datetime

import psutil


def safe_children(proc: psutil.Process):
    try:
        return proc.children(recursive=True)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return []


def collect_process_tree(proc: psutil.Process):
    processes = [proc]
    processes.extend(safe_children(proc))
    alive = []
    for p in processes:
        try:
            if p.is_running():
                alive.append(p)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return alive


def prime_cpu_counters(processes):
    for p in processes:
        try:
            p.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass


def process_cpu_time(p: psutil.Process) -> float:
    try:
        cpu_times = p.cpu_times()
        return float(cpu_times.user + cpu_times.system)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return 0.0


def sample_metrics(processes, sample_interval: float, previous_cpu_time: float):
    total_cpu = 0.0
    total_cpu_time = 0.0
    total_rss_mb = 0.0
    for p in processes:
        try:
            total_cpu += p.cpu_percent(interval=None)
            total_rss_mb += p.memory_info().rss / (1024 * 1024)
            total_cpu_time += process_cpu_time(p)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    cpu_time_delta = max(total_cpu_time - previous_cpu_time, 0.0)
    cpu_percent_from_times = (cpu_time_delta / sample_interval) * 100 if sample_interval > 0 else 0.0
    total_cpu = max(total_cpu, cpu_percent_from_times)
    return total_cpu, total_rss_mb, total_cpu_time


def ensure_dir(path: str):
    if path:
        os.makedirs(path, exist_ok=True)


def run_once(command: str, sample_interval: float):
    start_ts = time.perf_counter()
    start_wall = datetime.now().isoformat()
    process = subprocess.Popen(command, shell=True)
    parent = psutil.Process(process.pid)
    peak_memory_mb = 0.0
    cpu_samples = []
    system_cpu_samples = []
    memory_samples = []
    cpu_time_samples = []
    time.sleep(0.2)
    processes = collect_process_tree(parent)
    prime_cpu_counters(processes)
    try:
        psutil.cpu_percent(interval=None)
    except Exception:
        pass
    baseline_cpu_time = sum(process_cpu_time(p) for p in processes)
    previous_cpu_time = baseline_cpu_time
    while process.poll() is None:
        time.sleep(sample_interval)
        processes = collect_process_tree(parent)
        cpu_percent, memory_mb, cpu_time = sample_metrics(processes, sample_interval, previous_cpu_time)
        previous_cpu_time = cpu_time
        try:
            system_cpu_percent = psutil.cpu_percent(interval=None)
        except Exception:
            system_cpu_percent = 0.0
        cpu_samples.append(cpu_percent)
        system_cpu_samples.append(system_cpu_percent)
        memory_samples.append(memory_mb)
        cpu_time_samples.append(cpu_time)
        if memory_mb > peak_memory_mb:
            peak_memory_mb = memory_mb
    duration_sec = time.perf_counter() - start_ts
    exit_code = process.returncode
    avg_cpu = statistics.mean(cpu_samples) if cpu_samples else 0.0
    avg_system_cpu = statistics.mean(system_cpu_samples) if system_cpu_samples else 0.0
    avg_memory = statistics.mean(memory_samples) if memory_samples else 0.0
    cpu_time_sec = max((cpu_time_samples[-1] if cpu_time_samples else 0.0) - baseline_cpu_time, 0.0)
    estimated_cpu_time_sec = sum((sample / 100.0) * sample_interval for sample in cpu_samples)
    if cpu_time_sec == 0.0 and estimated_cpu_time_sec > 0.0:
        cpu_time_sec = estimated_cpu_time_sec
    return {
        "start_time": start_wall,
        "duration_sec": round(duration_sec, 4),
        "avg_cpu_percent": round(avg_cpu, 4),
        "avg_system_cpu_percent": round(avg_system_cpu, 4),
        "avg_memory_mb": round(avg_memory, 4),
        "peak_memory_mb": round(peak_memory_mb, 4),
        "cpu_time_sec": round(cpu_time_sec, 4),
        "sample_count": len(cpu_samples),
        "exit_code": exit_code,
        "success": 1 if exit_code == 0 else 0,
    }


def write_results(output_csv: str, rows: list[dict]):
    ensure_dir(os.path.dirname(output_csv))
    fieldnames = [
        "run_index",
        "tool",
        "start_time",
        "duration_sec",
        "avg_cpu_percent",
        "avg_system_cpu_percent",
        "avg_memory_mb",
        "peak_memory_mb",
        "cpu_time_sec",
        "sample_count",
        "exit_code",
        "success",
    ]
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def print_summary(tool: str, rows: list[dict]):
    success_rows = [r for r in rows if r["success"] == 1]
    if not success_rows:
        print(f"[{tool}] Başarılı çalıştırma yok.")
        return
    print()
    print(f"=== {tool.upper()} ÖZET ===")
    print(f"Başarılı tekrar sayısı : {len(success_rows)}/{len(rows)}")
    print(f"Ortalama süre          : {statistics.mean(r['duration_sec'] for r in success_rows):.4f} sn")
    print(f"Ortalama CPU           : {statistics.mean(r['avg_cpu_percent'] for r in success_rows):.4f} %")
    print(f"Sistem CPU ortalaması  : {statistics.mean(r['avg_system_cpu_percent'] for r in success_rows):.4f} %")
    print(f"Ortalama bellek        : {statistics.mean(r['avg_memory_mb'] for r in success_rows):.4f} MB")
    print(f"En yüksek bellek       : {max(r['peak_memory_mb'] for r in success_rows):.4f} MB")
    print(f"CPU süresi ortalaması  : {statistics.mean(r['cpu_time_sec'] for r in success_rows):.4f} sn")
    print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool", required=True)
    parser.add_argument("--command", required=True)
    parser.add_argument("--repeat", type=int, default=5)
    parser.add_argument("--interval", type=float, default=0.2)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = []
    for i in range(1, args.repeat + 1):
        print(f"[{args.tool}] Çalıştırma {i}/{args.repeat} başladı...")
        result = run_once(args.command, args.interval)
        row = {"run_index": i, "tool": args.tool, **result}
        rows.append(row)
        print(
            f"[{args.tool}] {i}. tekrar bitti | süre={row['duration_sec']} sn | "
            f"avg_cpu={row['avg_cpu_percent']} | system_cpu={row['avg_system_cpu_percent']} | "
            f"cpu_time={row['cpu_time_sec']} sn | peak_mem={row['peak_memory_mb']} MB | exit={row['exit_code']}"
        )
    write_results(args.output, rows)
    print_summary(args.tool, rows)
    print(f"CSV kaydedildi: {args.output}")


if __name__ == "__main__":
    main()
