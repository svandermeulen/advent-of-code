"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 16/12/2020
"""
import numpy as np

from collections import defaultdict

from solutions.year_2020.utils.profiler import profile


def take_turns(starting_number_list: list, turn_end: int) -> int:
    number_dict = defaultdict(list)

    for i, n in enumerate(starting_number_list):
        number_dict[n] = [i]

    turn = len(starting_number_list)
    last_number = starting_number_list[-1]
    while turn < turn_end:

        if len(number_dict[last_number]) < 2:
            last_number = 0
            number_dict[last_number].append(turn)
        elif len(number_dict[last_number]) >= 2:
            number_dict[last_number] = number_dict[last_number][-2:]
            last_number = (turn - number_dict[last_number][-2]) - (turn - number_dict[last_number][-1])
            number_dict[last_number].append(turn)
        else:
            raise ValueError("Unknown number")

        turn += 1

    return last_number


@profile
def play_game(numbers: str, turn_end: int) -> int:
    starting_number_list = [int(n) for n in numbers.split(",")]
    last_number = take_turns(starting_number_list=starting_number_list, turn_end=turn_end)

    print(f"The {turn_end}th number spoken is {last_number}")

    return last_number


def main():
    # PART ONE

    turn_end = 2020

    # Test
    test_input = "0,3,6"
    number_end = play_game(numbers=test_input, turn_end=turn_end)
    assert 436 == number_end

    test_input = "1,3,2"
    number_end = play_game(numbers=test_input, turn_end=turn_end)
    assert 1 == number_end

    test_input = "2,1,3"
    number_end = play_game(numbers=test_input, turn_end=turn_end)
    assert 10 == number_end

    # Real deal
    puzzle_input = "18,11,9,0,5,1"
    number_end = play_game(numbers=puzzle_input, turn_end=turn_end)
    assert 959 == number_end

    # PART TWO

    # Real deal
    turn_end = 30000000
    number_end = play_game(numbers=puzzle_input, turn_end=turn_end)
    assert 116590 == number_end

    return True


if __name__ == "__main__":
    main()
