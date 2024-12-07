import re
from typing import Iterable


def parse_input(puzzle_input: Iterable[str]) -> (list[int], list[int]):
    n1_list, n2_list = [], []

    for row in puzzle_input:
        n1, n2 = re.split(r"\s+", row)
        n1_list.append(int(n1))
        n2_list.append(int(n2))

    return sorted(n1_list), sorted(n2_list)


def run(puzzle_input: Iterable[str]) -> int:
    parsed_input = parse_input(puzzle_input)

    return sum([abs(n1 - n2) for n1, n2 in zip(parsed_input[0], parsed_input[1])])
