#!/usr/bin/env python3
import argparse
import json
import math
import resource
import sys
import time
import tracemalloc
from dis import dis

try:
    from numba import jit
except ImportError:
    print("ERROR: numba is not installed. Install: pip install numba", file=sys.stderr)
    sys.exit(1)


@jit(nopython=True)
def fibonacci_iter(n: int) -> int:
    mod = 1_000_000_007
    a, b = 0, 1
    for _ in range(n):
        a, b = b, (a + b) % mod
    return a


@jit(nopython=True)
def prime_count(limit: int) -> int:
    if limit < 2:
        return 0
    count = 0
    for n in range(2, limit + 1):
        is_prime = True
        root = int(math.sqrt(n))
        for d in range(2, root + 1):
            if n % d == 0:
                is_prime = False
                break
        if is_prime:
            count += 1
    return count


@jit(nopython=True)
def matrix_mul(size: int) -> int:
    a = [[0 for _ in range(size)] for _ in range(size)]
    b = [[0 for _ in range(size)] for _ in range(size)]
    c = [[0 for _ in range(size)] for _ in range(size)]
    
    for i in range(size):
        for j in range(size):
            a[i][j] = (i + j) % 10
            b[i][j] = (i * j) % 7
    
    for i in range(size):
        for k in range(size):
            aik = a[i][k]
            for j in range(size):
                c[i][j] += aik * b[k][j]
    return c[0][0]


def json_roundtrip(items: int) -> int:
    import json as pyjson

    payload = []
    for i in range(items):
        payload.append(
            {
                "id": i,
                "name": f"user_{i}",
                "active": (i % 2 == 0),
                "score": i * 1.5,
                "tags": [f"tag_{i % 10}", f"group_{i % 5}"],
            }
        )
    encoded = pyjson.dumps(payload, ensure_ascii=False)
    decoded = pyjson.loads(encoded)
    return len(decoded)


@jit(nopython=True)
def polymorphic_add_inner(iterations: int) -> int:
    result = 0
    for i in range(iterations):
        result = i + i + 1
    for i in range(iterations):
        result = int(float(i) + float(i) + 1.5)
    for i in range(iterations):
        result = i + i + 1
    return result


def polymorphic_add(iterations: int) -> int:
    return polymorphic_add_inner(iterations)


@jit(nopython=True)
def polymorphic_list_ops_inner(iterations: int) -> int:
    result = 0
    for i in range(iterations):
        total = 0
        for j in range(5):
            total += i + j
        result += total
    return result % 1_000_000


def polymorphic_list_ops(iterations: int) -> int:
    return polymorphic_list_ops_inner(iterations)


@jit(nopython=True)
def type_switching_loop_inner(iterations: int) -> int:
    result = 0
    for i in range(iterations):
        if i % 2 == 0:
            result += i * 2 + 1
        else:
            result += int(float(i) * 2.0 + 1.0)
    return result % 1_000_000


def type_switching_loop(iterations: int) -> int:
    return type_switching_loop_inner(iterations)


BENCHMARKS = {
    "fibonacci_iter": lambda: fibonacci_iter(180_000),
    "prime_count": lambda: prime_count(20_000),
    "matrix_mul": lambda: matrix_mul(120),
    "json_roundtrip": lambda: json_roundtrip(20_000),
    "polymorphic_add": lambda: polymorphic_add(50_000),
    "polymorphic_list_ops": lambda: polymorphic_list_ops(20_000),
    "type_switching_loop": lambda: type_switching_loop(100_000),
}


def run_single(name: str, warmup: int, repeat: int) -> dict:
    fn = BENCHMARKS[name]
    sink = 0
    for _ in range(warmup):
        sink ^= int(fn()) & 0xFFFFFFFF

    times = []
    peaks = []
    for _ in range(repeat):
        # if tracemalloc is not None:
        #     tracemalloc.start()
        before_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        start = time.perf_counter()
        sink ^= int(fn()) & 0xFFFFFFFF
        # print(dir(fn))
        # print(fn.__code__)
        # print(fn.__code__.__dir__())
        print(fibonacci_iter.__call__)
        print(dis(fibonacci_iter.__call__))
        elapsed = (time.perf_counter() - start) * 1000.0
        if tracemalloc is not None:
            _, peak = tracemalloc.get_traced_memory()
            # tracemalloc.stop()
            peak_kb = peak / 1024.0
        else:
            after_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            peak_kb = max(0.0, float(after_rss - before_rss))
        times.append(elapsed)
        peaks.append(peak_kb)

    return {
        "benchmark": name,
        "time_ms": sum(times) / len(times),
        "memory_kb": sum(peaks) / len(peaks),
        "sink": sink,
    }


def main() -> None:
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--benchmark", choices=sorted(BENCHMARKS.keys()), required=True)
    # parser.add_argument("--warmup", type=int, default=5)
    # parser.add_argument("--repeat", type=int, default=7)
    # args = parser.parse_args()
    # print(json.dumps(run_single(args.benchmark, args.warmup, args.repeat), ensure_ascii=False))

    print(json.dumps(run_single("fibonacci_iter", 3000, 1), ensure_ascii=False))
    tracemalloc.start()
    a = ["a"] * 100
    b = a[99]
    b += "a"
    del a
    x = tracemalloc.get_traced_memory()
    print(x)
    tracemalloc.stop()

if __name__ == "__main__":

    main()
