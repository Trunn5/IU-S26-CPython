import json

from config import BENCHMARKS, ROOT
from runtimes import detect_runtimes
from shell_utils import run_cmd


def run_benchmarks(warmup: int, repeat: int) -> list[dict]:
    runtimes = detect_runtimes()
    if not runtimes:
        raise RuntimeError("No supported runtimes found.")
    
    print("Detected runtimes:")
    for runtime in runtimes:
        print(f"- {runtime.name}")

    rows: list[dict] = []
    for runtime in runtimes:
        print(f"\nPreparing {runtime.name}...")
        try:
            if runtime.prepare_command:
                cwd = ROOT / "benchmarks" / "java" / "src" if "Java" in runtime.name else ROOT
                run_cmd(runtime.prepare_command, cwd=cwd)
        except Exception as exc:
            print(f"Skipping {runtime.name}: prepare step failed ({exc})")
            continue

        for bench in BENCHMARKS:
            try:
                cmd = runtime.command_builder(bench, warmup, repeat)
                output = run_cmd(cmd)
                payload = json.loads(output.splitlines()[-1])
                row = {
                    "runtime": runtime.name,
                    "benchmark": payload["benchmark"],
                    "time_ms": round(float(payload["time_ms"]), 3),
                    "memory_kb": round(float(payload["memory_kb"]), 3),
                }
                rows.append(row)
                print(
                    f"{runtime.name:20} | {bench:15} | "
                    f"{row['time_ms']:10.3f} ms | {row['memory_kb']:10.3f} KB"
                )
            except Exception as exc:
                print(f"Skipping {runtime.name} {bench}: failed ({exc})")
                break

    if not rows:
        raise RuntimeError("No successful benchmark runs.")

    return rows
