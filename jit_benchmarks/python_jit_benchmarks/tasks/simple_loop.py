"""
Простой цикл с арифметическими операциями.

Базовая оптимизация циклов и арифметики.
"""

def simple_loop(n: int) -> int:
    """
    Простой цикл с накоплением суммы.
    n^2
    """
    result = 0
    for i in range(n):
        result += i * 2 + 1
    return result


def fibonacci_loop(n: int) -> int:
    """
    Вычисление n-го числа Фибоначчи итеративно.
    """
    mod = 1_000_000_007
    a, b = 0, 1
    for _ in range(n):
        a, b = b, (a + b) % mod
    return a


def prime_count_loop(limit: int) -> int:
    """
    Подсчет простых чисел до limit.
    """
    count = 0
    for n in range(2, limit + 1):
        is_prime = True
        for d in range(2, int(n ** 0.5) + 1):
            if n % d == 0:
                is_prime = False
                break
        if is_prime:
            count += 1
    return count


# Параметры для бенчмарка
BENCHMARK_PARAMS = {
    "simple_loop": {"n": 10_000_000},
    "fibonacci_loop": {"n": 100_000},
    "prime_count_loop": {"limit": 100_000},
}
