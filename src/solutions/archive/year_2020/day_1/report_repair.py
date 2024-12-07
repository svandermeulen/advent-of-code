"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 01/12/2020
"""
import math
import os

from itertools import combinations
from typing import List, Tuple

from solutions.config import Config


def multiply(sequence: tuple) -> int:
    return math.prod(sequence)


def get_2020_groups(lst: List[int], group_size: int = 2, group_sum: int = 2020) -> Tuple:
    for pair in combinations(lst, group_size):
        if sum(pair) == group_sum:
            yield pair
    return ()


def main():
    config = Config(day=1)
    path_file = os.path.join(config.path_data, "expense_report.txt")

    with open(path_file, "r") as f:
        data = [int(value.strip("\n")) for value in f.readlines()]

    for group_size in [2, 3]:
        group_2020 = next(get_2020_groups(lst=data, group_size=group_size))
        if group_2020:
            print(
                f"Multiplying the group of size {group_size} which sum equals to 2020 {group_2020} gives: "
                f"{multiply(group_2020)}"
            )

    return True


if __name__ == "__main__":
    main()
