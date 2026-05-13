"""
Операции с NumPy массивами.

Почему PyPy плох:
- PyPy JIT не оптимизирует C-extensions (NumPy написан на C)
- Overhead на вызовы C функций
- Нет fusion операций
"""

import numpy as np


def matrix_multiply(size: int) -> float:
    """
    Умножение матриц через NumPy.
    
    Args:
        size: размер квадратных матриц
        
    Returns:
        сумма элементов результата
    """
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    C = np.matmul(A, B)
    return float(np.sum(C))


def vector_operations(n: int) -> float:
    """
    Последовательность векторных операций.
    
    Args:
        n: размер векторов
        
    Returns:
        результат вычислений
    """
    x = np.linspace(0, 10, n)
    y = np.sin(x) ** 2 + np.cos(x) ** 2
    z = np.exp(-x / 10) * y
    w = np.sqrt(np.abs(z)) + np.log(np.abs(z) + 1)
    return float(np.mean(w))


def array_reduction(shape: tuple) -> float:
    """
    Операции редукции на многомерных массивах.
    
    Args:
        shape: форма массива
        
    Returns:
        результат редукции
    """
    data = np.random.rand(*shape)
    
    # Последовательность редукций
    sum_result = np.sum(data, axis=0)
    mean_result = np.mean(sum_result, axis=0)
    max_result = np.max(mean_result)
    
    return float(max_result)


def stencil_operation(size: int) -> float:
    """
    Stencil операция (соседние элементы).
    
    Типичная операция в численных методах.
    
    Args:
        size: размер 2D grid
        
    Returns:
        сумма результата
    """
    grid = np.random.rand(size, size)
    
    # 5-point stencil
    result = (
        grid[1:-1, 1:-1] * 4.0
        - grid[:-2, 1:-1]
        - grid[2:, 1:-1]
        - grid[1:-1, :-2]
        - grid[1:-1, 2:]
    )
    
    return float(np.sum(result))


# Параметры для бенчмарка
BENCHMARK_PARAMS = {
    "matrix_multiply": {"size": 500},
    "vector_operations": {"n": 1_000_000},
    "array_reduction": {"shape": (100, 100, 100)},
    "stencil_operation": {"size": 1000},
}
