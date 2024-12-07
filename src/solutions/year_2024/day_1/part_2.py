from collections import Counter
from typing import Iterable

from solutions.year_2024.day_1.part_1 import parse_input


def run(puzzle_input: Iterable[str]):
    n1_list, n2_list = parse_input(puzzle_input)
    total = 0
    number_counts = Counter(n2_list)
    for n1 in n1_list:
        total += n1 * number_counts[n1]
    return total
