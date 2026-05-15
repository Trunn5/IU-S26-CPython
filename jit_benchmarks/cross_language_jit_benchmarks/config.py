from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Базовые бенчмарки (поддерживаются всеми языками)
BENCHMARKS = ["fibonacci_iter", "prime_count", "matrix_mul", "json_roundtrip"]

# Расширенные бенчмарки с полиморфизмом (только Python)
BENCHMARKS_EXTENDED = BENCHMARKS + [
    "polymorphic_add",
    "polymorphic_attr_access",
    "polymorphic_list_ops",
    "type_switching_loop",
]

# Бенчмарки поддерживаемые Numba (nopython mode)
BENCHMARKS_NUMBA = [
    "fibonacci_iter",
    "prime_count",
    "matrix_mul",
    "json_roundtrip",
    "polymorphic_add",
    "polymorphic_list_ops",
    "type_switching_loop",
]

DEFAULT_WARMUP = 10
DEFAULT_REPEAT = 10
RESULTS_DIR = ROOT / "results"
