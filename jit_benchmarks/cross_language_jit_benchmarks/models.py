from dataclasses import dataclass
from typing import Callable


@dataclass
class Runtime:
    name: str
    command_builder: Callable[[str, int, int], list[str]]
    prepare_command: list[str] | None = None
    supported_benchmarks: list[str] | None = None
