import re
from typing import Iterable

from solutions.year_2024.day_3.part_1 import parse_puzzle_input, Multiplication


def find_multiplications_and_enabling_instructions(line: str) -> list[str]:
    results = re.findall(r"mul\(\d+,\d+\)|don't\(\)|do\(\)", line)
    return results


def find_enabled_multiplications(instructions: list[str]) -> list[Multiplication]:
    enabled_multiplications: list[Multiplication] = []
    disabled: bool = False
    for instruction in instructions:
        if instruction == "do()":
            disabled = False
        if instruction == "don't()":
            disabled = True
        if instruction.startswith("mul"):
            if disabled:
                continue
            enabled_multiplications.append(Multiplication(multiplication_string=instruction))
    return enabled_multiplications

def run(puzzle_input: Iterable[str]) -> int:
    parsed_input = parse_puzzle_input(puzzle_input, find_pattern=find_multiplications_and_enabling_instructions)
    enabled_multiplications = find_enabled_multiplications(parsed_input)
    return sum(
        multiplication.product for multiplication in enabled_multiplications
    )

