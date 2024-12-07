"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 04/12/2022
"""
import os
import string

from typing import List, Set

from solutions.config import Config


def read_data(path: str) -> List[str]:
    with open(path, "r") as f:
        data = [line.strip("\n") for line in f.readlines()]

    return data


def get_overlapping_items(data: List[str]) -> List[Set[str]]:
    overlapping_items = []
    for st in data:
        compartement_one, compartement_two = st[:len(st) // 2], st[len(st) // 2:]
        overlapping_items.append(set(compartement_one).intersection(set(compartement_two)))

    return overlapping_items


def main():
    config = Config(year=2022, day=3)
    path_file = os.path.join(config.path_data, "rucksacks.txt")
    data = read_data(path=path_file)
    priorities = {char: i + 1 for i, char in enumerate(string.ascii_lowercase + string.ascii_uppercase)}

    # Part 1
    overlapping_items = get_overlapping_items(data=data)
    total_score = 0
    for line in overlapping_items:
        total_score += sum(priorities[i] for i in line)
    print(f"Total error score: {total_score}")
    assert total_score == 8252

    # Part 2
    total_score = 0
    for i in range(0, len(data), 3):
        group = data[i:i + 3]
        overlapping_item, = set(group[0]).intersection(set(group[1])).intersection(set(group[2]))
        total_score += priorities[overlapping_item[0]]
    print(f"Total badge score: {total_score}")
    assert total_score == 2828

    return


if __name__ == "__main__":
    main()
