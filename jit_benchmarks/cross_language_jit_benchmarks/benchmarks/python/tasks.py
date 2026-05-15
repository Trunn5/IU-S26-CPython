#!/usr/bin/env python3
import argparse
import json
import math
import resource
import time
try:
    import tracemalloc
except Exception:
    tracemalloc = None


def fibonacci_iter(n: int) -> int:
    mod = 1_000_000_007
    a, b = 0, 1
    for _ in range(n):
        a, b = b, (a + b) % mod
    return a


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


def matrix_mul(size: int) -> int:
    a = [[(i + j) % 10 for j in range(size)] for i in range(size)]
    b = [[(i * j) % 7 for j in range(size)] for i in range(size)]
    c = [[0 for _ in range(size)] for _ in range(size)]
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


def polymorphic_add(iterations: int) -> int:
    """
    Стресс-тест: JIT компилирует для int, потом резко переключается на float.
    Проверяет деоптимизацию при смене типов.
    """
    def add_values(a, b):
        return a + b
    
    result = 0
    # Фаза 1: прогрев с int - JIT оптимизируется под int
    for i in range(iterations):
        result = int(add_values(i, i + 1))
    
    # Фаза 2: резкое переключение на float - вызываем деоптимизацию
    for i in range(iterations):
        result = int(add_values(float(i), float(i) + 1.5))
    
    # Фаза 3: обратно на int
    for i in range(iterations):
        result = int(add_values(i, i + 1))
    
    return result


def polymorphic_attr_access(iterations: int) -> int:
    """
    Стресс-тест: доступ к атрибутам разных классов.
    JIT сначала оптимизируется под один класс, потом встречает другой.
    """
    class Point2D:
        def __init__(self, x, y):
            self.x = x
            self.y = y
        
        def compute(self):
            return self.x + self.y
    
    class Point3D:
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z
        
        def compute(self):
            return self.x + self.y + self.z
    
    def process_point(point):
        return point.compute()
    
    result = 0
    # Фаза 1: только Point2D
    for i in range(iterations):
        p = Point2D(i, i + 1)
        result += int(process_point(p))
    
    # Фаза 2: резко переключаемся на Point3D
    for i in range(iterations):
        p = Point3D(i, i + 1, i + 2)
        result += int(process_point(p))
    
    # Фаза 3: снова Point2D
    for i in range(iterations):
        p = Point2D(i, i + 1)
        result += int(process_point(p))
    
    return result % 1_000_000


def polymorphic_list_ops(iterations: int) -> int:
    """
    Стресс-тест: операции со списками разных типов элементов.
    Сначала однородный список int, потом смешанный список.
    """
    def sum_list(lst):
        total = 0
        for item in lst:
            total += item
        return total
    
    result = 0
    # Фаза 1: однородные списки int
    for i in range(iterations):
        lst = [i, i + 1, i + 2, i + 3, i + 4]
        result += int(sum_list(lst))
    
    # Фаза 2: смешанные типы (int, float)
    for i in range(iterations):
        lst = [i, float(i + 1), i + 2, float(i + 3), i + 4]
        result += int(sum_list(lst))
    
    # Фаза 3: обратно на int
    for i in range(iterations):
        lst = [i, i + 1, i + 2, i + 3, i + 4]
        result += int(sum_list(lst))
    
    return result % 1_000_000


def type_switching_loop(iterations: int) -> int:
    """
    Стресс-тест: переключение типов внутри одного цикла.
    Максимально тяжелый сценарий для JIT.
    """
    def compute(x):
        return x * 2 + 1
    
    result = 0
    for i in range(iterations):
        # Чередуем типы на каждой итерации
        if i % 2 == 0:
            result += int(compute(i))
        else:
            result += int(compute(float(i)))
    
    return result % 1_000_000


BENCHMARKS = {
    "fibonacci_iter": lambda: fibonacci_iter(180_000),
    "prime_count": lambda: prime_count(20_000),
    "matrix_mul": lambda: matrix_mul(120),
    "json_roundtrip": lambda: json_roundtrip(20_000),
    # Стресс-тесты для проверки переключения типов в JIT
    "polymorphic_add": lambda: polymorphic_add(50_000),
    "polymorphic_attr_access": lambda: polymorphic_attr_access(15_000),
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
        if tracemalloc is not None:
            tracemalloc.start()
        before_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        start = time.perf_counter()
        sink ^= int(fn()) & 0xFFFFFFFF
        elapsed = (time.perf_counter() - start) * 1000.0
        if tracemalloc is not None:
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", choices=sorted(BENCHMARKS.keys()), required=True)
    parser.add_argument("--warmup", type=int, default=5)
    parser.add_argument("--repeat", type=int, default=7)
    args = parser.parse_args()
    print(json.dumps(run_single(args.benchmark, args.warmup, args.repeat), ensure_ascii=False))


if __name__ == "__main__":
    main()
