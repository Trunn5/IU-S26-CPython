# S26-CPython: JIT

## Зависимости
 - python - Python 3.14.3
 - pypy3 - [PyPy 7.3.17 with GCC Apple LLVM 17.0.0 (clang-1700.3.19.1)]
 - cpython - Jit сборка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```bash
git clone https://github.com/python/cpython.git
cd cpython

./configure --enable-experimental-jit
make -j$(nproc)

PYTHON_JIT=1 ./python.exe -c "print('CPython JIT works!')"
```

## 📁 Структура проекта

### Домашние задания
- `homeworks/*`

### Теоретическая часть (Доклад)
- `JIT - CPython S26.pdf` - Презентация
- `CONCLUSIONS.md` - Выводы по исследованию JIT
- `jit_benchmarks/python_jit_examples/` - Примеры использования JIT
- `jit_benchmarks/THEORY.md` - Детальная теория JIT-компиляции

### Практическая часть (Бенчмарки)
- `jit_benchmarks/python_jit_benchmarks/` - Сравнение Python JIT компиляторов
  - 30 функций в 6 категориях
  - 5 JIT: CPython, PyPy, Numba (nopython + object), CPython JIT
  - Измерение времени и памяти
  - HTML отчет с графиками

**Запуск:**
```bash
cd jit_benchmarks/python_jit_benchmarks
./run_all.sh
open results/comparison_report.html
```

### Лабораторная работа (Кросс-языковое сравнение)
- `jit_benchmarks/cross_language_jit_benchmarks/` - Сравнение JIT разных языков
  - Python (CPython + PyPy)
  - JavaScript (Node.js V8)
  - Java (HotSpot JVM)
  - C# (.NET RyuJIT)

**Запуск:**
```bash
cd jit_benchmarks/cross_language_jit_benchmarks
./run_all.sh
open results/report.html
```