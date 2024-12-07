from typing import Iterable

from solutions.year_2024.day_2.part_1 import parse_puzzle_input, is_it_safe


def run(puzzle_input: Iterable[str]) -> int:

    reports = parse_puzzle_input(puzzle_input)
    n_safe = 0
    for report in reports:
        safe = is_it_safe(report)
        if safe:
            n_safe += 1
        if not safe:
            for i in range(len(report)):
                report_dampened = [v for j, v in enumerate(report) if j != i]
                safe = is_it_safe(report_dampened)
                if safe:
                    n_safe += 1
                    break
    return n_safe

