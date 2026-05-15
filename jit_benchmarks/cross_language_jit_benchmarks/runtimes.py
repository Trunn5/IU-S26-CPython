import shutil
import sys

from config import ROOT
from models import Runtime
from shell_utils import command_works


def detect_runtimes() -> list[Runtime]:
    runtimes: list[Runtime] = []
    python_script = ROOT / "benchmarks" / "python" / "tasks.py"
    runtimes.append(
        Runtime(
            name="CPython",
            command_builder=lambda bench, warmup, repeat: [
                sys.executable,
                str(python_script),
                "--benchmark",
                bench,
                "--warmup",
                str(warmup),
                "--repeat",
                str(repeat),
            ],
        )
    )

    pypy = shutil.which("pypy3")
    if pypy:
        runtimes.append(
            Runtime(
                name="PyPy",
                command_builder=lambda bench, warmup, repeat: [
                    pypy,
                    str(python_script),
                    "--benchmark",
                    bench,
                    "--warmup",
                    str(warmup),
                    "--repeat",
                    str(repeat),
                ],
            )
        )

    node = shutil.which("node")
    if node:
        js_script = ROOT / "benchmarks" / "js" / "tasks.js"
        runtimes.append(
            Runtime(
                name="V8 (Node.js)",
                command_builder=lambda bench, warmup, repeat: [
                    node,
                    str(js_script),
                    "--benchmark",
                    bench,
                    "--warmup",
                    str(warmup),
                    "--repeat",
                    str(repeat),
                ],
            )
        )

    java = shutil.which("java")
    javac = shutil.which("javac")
    if java and javac and command_works([java, "-version"]) and command_works([javac, "-version"]):
        java_src = ROOT / "benchmarks" / "java" / "src"
        runtimes.append(
            Runtime(
                name="Java (HotSpot JIT)",
                prepare_command=[javac, "Benchmarks.java"],
                command_builder=lambda bench, warmup, repeat: [
                    java,
                    "-cp",
                    str(java_src),
                    "Benchmarks",
                    "--benchmark",
                    bench,
                    "--warmup",
                    str(warmup),
                    "--repeat",
                    str(repeat),
                ],
            )
        )

    dotnet = shutil.which("dotnet")
    if dotnet and command_works([dotnet, "--version"]):
        csproj = ROOT / "benchmarks" / "csharp" / "Benchmarks.csproj"
        runtimes.append(
            Runtime(
                name="C# (.NET JIT)",
                prepare_command=[dotnet, "build", str(csproj), "-c", "Release", "-nologo"],
                command_builder=lambda bench, warmup, repeat: [
                    dotnet,
                    "run",
                    "--project",
                    str(csproj),
                    "-c",
                    "Release",
                    "--no-build",
                    "--",
                    "--benchmark",
                    bench,
                    "--warmup",
                    str(warmup),
                    "--repeat",
                    str(repeat),
                ],
            )
        )

    return runtimes
