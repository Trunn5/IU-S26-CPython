#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "Cross-Language JIT Benchmarks"
echo "========================================"
echo ""

# Проверка доступности рантаймов
echo "Checking available runtimes..."
echo ""

PYTHON_OK=false
PYPY_OK=false
NODE_OK=false
JAVA_OK=false
DOTNET_OK=false

if command -v python3 &> /dev/null; then
    echo "✅ Python: $(python3 --version)"
    PYTHON_OK=true
else
    echo "❌ Python: not found"
fi

if command -v pypy3 &> /dev/null; then
    echo "✅ PyPy: $(pypy3 --version)"
    PYPY_OK=true
else
    echo "❌ PyPy: not found"
fi

if command -v node &> /dev/null; then
    echo "✅ Node.js: $(node --version)"
    NODE_OK=true
else
    echo "❌ Node.js: not found"
fi

if command -v java &> /dev/null; then
    echo "✅ Java: $(java -version 2>&1 | head -n 1)"
    JAVA_OK=true
else
    echo "❌ Java: not found"
fi

if command -v dotnet &> /dev/null; then
    echo "✅ .NET: $(dotnet --version)"
    DOTNET_OK=true
else
    echo "❌ .NET: not found"
fi

echo ""
echo "========================================"
echo "Running benchmarks..."
echo "========================================"
echo ""

# Запуск бенчмарков
python3 run_all.py

echo ""
echo "========================================"
echo "Done!"
echo "========================================"
echo ""
echo "Results:"
echo "  - CSV: results/benchmark_results.csv"
echo "  - HTML: results/report.html"
echo ""
echo "Open the HTML report:"
echo "  open results/report.html"
