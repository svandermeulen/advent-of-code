"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 10/12/2020
"""
import doctest
import numpy as np
import os

from math import prod

from solutions.config import Config
from solutions.year_2020.utils.file_manager import read_txt_file


COMBINATIONS = {
    2: 2,
    3: 4,
    4: 7,
    5: 12
}


def get_contiguous_equal_numbers(sequence: np.ndarray) -> list:
    """"
    DOCTEST
    >>> get_contiguous_equal_numbers(sequence=np.array([1, 1, 3, 3]))
    [[1, 1], [3, 3]]
    >>> get_contiguous_equal_numbers(sequence=np.array([1, 1, 3, 3, 3, 3, 1, 1, 3, 3, 3]))
    [[1, 1], [3, 3, 3, 3], [1, 1], [3, 3, 3]]
    """
    stretches = []
    stretch = []
    for i, d in enumerate(sequence):
        if i == 0:
            stretch.append(d)
        elif d == sequence[i - 1]:
            stretch.append(d)
        else:
            stretches.append(stretch)
            stretch = [d]

    stretches.append(stretch)

    return stretches


def compute_part_one(adapters: np.ndarray) -> int:
    """
    Compute the distribution of jolt differences between consecutive adapters and
    return the product of the count of each unique jolt difference.
    """

    joltage_differences = np.diff(adapters)
    diff_unique, diff_count = np.unique(joltage_differences, return_counts=True)

    return np.product(diff_count)


def read_adapter_data(path_file: str) -> np.ndarray:
    adapters = read_txt_file(path_file=path_file)
    adapters = np.array([int(val) for val in adapters])
    adapters = np.sort(adapters)
    adapters = np.insert(adapters, 0, 0)  # Add source joltage
    adapters = np.append(adapters, np.max(adapters) + 3)  # Add device joltage

    return adapters


def get_adapter_arrangements(adapters: np.ndarray) -> int:
    joltage_difference = np.diff(adapters)
    number_stretches = get_contiguous_equal_numbers(sequence=joltage_difference)
    number_stretches = [stretch for stretch in number_stretches if len(stretch) > 1 and set(stretch) == {1}]

    combination_counts = [COMBINATIONS[len(stretch)] for stretch in number_stretches]

    return prod(combination_counts)


def main():
    config = Config()

    # PART ONE

    # Test one
    path_data = os.path.join(config.path_data, "day_10", "adapter_list_test_one.txt")
    data_test_one = read_adapter_data(path_file=path_data)

    result = compute_part_one(adapters=data_test_one)
    assert 35 == result

    # Test two
    path_data = os.path.join(config.path_data, "day_10", "adapter_list_test_two.txt")
    data_test_two = read_adapter_data(path_file=path_data)

    result = compute_part_one(adapters=data_test_two)
    assert 220 == result

    path_data = os.path.join(config.path_data, "day_10", "adapter_list.txt")
    data = read_adapter_data(path_file=path_data)
    result = compute_part_one(adapters=data)
    print(f"The number of 1 and 3 joltage differences multiplied equals: {result}")
    assert 1876 == result

    # PART TWO

    # Test one
    n_arrangements = get_adapter_arrangements(adapters=data_test_one)
    assert 8 == n_arrangements

    # Test two
    n_arrangements = get_adapter_arrangements(adapters=data_test_two)
    assert 19208 == n_arrangements

    n_arrangements = get_adapter_arrangements(adapters=data)
    print(f"The number of possible adapter arrangements equals: {n_arrangements}")
    assert 14173478093824 == n_arrangements

    return True


if __name__ == "__main__":
    doctest.testmod()
    main()
