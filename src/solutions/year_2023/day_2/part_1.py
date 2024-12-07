import re
from enum import Enum
from typing import Iterable


class Color(Enum):
    Blue = "blue"
    Red = "red"
    Green = "green"


def parse_color_set(color_set: str) -> dict[Color, int]:
    return {Color(color.split(" ")[1]): int(color.split(" ")[0]) for color in color_set.split(", ")}


def extract_color_sets(line: str) -> tuple[dict[Color, int]]:
    sets = re.sub(pattern=r"Game\s+\d+:\s+", string=line, repl="")
    return tuple(parse_color_set(color_set=color_set) for color_set in sets.split("; "))


def extract_game_id(line: str) -> int:
    (game_id,) = re.findall(pattern=r"(?<=Game )\d+(?=:)", string=line)
    return int(game_id)


def run(puzzle_input: Iterable[str]) -> int:
    bag_content_test = {Color.Red: 12, Color.Green: 13, Color.Blue: 14}

    games_possible = []
    for line in puzzle_input:
        possible = True
        game_id = extract_game_id(line=line)
        color_sets = extract_color_sets(line=line)
        for color_set in color_sets:
            for color, number in color_set.items():
                if bag_content_test[color] < number:
                    possible = False
        if possible:
            games_possible.append(game_id)
    return sum(games_possible)
