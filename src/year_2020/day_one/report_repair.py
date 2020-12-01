"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 01/12/2020
"""
import math
import os

from itertools import combinations
from typing import List, Tuple

from src.year_2020.config import Config


def multiply(sequence: tuple) -> int:
    return math.prod(sequence)


def get_2020_groups(lst: List[int], group_size: int = 2) -> Tuple:
    for pair in combinations(lst, group_size):
        if sum(pair) == 2020:
            yield pair
    return ()


def main():
    config = Config()
    path_file = os.path.join(config.path_data, "day_one", "expense_report.txt")

    with open(path_file, "r") as f:
        data = [int(value.strip("\n")) for value in f.readlines()]

    pair_2020 = next(get_2020_groups(lst=data))
    print(f"Multiplying the pair which sum equals to 2020 {pair_2020} gives: {multiply(pair_2020)}")

    triplet_2020 = next(get_2020_groups(lst=data, group_size=3))
    print(f"Multiplying the triplet which sum equals to 2020 {triplet_2020} gives: {multiply(triplet_2020)}")

    return True


if __name__ == "__main__":
    main()
