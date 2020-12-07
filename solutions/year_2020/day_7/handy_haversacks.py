"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 07/12/2020
"""

import os
import re
from copy import deepcopy
from typing import List

from solutions.config import Config
from solutions.year_2020.utils.file_manager import read_txt_file


def parse_data(data: List[str]) -> dict:

    data = [re.split("contain|, ", rule) for rule in data]
    data = [[item.strip(" |.") for item in rule] for rule in data]
    data_dict = {rule[0]: rule[1:] for rule in data}

    data_dict = unpack_bag_rules(rules=data_dict)

    return data_dict


def parse_bag(bag: str) -> (str, int):

    bag_count, = re.findall("^\d+", bag)
    bag_count = int(bag_count)
    bag_renamed = re.sub('^\d+\s+', "", bag)
    if bag_count < 2:
        bag_renamed += "s"
    return bag_renamed, bag_count


def unpack(rules: dict, outer_bag: str, inner_bags: str, bags_unpacked: list = None) -> list:

    bags_unpacked = bags_unpacked if bags_unpacked is not None else []

    if len(bags_unpacked) > 10000:
        return bags_unpacked

    for bag in inner_bags:

        if bag == "no other bags":
            return bags_unpacked

        bag, bag_count = parse_bag(bag=bag)

        if bag in bags_unpacked:
            continue

        if rules[bag] == ["no other bags"]:
            bags_unpacked.extend(bag_count * [bag])
            return bags_unpacked

        if bag in rules:
            for _ in range(bag_count):
                bags_unpacked.append(bag)
                bags_unpacked = unpack(rules=rules, outer_bag=bag, inner_bags=rules[bag], bags_unpacked=bags_unpacked)

                if "shiny gold bags" in bags_unpacked:
                    return bags_unpacked

    return bags_unpacked


def unpack_bag_rules(rules: dict) -> dict:

    rules_unpacked = deepcopy(rules)

    for outermost, underlying in rules.items():
        rules_unpacked[outermost] = unpack(rules=rules, outer_bag=outermost, inner_bags=underlying)

    return rules_unpacked


def compute_part_one(data: list) -> int:

    rules_unpacked = parse_data(data=data)

    bags_carrying_shiny_gold = [key for key, val in rules_unpacked.items() if "shiny gold bags" in val]

    return len(bags_carrying_shiny_gold)


def main():

    config = Config()
    path_file = os.path.join(config.path_data, "day_7", "bag_color_rules_test.txt")
    data_test = read_txt_file(path_file=path_file)
    n_bags_carrying_shiny_gold = compute_part_one(data=data_test)
    assert 4 == n_bags_carrying_shiny_gold

    path_file = os.path.join(config.path_data, "day_7", "bag_color_rules.txt")
    data = read_txt_file(path_file=path_file)
    n_bags_carrying_shiny_gold = compute_part_one(data=data)
    # assert 4 == n_bags_carrying_shiny_gold

    return True


if __name__ == "__main__":
    main()
