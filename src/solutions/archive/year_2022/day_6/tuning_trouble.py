"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 06/12/2022
"""
import os

from solutions.config import Config
from solutions.utils.file_manager import read_txt_file


def find_marker(datastream: str, delta: int = 4) -> int:
    for i in range(delta, len(datastream)):
        if len(set(datastream[i - delta:i])) == delta:
            return i


def main():
    config = Config(year=2022, day=6)

    # Test case
    path_file = os.path.join(config.path_data, "tuning_trouble.txt")
    data = read_txt_file(path_file=path_file)
    data = data[0]

    print(f"The length of the input string: {len(data)}")
    marker = find_marker(datastream="mjqjpqmgbljsphdztnvjfqwrcgsmlb")
    assert marker == 7

    marker = find_marker(datastream="bvwbjplbgvbhsrlpgdmjqwftvncz")
    assert marker == 5

    marker = find_marker(datastream="nppdvjthqldpwncqszvftbrmjlhg")
    assert marker == 6

    marker = find_marker(datastream="nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg")
    assert marker == 10

    marker = find_marker(datastream="zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")
    assert marker == 11

    # Part 1
    marker = find_marker(datastream=data)
    print(f"The marker of the puzzel input is: {marker}")
    assert marker == 1623

    # Part 2
    marker = find_marker(datastream="mjqjpqmgbljsphdztnvjfqwrcgsmlb", delta=14)
    assert marker == 19

    marker = find_marker(datastream="nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", delta=14)
    assert marker == 29

    marker = find_marker(datastream=data, delta=14)
    print(f"The start-of-message marker of the puzzel input is: {marker}")
    # assert marker == 1623


if __name__ == "__main__":
    main()
