"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 07/12/2020
"""

import os
import re
from typing import List

from solutions.config import Config
from solutions.year_2020.utils.file_manager import read_txt_file


def parse_data(data: List[str]) -> dict:

    data = [re.split("contain|, ", rule) for rule in data]
    data = [[item.strip(" |.") for item in rule] for rule in data]
    data_dict = {rule[0]: rule[1:] for rule in data}

    data_dict = unpack_bag_rules(rules=data_dict)

    return data_dict


def unpack_bag_rules(rules: dict, subrules: dict = None) -> dict:

    subrules = subrules if subrules is not None else rules

    for outermost, underlying in subrules.items():
        for bag in underlying:

            if isinstance(bag, dict):
                subrules[outermost].extend(unpack_bag_rules(rules=rules, subrules=bag))
                subrules[outermost].remove(bag_renamed)
                continue
            if bag == "no other bags":
                continue

            bag_count, = re.findall("^\d+", bag)
            bag_count = int(bag_count)
            bag_renamed = re.sub('^\d+\s+', "", bag)
            if bag_count < 2:
                bag_renamed += "s"
            if bag_renamed in rules.keys():
                subrules[outermost].remove(bag)
                if subrules != rules:
                    subrules[outermost] = {bag_renamed: bag_count * rules[bag_renamed]}
                else:
                    subrules[outermost].extend([{bag_renamed: bag_count * rules[bag_renamed]}])

    return subrules


def compute_part_one(data: list) -> int:

    rules = parse_data(data=data)

    return data


def main():

    config = Config()
    path_file = os.path.join(config.path_data, "day_7", "bag_color_rules_test.txt")
    data_test = read_txt_file(path_file=path_file)
    n_bags_carrying_shiny_gold = compute_part_one(data=data_test)
    assert 4 == n_bags_carrying_shiny_gold

    return True


if __name__ == "__main__":
    main()
