"""
Циклы и ветвления которые зависят от runtime данных..

Почему PyPy/Numba хороши:
- Tracing JIT (PyPy) записывает фактический путь выполнения
- LLVM (Numba) может оптимизировать dynamic branches
"""

def collatz_sequence(n: int, max_steps: int) -> int:
    """
    Последовательность Коллатца (3n+1 проблема).
    
    Control flow полностью зависит от runtime значений.
    
    Args:
        n: начальное число
        max_steps: максимум шагов
        
    Returns:
        количество шагов до достижения 1
    """
    steps = 0
    while n != 1 and steps < max_steps:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps


def branching_heavy(iterations: int) -> int:
    """
    Много ветвлений зависящих от данных.
    
    Args:
        iterations: количество итераций
        
    Returns:
        результат вычислений
    """
    result = 0
    for i in range(iterations):
        x = i % 100
        
        if x < 10:
            result += x * 2
        elif x < 30:
            result += x ** 2
        elif x < 50:
            result += x // 2
        elif x < 70:
            result -= x
        elif x < 90:
            result += x * 3
        else:
            result -= x // 3
    
    return result % 1_000_000_007


def early_exit_search(arr_size: int, target_ratio: float) -> int:
    """
    Поиск с ранним выходом.
    
    Args:
        arr_size: размер массива
        target_ratio: на какой позиции найти (0.0-1.0)
        
    Returns:
        индекс найденного элемента
    """
    data = list(range(arr_size))
    target = int(arr_size * target_ratio)
    
    found_index = -1
    for i, value in enumerate(data):
        if value == target:
            found_index = i
            break
    
    return found_index


def nested_conditions(n: int) -> int:
    """
    Глубоко вложенные условия.
    
    Args:
        n: количество итераций
        
    Returns:
        результат
    """
    result = 0
    
    for i in range(n):
        x = i % 17
        
        if x % 2 == 0:
            if x % 4 == 0:
                if x % 8 == 0:
                    result += x * 4
                else:
                    result += x * 2
            else:
                result += x
        else:
            if x % 3 == 0:
                result -= x
            else:
                if x % 5 == 0:
                    result += x * 3
                else:
                    result -= x // 2
    
    return result % 1_000_000_007


def state_machine(iterations: int) -> int:
    """
    Простой конечный автомат.
    
    State transitions зависят от текущего состояния.
    
    Args:
        iterations: количество переходов
        
    Returns:
        финальное состояние
    """
    state = 0
    counter = 0
    
    for i in range(iterations):
        if state == 0:
            if i % 3 == 0:
                state = 1
            else:
                state = 2
                counter += 1
        elif state == 1:
            if i % 2 == 0:
                state = 2
                counter += 2
            else:
                state = 0
        elif state == 2:
            if i % 5 == 0:
                state = 0
                counter += 3
            else:
                state = 1
        
        counter += i % 10
    
    return counter % 1_000_000_007


# Параметры для бенчмарка
BENCHMARK_PARAMS = {
    "collatz_sequence": {"n": 27, "max_steps": 10_000_000},  # Известное долгое значение
    "branching_heavy": {"iterations": 1_000_000},
    "early_exit_search": {"arr_size": 1_000_000, "target_ratio": 0.5},
    "nested_conditions": {"n": 1_000_000},
    "state_machine": {"iterations": 1_000_000},
}
