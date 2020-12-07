"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 07/12/2020
"""
import math
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

    # data_dict = unpack_bag_rules(rules=data_dict)

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


def count_bags_in_gold_bag(data: dict, bag_type: str = "shiny gold bags", bags_count: list = None) -> list:
    bags_count = bags_count if bags_count is not None else []

    bags_type = data[bag_type]
    for bag in bags_type:

        if bag == "no other bags":
            return bags_count

        bag, bag_count = parse_bag(bag=bag)

        if data[bag] == ["no other bags"]:
            bags_count.append(f"+{bag_count}")
        else:
            bags_count.append(str(bag_count))
        bags_count = count_bags_in_gold_bag(data=data, bag_type=bag, bags_count=bags_count)

    return bags_count


def parse_bag_counts(bag_counts: List[str]) -> str:

    calculation = ""
    summation_count = 0
    for bag_count in bag_counts:
        if "+" not in bag_count and summation_count == 0 and not calculation:
            calculation += bag_count + "+" + bag_count
            summation_count = 0
        elif "+" not in bag_count and summation_count == 0 and calculation:
            calculation += "*" + bag_count + "+" + bag_count

        elif "+" in bag_count and summation_count != 0:
            calculation += bag_count
        elif "+" not in bag_count and summation_count > 0:
            calculation += ")+" + bag_count + "+" + bag_count
            summation_count = 0
        else:
            calculation += "*(" + bag_count.lstrip("+")
            summation_count += 1

    return calculation.strip("+") + ")"


def main():

    config = Config()

    # PART ONE
    path_file = os.path.join(config.path_data, "day_7", "bag_color_rules_test.txt")
    data_test = read_txt_file(path_file=path_file)
    data_test_parsed = parse_data(data=data_test)
    bags_carrying_shiny_gold = find_gold_carrying_bags(data=data_test_parsed, bag_type="shiny gold bag")
    n_bags_carrying_shiny_gold = len(bags_carrying_shiny_gold)
    assert 4 == n_bags_carrying_shiny_gold

    path_file = os.path.join(config.path_data, "day_7", "bag_color_rules.txt")
    data = read_txt_file(path_file=path_file)
    data_parsed = parse_data(data=data)
    bags_carrying_shiny_gold = find_gold_carrying_bags(data=data_parsed)
    assert 128 == len(bags_carrying_shiny_gold)

    # PART TWO
    bag_counts = count_bags_in_gold_bag(data=data_test_parsed)
    bag_counts_parsed = parse_bag_counts(bag_counts=bag_counts)
    total_bags = eval(bag_counts_parsed)
    assert 32 == total_bags

    path_file = os.path.join(config.path_data, "day_7", "bag_color_rules_test_part_two.txt")
    data = read_txt_file(path_file=path_file)
    data_parsed = parse_data(data=data)
    bag_counts = count_bags_in_gold_bag(data=data_parsed)
    bag_counts_parsed = parse_bag_counts(bag_counts=bag_counts)
    total_bags = eval(bag_counts_parsed)
    assert 126 == total_bags

    print(f"The total number of bags within a shiny gold bag equals: {total_bags}")

    return True


if __name__ == "__main__":
    main()
