# cpython_test.py
#
# Запуск:
#   python cpython_test.py
#
#   PYTHON_JIT=1 ./python.exe /Users/prosvirkindm/IdeaProjects/IU-S26-CPython/jit_benchmarks/cpython_test.py

import sys
import time
import dis


print("1) Runtime")
print("implementation:", sys.implementation.name)
print("version:", sys.version)
print("executable:", sys.executable)


print("\n2) CPython JIT API")

jit = getattr(sys, "_jit", None)

if jit is None:
    print("sys._jit: not available")
    print("Этот Python не имеет публичного experimental JIT API.")
else:
    print("sys._jit:", jit)

    for name in ["is_available", "is_enabled", "is_active"]:
        attr = getattr(jit, name, None)
        if attr is None:
            print(f"sys._jit.{name}: not found")
        else:
            try:
                print(f"sys._jit.{name}():", attr())
            except Exception as e:
                print(f"sys._jit.{name}() error:", type(e).__name__, e)


print("\n3) Обычная Python-функция")

first_jit_i = None

def f(n):
    global first_jit_i

    s = 0
    i = 0
    while i < n:
        if first_jit_i is None and sys._jit.is_active():
            first_jit_i = i

        s += i + 1
        i += 1
    return s

print("type(f):", type(f))
print("f:", f)
print("f.__code__:", f.__code__)
print("locals:", f.__code__.co_varnames)


# print("\n4) CPython bytecode")
# dis.dis(f, adaptive=True, show_caches=True)


print("\n5) Прогрев функции")

N = 10_000_000

for k in range(6):
    first_jit_i = None

    t0 = time.perf_counter()
    r = f(N)
    t1 = time.perf_counter()

    print(f"run {k + 1}: result={r}, time={t1 - t0:.6f} sec, first_jit_i={first_jit_i}")

# print("\n6) Bytecode после прогрева")
# dis.dis(f, adaptive=True, show_caches=True)

print("\n7) После JIT функция всё ещё обычная")
print("type(f):", type(f))
print("f.__dict__:", getattr(f, "__dict__", None))
print("f.__code__:", f.__code__)
