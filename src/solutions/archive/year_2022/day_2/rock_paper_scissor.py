"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 02/12/2022
"""
import os

from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict

from solutions.config import Config


@dataclass
class RPS(ABC):
    score = 0

    def __lt__(self, other) -> bool:
        pass

    def __gt__(self, other) -> bool:
        pass

    def __eq__(self, other) -> bool:
        pass


class Rock(RPS):
    score: int = 1

    def __lt__(self, other: RPS) -> bool:
        if isinstance(other, Paper):
            return True
        return False

    def __gt__(self, other: RPS) -> bool:
        if isinstance(other, Scissors):
            return True
        return False

    def __eq__(self, other: RPS) -> bool:
        if isinstance(other, Rock):
            return True
        return False


class Paper(RPS):
    score: int = 2

    def __lt__(self, other: RPS) -> bool:
        if isinstance(other, Scissors):
            return True
        return False

    def __gt__(self, other: RPS) -> bool:
        if isinstance(other, Rock):
            return True
        return False

    def __eq__(self, other: RPS) -> bool:
        if isinstance(other, Paper):
            return True
        return False


class Scissors(RPS):
    score: int = 3

    def __lt__(self, other: RPS) -> bool:
        if isinstance(other, Rock):
            return True
        return False

    def __gt__(self, other: RPS) -> bool:
        if isinstance(other, Paper):
            return True
        return False

    def __eq__(self, other: RPS) -> bool:
        if isinstance(other, Scissors):
            return True
        return False


CODE_MAPPING_PART_ONE: Dict[str, RPS] = {
    "A": Rock(),
    "B": Paper(),
    "C": Scissors(),
    "X": Rock(),
    "Y": Paper(),
    "Z": Scissors()
}


class Condition(Enum):
    X = "LOSS", 0
    Y = "DRAW", 3
    Z = "WIN", 6


def contest(player_one: RPS, player_two: RPS) -> int:
    if player_one == player_two:
        return 3
    if player_one < player_two:
        return 0
    return 6


def compute_score(player_one: RPS, player_two: RPS) -> int:
    return contest(player_one=player_one, player_two=player_two) + player_one.score


def find_shape(opponent: RPS, condition: Condition) -> RPS:
    for shape_condition in [Rock, Paper, Scissors]:
        if contest(player_one=shape_condition(), player_two=opponent) == condition.value[1]:
            return shape_condition()


def read_data(path: str) -> (List[str], List[str]):
    with open(path, "r") as f:
        data = [line.strip("\n") for line in f.readlines()]

    data = [d.split(" ") for d in data]
    opponent = [d[0] for d in data]
    you = [d[1] for d in data]

    return opponent, you


def main():
    config = Config(year=2022, day=2)
    path_file = os.path.join(config.path_data, "rock_paper_scissor.txt")
    opponent, you = read_data(path=path_file)

    # Part 1
    opponent = [CODE_MAPPING_PART_ONE[op] for op in opponent]
    you_p1 = [CODE_MAPPING_PART_ONE[y] for y in you]
    score_total = 0
    for o, y in zip(opponent, you_p1):
        score_total += compute_score(player_one=y, player_two=o)
    print(f"You scored a total points of: {score_total}")
    assert score_total == 15572, f"The calculated score: {score_total} != 15572"

    # Part 2
    you_p2 = [find_shape(opponent=o, condition=Condition[y]) for o, y in zip(opponent, you)]
    score_total = 0
    for o, y in zip(opponent, you_p2):
        score_total += compute_score(player_one=y, player_two=o)
    print(f"You scored a total points of: {score_total}")
    assert score_total == 16098, f"The calculated score: {score_total} != 16098"


if __name__ == "__main__":
    main()
