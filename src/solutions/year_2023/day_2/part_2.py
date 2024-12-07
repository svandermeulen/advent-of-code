import math
from typing import Iterable

from solutions.year_2023.day_2.part_1 import Color, extract_color_sets


def compute_power(color_sets: tuple[dict[Color, int]]) -> int:
    max_color_numbers = []
    for color in Color:
        max_color_numbers.append(max(color_set[color] for color_set in color_sets if color in color_set))
    return math.prod(max_color_numbers)


def run(puzzle_input: Iterable[str]):
    game_powers = []
    for line in puzzle_input:
        color_sets = extract_color_sets(line=line)
        power = compute_power(color_sets=color_sets)
        game_powers.append(power)
    return sum(game_powers)
