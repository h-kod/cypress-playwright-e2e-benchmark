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


def sample_metrics(processes):
    total_cpu = 0.0
    total_rss_mb = 0.0

    for p in processes:
        try:
            total_cpu += p.cpu_percent(interval=None)
            mem = p.memory_info().rss / (1024 * 1024)
            total_rss_mb += mem
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return total_cpu, total_rss_mb


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
    memory_samples = []

    time.sleep(0.2)
    processes = collect_process_tree(parent)
    prime_cpu_counters(processes)

    while process.poll() is None:
        time.sleep(sample_interval)
        processes = collect_process_tree(parent)
        cpu_percent, memory_mb = sample_metrics(processes)

        cpu_samples.append(cpu_percent)
        memory_samples.append(memory_mb)

        if memory_mb > peak_memory_mb:
            peak_memory_mb = memory_mb

    end_ts = time.perf_counter()
    duration_sec = end_ts - start_ts

    exit_code = process.returncode
    success = 1 if exit_code == 0 else 0

    avg_cpu = statistics.mean(cpu_samples) if cpu_samples else 0.0
    avg_memory = statistics.mean(memory_samples) if memory_samples else 0.0

    return {
        "start_time": start_wall,
        "duration_sec": round(duration_sec, 4),
        "avg_cpu_percent": round(avg_cpu, 4),
        "avg_memory_mb": round(avg_memory, 4),
        "peak_memory_mb": round(peak_memory_mb, 4),
        "sample_count": len(cpu_samples),
        "exit_code": exit_code,
        "success": success,
    }


def write_results(output_csv: str, rows: list[dict]):
    ensure_dir(os.path.dirname(output_csv))

    fieldnames = [
        "run_index",
        "tool",
        "start_time",
        "duration_sec",
        "avg_cpu_percent",
        "avg_memory_mb",
        "peak_memory_mb",
        "sample_count",
        "exit_code",
        "success",
    ]

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def print_summary(tool: str, rows: list[dict]):
    success_rows = [r for r in rows if r["success"] == 1]

    if not success_rows:
        print(f"[{tool}] Başarılı çalıştırma yok.")
        return

    avg_duration = statistics.mean(r["duration_sec"] for r in success_rows)
    avg_cpu = statistics.mean(r["avg_cpu_percent"] for r in success_rows)
    avg_mem = statistics.mean(r["avg_memory_mb"] for r in success_rows)
    peak_mem = max(r["peak_memory_mb"] for r in success_rows)

    print()
    print(f"=== {tool.upper()} ÖZET ===")
    print(f"Başarılı tekrar sayısı : {len(success_rows)}/{len(rows)}")
    print(f"Ortalama süre          : {avg_duration:.4f} sn")
    print(f"Ortalama CPU           : {avg_cpu:.4f} %")
    print(f"Ortalama bellek        : {avg_mem:.4f} MB")
    print(f"En yüksek bellek       : {peak_mem:.4f} MB")
    print()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool", required=True, help="playwright veya cypress")
    parser.add_argument("--command", required=True, help="çalıştırılacak test komutu")
    parser.add_argument("--repeat", type=int, default=5, help="tekrar sayısı")
    parser.add_argument("--interval", type=float, default=0.5, help="örnekleme aralığı")
    parser.add_argument("--output", required=True, help="çıktı csv yolu")
    args = parser.parse_args()

    rows = []

    for i in range(1, args.repeat + 1):
        print(f"[{args.tool}] Çalıştırma {i}/{args.repeat} başladı...")
        result = run_once(args.command, args.interval)
        row = {
            "run_index": i,
            "tool": args.tool,
            **result,
        }
        rows.append(row)
        print(
            f"[{args.tool}] {i}. tekrar bitti | süre={row['duration_sec']} sn | "
            f"avg_cpu={row['avg_cpu_percent']} | peak_mem={row['peak_memory_mb']} MB | "
            f"exit={row['exit_code']}"
        )

    write_results(args.output, rows)
    print_summary(args.tool, rows)
    print(f"CSV kaydedildi: {args.output}")


if __name__ == "__main__":
    main()
