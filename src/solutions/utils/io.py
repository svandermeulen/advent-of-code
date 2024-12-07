from pathlib import Path
from typing import Iterator


def read(path: Path) -> str:
    with open(path) as f:
        data = f.read()
    return data


def read_lines(path: Path) -> Iterator[str]:
    with open(path) as f:
        data = f.readlines()
    return (x.rstrip() for x in data)
