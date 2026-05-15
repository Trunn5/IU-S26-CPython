# Python JIT Examples

Практические примеры использования JIT компиляторов в Python.

## Файлы

- `numba_test.ipynb` - Numba JIT (LLVM), примеры с NumPy
- `cpython_test.py` - CPython JIT (experimental, 3.13+), `sys._jit` API
- `pypy_test.py` - PyPy tracing JIT, hot loops
- `jax_test.py` - JAX XLA JIT, JAXPR/StableHLO

## Запуск

```bash
# Numba (notebook)
jupyter notebook numba_test.ipynb

# CPython JIT
python3 cpython_test.py
PYTHON_JIT=1 /path/to/cpython/python.exe cpython_test.py

# PyPy
pypy3 pypy_test.py
PYPYLOG=jit-log-opt:jit.log pypy3 pypy_test.py

# JAX
python3 jax_test.py
JAX_LOG_COMPILES=1 python3 jax_test.py
```

## Установка зависимостей

См. [корневой README](../../README.md) для установки всех зависимостей.
