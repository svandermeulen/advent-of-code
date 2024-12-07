from typing import Iterable


def parse_puzzle_input(puzzle_input: Iterable[str]) -> list[list[int]]:

    reports = []
    for row in puzzle_input:
        reports.append(list(map(int, row.split(" "))))
    return reports


def is_it_safe(report: list[int]) -> bool:
    difference = [report[i] - report[i + 1] for i in range(len(report) - 1)]
    if max(map(abs, difference)) > 3:
        return False
    if all(v > 0 for v in difference) or all(v < 0 for v in difference):
        return True
    return False


def run(puzzle_input: Iterable[str]) -> int:

    parsed_input = parse_puzzle_input(puzzle_input)
    safe = 0
    for report in parsed_input:
        safe += int(is_it_safe(report))
    return safe
