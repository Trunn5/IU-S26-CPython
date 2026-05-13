#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
CPYTHON_JIT_EXE = ROOT.parent.parent / "cpython" / "python.exe"
VENV_PYTHON = ROOT / ".venv" / "bin" / "python3"


def check_import_in_venv(module_name, venv_path):
    if not venv_path.exists():
        return False
    try:
        result = subprocess.run(
            [str(venv_path), "-c", f"import {module_name}"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False


def check_jit_availability():
    available = {}
    
    available["cpython"] = True
    
    if CPYTHON_JIT_EXE.exists():
        try:
            env = os.environ.copy()
            env["PYTHON_JIT"] = "1"
            result = subprocess.run(
                [str(CPYTHON_JIT_EXE), "-c", "import sys; print(hasattr(sys, '_jit'))"],
                capture_output=True,
                text=True,
                timeout=5,
                env=env
            )
            available["cpython_jit"] = "True" in result.stdout
        except Exception:
            available["cpython_jit"] = False
    else:
        available["cpython_jit"] = False
    
    available["pypy"] = subprocess.run(
        ["which", "pypy3"],
        capture_output=True
    ).returncode == 0
    
    available["numba"] = check_import_in_venv("numba", VENV_PYTHON)
    available["jax"] = check_import_in_venv("jax", VENV_PYTHON)
    
    for jit_name, is_available in available.items():
        status = "✅" if is_available else "❌"
        print(f"{status} {jit_name}")
    
    return available


if __name__ == "__main__":
    check_jit_availability()
