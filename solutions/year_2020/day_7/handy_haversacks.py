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


def parse_rules(data: List[str]) -> dict:
    data = [re.split("contain|, ", rule) for rule in data]
    data = [[item.strip(" |.") for item in rule] for rule in data]
    data_dict = {rule[0]: rule[1:] for rule in data}

    return data_dict


def parse_bag(bag: str) -> (str, int):
    bag_count, = re.findall("^\d+", bag)
    bag_count = int(bag_count)
    bag_renamed = re.sub('^\d+\s+', "", bag)
    if bag_count < 2:
        bag_renamed += "s"
    return bag_renamed, bag_count


def find_gold_carrying_bags(data: dict, bag_type: str = "shiny gold bag", bags_gold: list = None) -> list:
    bags_gold = bags_gold if bags_gold is not None else []

    bags_containing_type = [key for key, lst in data.items() if any([bag_type in val for val in lst])]
    bags_containing_type = [bag for bag in bags_containing_type if bag not in bags_gold]
    if bags_containing_type:
        bags_gold.extend(bags_containing_type)
        for bag in bags_containing_type:
            bags_gold = find_gold_carrying_bags(data=data, bag_type=bag.rstrip("s"), bags_gold=bags_gold)

    return bags_gold


def unpack(rules: dict, inner_bags: str, bags_unpacked: list = None) -> list:
    bags_unpacked = bags_unpacked if bags_unpacked is not None else []

    for bag in inner_bags:

        if bag == "no other bags":
            return bags_unpacked
        bag, bag_count = parse_bag(bag=bag)

        if rules[bag] == ["no other bags"]:
            bags_unpacked.extend(bag_count * [bag])
            continue

        if bag in rules:
            for _ in range(bag_count):
                bags_unpacked.append(bag)
                bags_unpacked = unpack(rules=rules, inner_bags=rules[bag], bags_unpacked=bags_unpacked)

    return bags_unpacked


def main():
    config = Config()

    # PART ONE
    path_file = os.path.join(config.path_data, "day_7", "bag_color_rules_test.txt")
    data_test = read_txt_file(path_file=path_file)
    data_test_parsed = parse_rules(data=data_test)
    bags_carrying_shiny_gold = find_gold_carrying_bags(data=data_test_parsed, bag_type="shiny gold bag")
    n_bags_carrying_shiny_gold = len(bags_carrying_shiny_gold)
    assert 4 == n_bags_carrying_shiny_gold

    path_file = os.path.join(config.path_data, "day_7", "bag_color_rules.txt")
    data = read_txt_file(path_file=path_file)
    data_parsed = parse_rules(data=data)
    bags_carrying_shiny_gold = find_gold_carrying_bags(data=data_parsed)
    assert 128 == len(bags_carrying_shiny_gold)

    # PART TWO
    bags_unpacked = unpack(rules=data_test_parsed, inner_bags=data_test_parsed["shiny gold bags"])
    assert 32 == len(bags_unpacked)

    path_file = os.path.join(config.path_data, "day_7", "bag_color_rules_test_part_two.txt")
    data_test_two = read_txt_file(path_file=path_file)
    data_test_two_parsed = parse_rules(data=data_test_two)
    bags_unpacked = unpack(rules=data_test_two_parsed, inner_bags=data_test_two_parsed["shiny gold bags"])
    assert 126 == len(bags_unpacked)

    bags_unpacked = unpack(rules=data_parsed, inner_bags=data_parsed["shiny gold bags"])
    print(f"The total number of bags within a shiny gold bag equals: {len(bags_unpacked)}")
    assert 20189 == len(bags_unpacked)

    return True


if __name__ == "__main__":
    main()
