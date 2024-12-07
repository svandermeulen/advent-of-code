import re
from typing import Iterable


def find_surrounding_characters(
        puzzle_input: list[str], number_pos: tuple[int, int], line: str, line_number: int
) -> tuple[int, int, int, int]:
    left = max(0, number_pos[0] - 1)
    right = min(len(line), number_pos[1] + 1)
    up = max(0, line_number - 1)
    down = min(len(puzzle_input), line_number + 1)
    return left, right, up, down


def run(puzzle_input: Iterable[str]):
    total = 0
    puzzle_input: list[str] = list(puzzle_input)
    for i, line in enumerate(puzzle_input):
        for match in re.finditer(string=line, pattern=r"\d+"):
            number_pos = match.span()
            left, right, up, down = find_surrounding_characters(
                puzzle_input=puzzle_input, number_pos=number_pos, line=line, line_number=i
            )
            all_characters = "".join([puzzle_input[i][left:right] for i in range(up, min(len(puzzle_input), down + 1))])
            if any(re.findall(pattern=r"[^\d\.]", string=all_characters)):
                total += int(line[number_pos[0]: number_pos[1]])
    return total
