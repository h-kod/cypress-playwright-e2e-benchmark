import argparse
import math
import os
from dataclasses import dataclass
from typing import Iterable

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


TOOLS = ("playwright", "cypress")
PROFILES = ("baseline", "ui-heavy", "cpu-heavy", "ram-heavy")
DEFAULT_METRICS = (
    "duration_sec",
    "avg_cpu_percent",
    "avg_system_cpu_percent",
    "avg_memory_mb",
    "peak_memory_mb",
    "cpu_time_sec",
)


@dataclass(frozen=True)
class Dataset:
    tool: str
    profile: str
    path: str
    frame: pd.DataFrame


def ensure_dir(path: str):
    if path:
        os.makedirs(path, exist_ok=True)


def sanitize_filename(value: str) -> str:
    return value.replace("/", "_").replace(" ", "_")


def resolve_input_path(results_root: str, tool: str, profile: str, repeat: int) -> str | None:
    candidates = []
    if profile == "baseline":
        candidates.append(os.path.join(results_root, tool, f"{profile}_benchmark_{repeat}.csv"))
        candidates.append(os.path.join(results_root, tool, f"{tool}_benchmark_{repeat}.csv"))
    else:
        candidates.append(os.path.join(results_root, tool, f"{profile}_benchmark_{repeat}.csv"))

    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return None


def load_dataset(results_root: str, tool: str, profile: str, repeat: int) -> Dataset | None:
    path = resolve_input_path(results_root, tool, profile, repeat)
    if path is None:
        return None

    frame = pd.read_csv(path)
    if "profile" not in frame.columns:
        frame = frame.copy()
        frame["profile"] = profile
    else:
        frame = frame.copy()
        frame["profile"] = frame["profile"].fillna(profile)

    if "tool" not in frame.columns:
        frame["tool"] = tool

    return Dataset(tool=tool, profile=profile, path=path, frame=frame)


def successful_rows(frame: pd.DataFrame) -> pd.DataFrame:
    if "success" not in frame.columns:
        return frame.copy()
    return frame[frame["success"] == 1].copy()


def metric_stats(series: pd.Series) -> dict[str, float | None]:
    if series.empty:
        return {
            "mean": None,
            "median": None,
            "std": None,
            "min": None,
            "max": None,
        }

    return {
        "mean": round(float(series.mean()), 4),
        "median": round(float(series.median()), 4),
        "std": round(float(series.std(ddof=1)), 4) if len(series) > 1 else 0.0,
        "min": round(float(series.min()), 4),
        "max": round(float(series.max()), 4),
    }


def rank_values(values: list[float]) -> list[float]:
    sorted_pairs = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(sorted_pairs):
        j = i
        while j < len(sorted_pairs) and sorted_pairs[j][1] == sorted_pairs[i][1]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            original_index = sorted_pairs[k][0]
            ranks[original_index] = avg_rank
        i = j
    return ranks


def mann_whitney_u(x: list[float], y: list[float]) -> float | None:
    if not x or not y:
        return None

    combined = x + y
    ranks = rank_values(combined)
    rank_sum_x = sum(ranks[: len(x)])
    n1 = len(x)
    u1 = rank_sum_x - (n1 * (n1 + 1)) / 2.0
    n2 = len(y)
    u2 = n1 * n2 - u1
    return round(float(min(u1, u2)), 4)


def cliffs_delta(x: list[float], y: list[float]) -> float | None:
    if not x or not y:
        return None

    greater = 0
    less = 0
    for xv in x:
        for yv in y:
            if xv > yv:
                greater += 1
            elif xv < yv:
                less += 1

    return round((greater - less) / (len(x) * len(y)), 4)


def welch_t(x: list[float], y: list[float]) -> tuple[float | None, float | None]:
    if not x or not y:
        return None, None

    n1 = len(x)
    n2 = len(y)
    mean1 = sum(x) / n1
    mean2 = sum(y) / n2
    if n1 < 2 or n2 < 2:
        return round(mean1 - mean2, 4), None

    var1 = pd.Series(x).var(ddof=1)
    var2 = pd.Series(y).var(ddof=1)
    denom = math.sqrt((var1 / n1) + (var2 / n2))
    if denom == 0:
        return 0.0, None
    t_value = (mean1 - mean2) / denom
    numerator = (var1 / n1 + var2 / n2) ** 2
    denominator = ((var1 / n1) ** 2) / (n1 - 1) + ((var2 / n2) ** 2) / (n2 - 1)
    df = numerator / denominator if denominator else None
    return round(float(t_value), 4), round(float(df), 4) if df is not None else None


def cohens_d(x: list[float], y: list[float]) -> float | None:
    if not x or not y:
        return None

    n1 = len(x)
    n2 = len(y)
    if n1 < 2 or n2 < 2:
        return None

    mean1 = sum(x) / n1
    mean2 = sum(y) / n2
    var1 = pd.Series(x).var(ddof=1)
    var2 = pd.Series(y).var(ddof=1)
    pooled_denom = n1 + n2 - 2
    if pooled_denom <= 0:
        return None
    pooled_var = (((n1 - 1) * var1) + ((n2 - 1) * var2)) / pooled_denom
    if pooled_var <= 0:
        return 0.0
    return round((mean1 - mean2) / math.sqrt(pooled_var), 4)


def pairwise_stats(playwright_values: list[float], cypress_values: list[float]) -> dict[str, float | None]:
    welch_t_value, welch_df_value = welch_t(playwright_values, cypress_values)
    return {
        "mann_whitney_u": mann_whitney_u(playwright_values, cypress_values),
        "cliffs_delta": cliffs_delta(playwright_values, cypress_values),
        "welch_t": welch_t_value,
        "welch_df": welch_df_value,
        "cohens_d": cohens_d(playwright_values, cypress_values),
    }


