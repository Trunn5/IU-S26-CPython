# jax_test.py
#
# Запуск:
#   JAX_LOG_COMPILES=1 python jax_test.py

import time
import jax
import jax.numpy as jnp


print("JAX:", jax.__version__)
print("backend:", jax.default_backend())
print("devices:", jax.devices())


def model(x, y):
    return x + y


x = 1 # jnp.linspace(-1.0, 1.0, 4)
y = 3 # jnp.arange(16.0).reshape(4, 4) / 10.0


print("\n1) Inputs")
print("x:", x)
print("y:", y)


print("\n2) JAXPR: граф зависимостей")

print(jax.make_jaxpr(model)(x, y))


print("\n3) jax.jit wrapper")

jmodel = jax.jit(model)

print("type(jmodel):", type(jmodel))
print("jmodel:", jmodel)


print("\n4) StableHLO / MLIR")

lowered = jmodel.lower(x, y)
stablehlo = lowered.compiler_ir(dialect="stablehlo")
print(stablehlo)


print("\n5) Первый вызов: tracing/lowering/XLA compile + execution")

t0 = time.perf_counter()
r1 = jmodel(x, y)#.block_until_ready()
t1 = time.perf_counter()

print("result:", r1)
print("first call time:", t1 - t0)


print("\n6) Второй вызов: cached executable")

t0 = time.perf_counter()
r2 = jmodel(x, y)#.block_until_ready()
t1 = time.perf_counter()

print("result:", r2)
print("second call time:", t1 - t0)
