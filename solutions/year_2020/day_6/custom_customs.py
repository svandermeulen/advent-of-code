"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 07/12/2020
"""
import os
from collections import Counter
from typing import List

from solutions.config import Config
from solutions.year_2020.utils.file_manager import read_txt_file


def split_group_data(data: list) -> List[List[str]]:
    data = ";".join(data)
    data = data.replace(";;", ";+;")
    data = data.split("+")
    return [line.strip(";").split(";") for line in data]


def join_group(group: List[str]) -> str:
    return "".join(group)


def get_unique_questions(group: List[str]) -> set:
    return set(join_group(group))


def compute_part_one(groups: List[List[str]]) -> int:

    counts_per_group = [*map(len, map(get_unique_questions, groups))]
    return sum(counts_per_group)


def compute_part_two(groups: List[List[str]]) -> int:

    total = 0
    for group in groups:
        group_size = len(group)
        answers = join_group(group=group)
        for answer, count in Counter(answers).items():
            if count == group_size:
                total += 1
    return total


def main():
    config = Config()

    path_file = os.path.join(config.path_data, "day_6", "custom_declaration_forms.txt")

    # PART ONE
    path_file_test = os.path.join(config.path_data, "day_6", "custom_declaration_forms_test.txt")
    data_test = read_txt_file(path_file=path_file_test)
    data_test_group = split_group_data(data=data_test)

    sum_of_counts = compute_part_one(groups=data_test_group)
    assert 11 == sum_of_counts, f"Script does not lead to the correct sum. 11 != {sum_of_counts}"

    data = read_txt_file(path_file=path_file)
    groups = split_group_data(data=data)
    sum_of_counts = compute_part_one(groups=groups)
    print(f"The sum of the counts of the unique questions to which a group answered yes equals: {sum_of_counts}")
    assert 6585 == sum_of_counts

    # PART TWO
    data_test_group = split_group_data(data=data_test)
    sum_of_counts = compute_part_two(groups=data_test_group)
    assert 6 == sum_of_counts, f"Script does not lead to the correct sum. 6 != {sum_of_counts}"

    groups = split_group_data(data=data)
    sum_of_counts = compute_part_two(groups=groups)
    print(f"The sum of the counts of the questions to which all group members answered yes: {sum_of_counts}")

    return True
    pass


if __name__ == "__main__":
    main()
