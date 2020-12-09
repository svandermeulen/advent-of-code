"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 09/12/2020
"""
import doctest
import os

from itertools import combinations

from solutions.config import Config
from solutions.year_2020.utils.file_manager import read_txt_file


def detect_encoding_error(sequence: list, preamble: int) -> int:

    for i, digit in zip(range(preamble, len(sequence)), sequence[preamble:]):
        previous_numbers = sequence[i - preamble:i]
        possible_sums = [sum(pair) for pair in combinations(previous_numbers, 2)]
        if digit not in possible_sums:
            return digit

    return -1


def get_contiguous_pairs(sequence: list, pair_size: int) -> list:

    """"
    DOCTEST
    >>> get_contiguous_pairs(sequence=[1, 2, 3, 4], pair_size=2)
    [[1, 2], [2, 3], [3, 4]]
    >>> get_contiguous_pairs(sequence=[1, 2, 3, 4], pair_size=3)
    [[1, 2, 3], [2, 3, 4]]
    """

    return [sequence[i:i+pair_size] for i in range(len(sequence) - (pair_size - 1))]


def detect_encrption_weakness(sequence: list, encoding_error: int) -> int:

    idx_encoding_error, = [i for i, value in enumerate(sequence) if value == encoding_error]
    for pair_size in range(2, idx_encoding_error):
        for pair in get_contiguous_pairs(sequence=sequence, pair_size=pair_size):
            if encoding_error == sum(pair):
                return min(pair) + max(pair)

    return -1


def main():

    config = Config()

    # PART ONE

    # Test
    path_data = os.path.join(config.path_data, "day_9", "xmas_test.txt")
    data_test = read_txt_file(path_file=path_data)
    data_test = [int(val) for val in data_test]
    encoding_error_test = detect_encoding_error(sequence=data_test, preamble=5)
    assert 127 == encoding_error_test

    path_data = os.path.join(config.path_data, "day_9", "xmas.txt")
    data = read_txt_file(path_file=path_data)
    data = [int(val) for val in data]
    encoding_error = detect_encoding_error(sequence=data, preamble=25)
    assert 167829540 == encoding_error
    print(f"The first digit which does not abide to XMAX encoding is: {encoding_error}")

    # PART TWO

    # Test
    encoding_weakness_test = detect_encrption_weakness(sequence=data_test, encoding_error=encoding_error_test)
    assert 62 == encoding_weakness_test

    encoding_weakness = detect_encrption_weakness(sequence=data, encoding_error=encoding_error)
    print(
        f"The sum of the min and max of the contiguous sequence of numbers, "
        f"which sum equals the encoding error equals: {encoding_weakness}"
    )
    assert 28045630 == encoding_weakness

    return True


if __name__ == "__main__":
    doctest.testmod()
    main()
