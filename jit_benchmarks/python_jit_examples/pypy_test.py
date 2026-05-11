# pypy3 pypy_test.py
# Для JIT-логов:
#   PYPYLOG=jit-log-opt,jit-backend:jit.log pypy3 pypy_test.py

import sys
import time
import dis
import os

print("1) Runtime")
print("implementation:", sys.implementation.name)
print("executable:", sys.executable)

try:
    import __pypy__
    print("PyPy: yes")
except ImportError:
    print("PyPy: no, запусти через pypy3")
    raise SystemExit


print("\n2) Обычная Python-функция")

def f(n):
    s = 0
    i = 0
    while i < n:
        s += i + 1
        i += 1
    return s

print("type(f):", type(f))
print("f.__code__:", f.__code__)
print("locals:", f.__code__.co_varnames)

print("\nPython bytecode:")
dis.dis(f)

print("\n3) Запуски функции: JIT прогревается на hot loop")

N = 10_000_000

for k in range(6):
    t0 = time.perf_counter()
    r = f(N)
    t1 = time.perf_counter()
    print(f"run {k + 1}: result={r}, time={t1 - t0:.6f} sec")

print("\n4) JIT logs")
if os.path.exists("../jit.log"):
    with open("../jit.log", "r", errors="ignore") as fp:
        lines = fp.readlines()
    loop_lines = [
        i
        for i, line in enumerate(lines)
        if "jit-log-opt-loop" in line \
           or "# Loop" in line
    ]
    print("Найденные JIT loop-блоки:")
    for i in loop_lines:
        print(f"line {i + 1}: {lines[i].rstrip()}")
else:
    print("\njit.log не найден. PYPYLOG=jit-log-opt,jit-backend:jit.log pypy3 pypy_test.py")
