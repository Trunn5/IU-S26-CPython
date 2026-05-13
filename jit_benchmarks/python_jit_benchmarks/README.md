# Python JIT Benchmarks

## Установка и запуск

### 1. Компиляция CPython JIT (в корневой папке проекта)

```bash
cd /Users/prosvirkindm/IdeaProjects/IU-S26-CPython

# Клонировать CPython (если еще не клонирован)
git clone https://github.com/python/cpython.git
cd cpython

# Настроить и скомпилировать с JIT
./configure --enable-experimental-jit
make -j$(nproc)

# Проверить, что JIT работает
PYTHON_JIT=1 ./python.exe -c "print('CPython JIT works!')"
```

### 2. Установка venv для CPython и Numba

```bash
cd jit_benchmarks/python_jit_benchmarks

# Создать venv
python3 -m venv .venv
source .venv/bin/activate

# Установить зависимости
pip install -r requirements.txt
```

### 3. Установка venv для PyPy с NumPy

```bash
# Создать отдельный venv для PyPy
pypy3 -m venv .venv_pypy

# Установить NumPy и psutil
.venv_pypy/bin/pip install numpy psutil
```

### 4. Запуск бенчмарков

```bash
# Запустить все JIT сразу
./run_all.sh

# Или запустить каждый JIT отдельно:
python3 run_single_jit.py cpython
.venv/bin/python3 run_single_jit.py numba_nopython
.venv/bin/python3 run_single_jit.py numba_object
.venv_pypy/bin/pypy3 run_single_jit.py pypy
PYTHON_JIT=1 ../../cpython/python.exe run_single_jit.py cpython_jit
```

### 5. Просмотр результатов

```bash
# Сгенерировать HTML отчет (если не запускали run_all.sh)
python3 visualize_results.py

# Открыть отчет в браузере
open results/comparison_report.html
```
