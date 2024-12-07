import math
import re
from typing import Iterable


def find_all_numbers(line: str) -> list[str]:
    return [val for sublist in [re.findall(string=line, pattern=r"\d+")] for val in sublist]


def find_number_positions(line: str) -> list[tuple[int, int]]:
    return [match.span() for match in re.finditer(string=line, pattern=r"\d+")]


def is_adjacent(number_pos: tuple[int, int], gear_pos: tuple[int, int], line: str) -> bool:
    return set(range(*gear_pos)).issubset(set(range(max(0, number_pos[0] - 1), min(len(line), number_pos[1] + 1))))


def run(puzzle_input: Iterable[str]):
    total = 0
    puzzle_input: list[str] = list(puzzle_input)
    for i, line in enumerate(puzzle_input):
        for match in re.finditer(string=line, pattern=r"\*"):
            gear_pos = match.span()
            line_top = puzzle_input[i - 1] if i > 0 else ""
            line_bottom = puzzle_input[min(len(puzzle_input), i + 1)]
            gear_lines = [line_top, line, line_bottom]
            numbers = [val for sublist in [find_all_numbers(line=line) for line in gear_lines] for val in sublist]
            number_positions = [val for sub in [find_number_positions(line=line) for line in gear_lines] for val in sub]
            numbers_adjacent = [
                numbers[n]
                for (n, number_pos) in enumerate(number_positions)
                if is_adjacent(number_pos=number_pos, gear_pos=gear_pos, line=line)
            ]
            if len(numbers_adjacent) == 2:
                total += math.prod(map(int, numbers_adjacent))
    return total
