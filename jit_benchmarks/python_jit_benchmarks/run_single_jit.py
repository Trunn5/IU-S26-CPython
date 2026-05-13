#!/usr/bin/env python3
import argparse
import gc
import json
import sys
import time
from pathlib import Path

try:
    import tracemalloc
    HAS_TRACEMALLOC = True
except (ImportError, ModuleNotFoundError):
    print("SKIP tracemalloc")
    HAS_TRACEMALLOC = False

try:
    import psutil
    HAS_PSUTIL = True
except (ImportError, ModuleNotFoundError):
    print("SKIP psutil")
    HAS_PSUTIL = False

try:
    import resource
    HAS_RESOURCE = True
except (ImportError, ModuleNotFoundError):
    print("SKIP resource")
    HAS_RESOURCE = False

ROOT = Path(__file__).parent
TASKS_DIR = ROOT / "tasks"
RESULTS_FILE = ROOT / "results" / "results.json"

sys.path.insert(0, str(TASKS_DIR))

TASKS = [
    "control_flow",
    "simple_loop",
    "numpy_ops",
    "dynamic_structures",
    "oop_code",
    "python_features",
]


def apply_jit_decorator(func, jit_name):
    if jit_name in ["cpython", "cpython_jit", "pypy"]:
        return func
    elif jit_name == "numba_nopython":
        from numba import jit
        try:
            return jit(nopython=True)(func)
        except Exception as e:
            print(f"SKIP {func.__name__} (Numba nopython=True): {type(e).__name__}: {str(e)[:100]}")
            return None
    elif jit_name == "numba_object":
        from numba import jit
        try:
            return jit(forceobj=True)(func)
        except Exception as e:
            print(f"SKIP {func.__name__} (Numba forceobj): {type(e).__name__}: {str(e)[:100]}")
            return None
    elif jit_name == "jax":
        import jax
        try:
            return jax.jit(func)
        except Exception as e:
            print(f"SKIP {func.__name__} (JAX): {type(e).__name__}: {str(e)[:100]}")
            return None
    return func


def measure_time_and_memory(func, params, jit_name, warmup=3, measure=5):
    try:
        for _ in range(warmup):
            _ = func(**params)
    except Exception as e:
        print(f"SKIP {func.__name__} (warmup failed): {type(e).__name__}: {str(e)[:100]}")
        return None
    
    times = []
    memories = []
    
    for _ in range(measure):
        gc.collect()
        
        mem_before = 0
        process = None
        if HAS_TRACEMALLOC:
            tracemalloc.start()
        elif HAS_PSUTIL:
            process = psutil.Process()
            gc.collect()
            mem_before = process.memory_info().rss
        elif HAS_RESOURCE:
            mem_before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        
        start = time.perf_counter()
        try:
            result = func(**params)
            
            if jit_name == "jax" and hasattr(result, "block_until_ready"):
                result.block_until_ready()
        except Exception as e:
            if HAS_TRACEMALLOC:
                tracemalloc.stop()
            print(f"SKIP {func.__name__} (execution failed): {type(e).__name__}: {str(e)[:100]}")
            return None
        
        elapsed = (time.perf_counter() - start) * 1000
        
        if HAS_TRACEMALLOC:
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            memories.append(peak / 1024)
        elif HAS_PSUTIL:
            gc.collect()
            mem_after = process.memory_info().rss
            mem_used = (mem_after - mem_before) / 1024
            if mem_used < 0:
                mem_used = 0
            memories.append(mem_used)
        elif HAS_RESOURCE:
            mem_after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            mem_used = (mem_after - mem_before) / 1024
            memories.append(max(0, mem_used))
        else:
            memories.append(0)
        
        times.append(elapsed)
    
    return {
        "time_ms": sum(times) / len(times),
        "memory_kb": sum(memories) / len(memories),
        "result": str(result)[:100]
    }


def run_task(task_name, jit_name):
    try:
        task_module = __import__(task_name)
        benchmark_params = getattr(task_module, "BENCHMARK_PARAMS", {})
        
        results = []
        for func_name, params in benchmark_params.items():
            func = getattr(task_module, func_name, None)
            if func is None:
                continue
            
            jit_func = apply_jit_decorator(func, jit_name)
            if jit_func is None:
                continue
            
            metrics = measure_time_and_memory(jit_func, params, jit_name)
            if metrics:
                results.append({
                    "task": task_name,
                    "function": func_name,
                    "jit": jit_name,
                    **metrics
                })
        
        return results
    except Exception as e:
        print(f"ERROR in {task_name}: {type(e).__name__}: {e}")
        return []


def load_results():
    if RESULTS_FILE.exists():
        try:
            with open(RESULTS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_results(new_results, jit_name):
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    all_results = load_results()
    all_results = [r for r in all_results if r.get("jit") != jit_name]
    all_results.extend(new_results)
    
    with open(RESULTS_FILE, "w") as f:
        json.dump(all_results, f, indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("jit", choices=["cpython", "cpython_jit", "pypy", "numba_object", "numba_nopython", "jax"])
    parser.add_argument("--tasks", nargs="+")
    args = parser.parse_args()
    
    jit_name = args.jit
    tasks_to_run = args.tasks if args.tasks else TASKS
    
    if jit_name == "cpython_jit" and not hasattr(sys, '_jit'):
        print(f"ERROR: CPython JIT not enabled. Use: PYTHON_JIT=1 python.exe")
        return
    
    all_results = []
    for task_name in tasks_to_run:
        if task_name not in TASKS:
            continue
        results = run_task(task_name, jit_name)
        all_results.extend(results)
    
    save_results(all_results, jit_name)
    print(f"Saved {len(all_results)} results for {jit_name}")


if __name__ == "__main__":
    main()
