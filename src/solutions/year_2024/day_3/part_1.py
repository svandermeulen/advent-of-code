import math
import re
from typing import Iterable, Callable, Protocol

from pydantic import BaseModel, Field, field_validator, computed_field


class Multiplication(BaseModel):
    multiplication_string: str = Field(
        title="Multiplication String",
        description="The string expression of a mutliplication",
    )

    @field_validator("multiplication_string")
    @classmethod
    def validate_multiplication_string(cls, value: str) -> str:
        if not value.startswith("mul("):
            raise ValueError(f"{value} is not a valid multiplication string. Should start with 'mul('")
        if not value.endswith(")"):
            raise ValueError(f"{value} is not a valid multiplication string. Should end with ')'")
        if not bool(re.search("\d+,\d+", value)):
            raise ValueError(f"{value} is not a valid multiplication string. Should contain 2 comma separate digits.")
        return value

    @computed_field
    @property
    def digits(self) -> list[int]:
        digits = re.findall(r"\d+", self.multiplication_string)
        if not len(digits) == 2:
            raise ValueError(
                f"Invalid number of digits: {digits}. "
                f"The multiplication string must contain exactly 2 digits."
            )
        return list(map(int, digits))

    @computed_field
    @property
    def product(self) -> int:
        return math.prod(self.digits)


def execute_multiplication(multiplication: str) -> int:
    multiplication_string = Multiplication(multiplication_string=multiplication)
    return multiplication_string.product


def find_multiplications(line: str) -> list[str]:
    multiplications = re.findall(r"mul\(\d+,\d+\)", line)
    return multiplications


class FindPatternFunc(Protocol):

    def __call__(self, line: str) -> list[str]:
        pass


def parse_puzzle_input(puzzle_input: Iterable[str], find_pattern: FindPatternFunc) -> list[str]:
    multiplications = []
    for line in puzzle_input:
        multiplications.extend(find_pattern(line=line))
    return multiplications


def run(puzzle_input: Iterable[str]) -> int:
    multiplications = parse_puzzle_input(puzzle_input, find_pattern=find_multiplications)
    return sum(
        execute_multiplication(multiplication) for multiplication in multiplications
    )
