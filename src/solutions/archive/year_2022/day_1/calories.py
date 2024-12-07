"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 01/12/2022
"""
import os
from typing import List

import numpy as np

from solutions.config import Config


def read_data(path: str) -> List:
    with open(path, "r") as f:
        data = [l.strip("\n") for l in f.readlines()]
    return data


def sum_calories(data: List) -> List[int]:
    data = ",".join(data)
    data = data.split(",,")
    data = [d.split(",") for d in data]
    data = [sum([int(val) for val in d]) for d in data]
    return data


def main():
    config = Config(year=2022, day=1)
    path_file = os.path.join(config.path_data, "calories.txt")
    data = read_data(path=path_file)

    # part 1
    calories_summed = sum_calories(data=data)
    best_elf_idx = np.argmax(calories_summed)
    print(f"The best elf is the one with id: {best_elf_idx}, who carries {calories_summed[best_elf_idx]} calories")

    # part 2
    top_three_calories = sorted(calories_summed)[-3:]
    print(f"The top 3 carry a total of {sum(top_three_calories)} calories")

    pass


if __name__ == "__main__":
    main()
