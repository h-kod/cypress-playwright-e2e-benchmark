import argparse
import os

import pandas as pd


def summarize_file(path: str):
    df = pd.read_csv(path)
    ok = df[df["success"] == 1].copy()
    if ok.empty:
        return {
            "file": os.path.basename(path),
            "success_count": 0,
            "total_count": len(df),
            "avg_duration_sec": None,
            "min_duration_sec": None,
            "max_duration_sec": None,
            "avg_cpu_percent": None,
            "avg_memory_mb": None,
            "peak_memory_mb": None,
        }
    return {
        "file": os.path.basename(path),
        "success_count": int(ok["success"].sum()),
        "total_count": int(len(df)),
        "avg_duration_sec": round(ok["duration_sec"].mean(), 4),
        "min_duration_sec": round(ok["duration_sec"].min(), 4),
        "max_duration_sec": round(ok["duration_sec"].max(), 4),
        "avg_cpu_percent": round(ok["avg_cpu_percent"].mean(), 4),
        "avg_memory_mb": round(ok["avg_memory_mb"].mean(), 4),
        "peak_memory_mb": round(ok["peak_memory_mb"].max(), 4),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--playwright", required=True)
    parser.add_argument("--cypress", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    p = summarize_file(args.playwright)
    c = summarize_file(args.cypress)
    result = pd.DataFrame([p, c])
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    result.to_csv(args.output, index=False, encoding="utf-8-sig")
    print(result.to_string(index=False))
    print(f"\nÖzet dosyası kaydedildi: {args.output}")


if __name__ == "__main__":
    main()
