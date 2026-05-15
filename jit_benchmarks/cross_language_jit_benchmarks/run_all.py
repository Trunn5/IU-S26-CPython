#!/usr/bin/env python3
from config import DEFAULT_REPEAT, DEFAULT_WARMUP, RESULTS_DIR
from reporting import save_csv, write_html_report
from runner import run_benchmarks


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    rows = run_benchmarks(warmup=DEFAULT_WARMUP, repeat=DEFAULT_REPEAT)

    csv_path = RESULTS_DIR / "benchmark_results.csv"
    report_path = RESULTS_DIR / "report.html"

    save_csv(rows, csv_path)
    write_html_report(rows, report_path)

    print(f"\nSaved table: {csv_path}")
    print(f"Saved report: {report_path}")


if __name__ == "__main__":
    main()
