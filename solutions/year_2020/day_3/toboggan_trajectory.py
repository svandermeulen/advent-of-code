"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 03/12/2020
"""
import math
import numpy as np
import os

from solutions.config import Config


def expand_array(data: np.ndarray, slope: tuple) -> np.ndarray:
    """
    Expand data to account for the slope horizontally moving out of the width of the data
    """

    total_steps_down = int(np.ceil(data.shape[0] / slope[0]))
    total_steps_right = ((data.shape[0] - 1) * slope[1]) + 1  # -1 to account for the first row, +1 index start at 0
    total_steps_right = total_steps_right / (total_steps_down / data.shape[0])

    repetition_count = int(np.ceil(total_steps_right / len(data[0])))
    return np.tile(data, repetition_count)


def count_encountered_trees(tree_data: list, slope: tuple) -> int:
    tree_data = np.array([[(0 if char == "." else 1) for char in line] for line in tree_data])
    tree_data = expand_array(data=tree_data, slope=slope)

    tree_count = tree_data[0, 0] + sum(
        tree_data[
            range(slope[0], tree_data.shape[0], slope[0]),
            range(slope[1], int(np.ceil(slope[1] * tree_data.shape[0] / slope[0])), slope[1])
        ]
    )

    return int(tree_count)


def main():
    config = Config()
    path_test_file = os.path.join(config.path_data, "day_three", "tree_map_test.txt")

    slope = (1, 3)

    with open(path_test_file, "r") as f:
        data_test = [value.strip("\n") for value in f.readlines()]

    tree_count = count_encountered_trees(tree_data=data_test, slope=slope)

    assert tree_count == 7, f"The number of encountered trees in the test set != 7 but {tree_count}"

    path_file = os.path.join(config.path_data, "day_three", "tree_map.txt")
    with open(path_file, "r") as f:
        data = [value.strip("\n") for value in f.readlines()]

    # Part 1
    tree_count = count_encountered_trees(tree_data=data, slope=slope)
    print(f"The total number of encountered trees with slope {slope} are: {tree_count}")

    # Part 2
    slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
    tree_counts = []
    tree_counts_test_exp = [2, 7, 3, 4, 2]
    for slope, tree_count_exp in zip(slopes, tree_counts_test_exp):
        tree_count_test = count_encountered_trees(tree_data=data_test, slope=slope)
        assert tree_count_test == tree_count_exp, f"Tree count != expected tree count. " \
                                                  f"{tree_count_test} != {tree_count_exp}"

        tree_count = count_encountered_trees(tree_data=data, slope=slope)
        tree_counts.append(tree_count)
        print(f"The total number of encountered trees with slope {slope} are: {tree_count}")

    print(f"The product of all the tree counts is: {math.prod(tree_counts)}")
    return True


if __name__ == "__main__":
    main()