def write_csv(path: str, rows: list[dict]):
    ensure_dir(os.path.dirname(path))
    pd.DataFrame(rows).to_csv(path, index=False, encoding="utf-8-sig")


def build_summary_rows(datasets: list[Dataset], metrics: Iterable[str]) -> list[dict]:
    rows = []
    for dataset in datasets:
        ok = successful_rows(dataset.frame)
        for metric in metrics:
            if metric not in ok.columns:
                continue
            stats = metric_stats(pd.to_numeric(ok[metric], errors="coerce").dropna())
            rows.append(
                {
                    "tool": dataset.tool,
                    "profile": dataset.profile,
                    "metric": metric,
                    **stats,
                }
            )
    return rows


def plot_profile_metric(profile: str, metric: str, playwright_values: list[float], cypress_values: list[float], graphs_dir: str):
    if not playwright_values and not cypress_values:
        return

    ensure_dir(graphs_dir)
    safe_profile = sanitize_filename(profile)
    safe_metric = sanitize_filename(metric)
    output_path = os.path.join(graphs_dir, f"{safe_profile}_{safe_metric}_comparison.png")

    fig, ax = plt.subplots(figsize=(8, 5))
    data = []
    labels = []
    if playwright_values:
        data.append(playwright_values)
        labels.append("Playwright")
    if cypress_values:
        data.append(cypress_values)
        labels.append("Cypress")

    ax.boxplot(data, tick_labels=labels, showmeans=True)

    # Uç noktaları doğrudan kesin değerlerle etiketle.
    for index, values in enumerate(data, start=1):
        min_value = min(values)
        max_value = max(values)
        x_offset = 0.08
        y_padding = (max(values) - min(values)) * 0.02 if max(values) != min(values) else 0.02

        ax.scatter([index, index], [min_value, max_value], color="#333333", s=18, zorder=3)
        ax.annotate(
            f"min {min_value:.4f}",
            xy=(index, min_value),
            xytext=(index + x_offset, min_value - y_padding),
            textcoords="data",
            fontsize=8,
            ha="left",
            va="top",
            arrowprops=dict(arrowstyle="-", color="#666666", lw=0.8),
        )
        ax.annotate(
            f"max {max_value:.4f}",
            xy=(index, max_value),
            xytext=(index + x_offset, max_value + y_padding),
            textcoords="data",
            fontsize=8,
            ha="left",
            va="bottom",
            arrowprops=dict(arrowstyle="-", color="#666666", lw=0.8),
        )

    ax.set_title(f"{profile} | {metric} comparison")
    ax.set_ylabel(metric)
    ax.grid(axis="y", alpha=0.25)
    ax.margins(x=0.18)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def build_comparison_rows(datasets: list[Dataset], metrics: Iterable[str], graphs_dir: str) -> list[dict]:
    by_key = {(dataset.tool, dataset.profile): successful_rows(dataset.frame) for dataset in datasets}
    rows = []
    for profile in PROFILES:
        playwright_frame = by_key.get(("playwright", profile))
        cypress_frame = by_key.get(("cypress", profile))
        if playwright_frame is None or cypress_frame is None:
            continue

        for metric in metrics:
            if metric not in playwright_frame.columns or metric not in cypress_frame.columns:
                continue

            playwright_values = pd.to_numeric(playwright_frame[metric], errors="coerce").dropna().tolist()
            cypress_values = pd.to_numeric(cypress_frame[metric], errors="coerce").dropna().tolist()
            if not playwright_values or not cypress_values:
                continue

            pair_stats = pairwise_stats(playwright_values, cypress_values)
            rows.append(
                {
                    "profile": profile,
                    "metric": metric,
                    "playwright_n": len(playwright_values),
                    "cypress_n": len(cypress_values),
                    **pair_stats,
                }
            )
            plot_profile_metric(profile, metric, playwright_values, cypress_values, graphs_dir)
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-root", default="results")
    parser.add_argument("--tools", nargs="+", default=list(TOOLS), choices=TOOLS)
    parser.add_argument("--profiles", nargs="+", default=list(PROFILES), choices=PROFILES)
    parser.add_argument("--repeat", type=int, default=100)
    parser.add_argument(
        "--metrics",
        nargs="+",
        default=list(DEFAULT_METRICS),
        choices=DEFAULT_METRICS,
    )
    parser.add_argument(
        "--summary-csv",
        default=os.path.join("results", "summaries", "profile_metric_summary.csv"),
    )
    parser.add_argument(
        "--comparison-csv",
        default=os.path.join("results", "summaries", "profile_comparison_stats.csv"),
    )
    parser.add_argument("--graphs-dir", default=os.path.join("results", "graphs"))
    args = parser.parse_args()

    datasets: list[Dataset] = []
    for profile in args.profiles:
        for tool in args.tools:
            dataset = load_dataset(args.results_root, tool, profile, args.repeat)
            if dataset is None:
                print(f"[warn] Eksik veri atlandı: {tool}/{profile}")
                continue
            datasets.append(dataset)

    if not datasets:
        raise SystemExit("Analiz edilecek veri bulunamadı.")

    summary_rows = build_summary_rows(datasets, args.metrics)
    comparison_rows = build_comparison_rows(datasets, args.metrics, args.graphs_dir)

    write_csv(args.summary_csv, summary_rows)
    write_csv(args.comparison_csv, comparison_rows)

    print("Genel summary CSV kaydedildi:", args.summary_csv)
    print("Karşılaştırma CSV kaydedildi:", args.comparison_csv)
    print("Grafikler kaydedildi:", args.graphs_dir)


if __name__ == "__main__":
    main()
