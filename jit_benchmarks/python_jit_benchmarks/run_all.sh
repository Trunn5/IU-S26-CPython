#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Running Python JIT Benchmarks"
echo "=============================="

[ -f "results/results.json" ] && rm results/results.json

../../.venv/bin/python3 check_availability.py

echo ""
echo "CPython..."
python3 run_single_jit.py cpython

if [ -f "../../.venv/bin/python3" ]; then
    echo ""
    echo "Numba (nopython=True)..."
    ../../.venv/bin/python3 run_single_jit.py numba_nopython
    echo ""
    echo "Numba (nopython=False, object mode)..."
    ../../.venv/bin/python3 run_single_jit.py numba_object
fi

if [ -f "../../.venv_pypy/bin/pypy3" ]; then
    echo ""
    echo "PyPy (with NumPy)..."
    ../../.venv_pypy/bin/pypy3 run_single_jit.py pypy
elif command -v pypy3 &> /dev/null; then
    echo ""
    echo "PyPy..."
    pypy3 run_single_jit.py pypy
fi

if [ -f "../../cpython/python.exe" ]; then
    echo ""
    echo "CPython JIT..."
    PYTHON_JIT=1 ../../cpython/python.exe run_single_jit.py cpython_jit
fi

echo ""
echo "Generating report..."
python3 visualize_results.py

echo ""
echo "Done! Open results/comparison_report.html"
