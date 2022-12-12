"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 04/12/2022
"""
import os
from typing import List

from solutions.config import Config


def read_data(path: str) -> List[List[range]]:
    with open(path, "r") as f:
        data = [line.strip("\n").split(",") for line in f.readlines()]
    data = [[line[0].split("-"), line[1].split("-")] for line in data]
    data = [[range(int(l[0][0]), int(l[0][1]) + 1), range(int(l[1][0]), int(l[1][1]) + 1)] for l in data]
    return data


def main():
    config = Config(year=2022, day=4)
    path_file = os.path.join(config.path_data, "cleaning_pairs.txt")
    data = read_data(path=path_file)

    # Part 1
    overlapping_pairs = 0
    for pair in data:
        if set(pair[0]).issubset(set(pair[1])):
            overlapping_pairs += 1
        elif set(pair[1]).issubset(set(pair[0])):
            overlapping_pairs += 1

    print(f"The total number pairs to fully contain the other: {overlapping_pairs}")
    assert overlapping_pairs == 431

    # Part 2
    overlapping_pairs = 0
    for pair in data:
        if set(pair[0]).intersection(set(pair[1])):
            overlapping_pairs += 1

    print(f"The total number pairs that (partly) overlap: {overlapping_pairs}")
    # assert overlapping_pairs == 431
    return


if __name__ == "__main__":
    main()
