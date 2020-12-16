"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 16/12/2020
"""

import numpy as np
import matplotlib.pyplot as plt


from solutions.year_2020.utils.profiler import profile


def get_new_number(turn: int, last_number_occourences: np.ndarray):
    last_two_number_turns = turn - last_number_occourences[-2:]
    return np.subtract(*last_two_number_turns)


def take_turns(starting_number_list: list, turn_end: int) -> np.ndarray:

    numbers_spoken = np.ones(turn_end) * -1
    numbers_spoken[0:len(starting_number_list)] = starting_number_list
    turn = len(starting_number_list)
    while turn < turn_end:

        last_number = numbers_spoken[turn - 1]

        last_number_occourences = np.where(numbers_spoken == last_number)[0]
        if len(last_number_occourences) < 2:
            numbers_spoken[turn] = 0
        elif len(last_number_occourences) >= 2:
            numbers_spoken[turn] = get_new_number(turn=turn, last_number_occourences=last_number_occourences)
        else:
            raise ValueError("Last number has not been counted before.")

        turn += 1

    return numbers_spoken


def play_game(numbers: str, turn_end: int) -> int:

    starting_number_list = [int(n) for n in numbers.split(",")]
    numbers_spoken = take_turns(starting_number_list=starting_number_list, turn_end=turn_end)
    print(f"The {turn_end}th number spoken is {numbers_spoken[-1]}")

    plot_number_sequence(number_seq=numbers_spoken)

    return numbers_spoken[-1]


def plot_number_sequence(number_seq: np.ndarray) -> bool:

    plt.plot(number_seq)
    plt.plot(range(0, len(number_seq)), "-r")
    plt.show()

    derivative = np.diff(number_seq)
    plt.plot(derivative)
    plt.show()

    return True


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
    puzzle_input = "3,2,1"
    turn_end = 100
    number_end = play_game(numbers=puzzle_input, turn_end=turn_end)

    turn_end = 1000
    number_end = play_game(numbers=puzzle_input, turn_end=turn_end)

    turn_end = 10000
    number_end = play_game(numbers=puzzle_input, turn_end=turn_end)

    turn_end = 100000
    number_end = play_game(numbers=puzzle_input, turn_end=turn_end)

    turn_end = 1000000
    number_end = play_game(numbers=puzzle_input, turn_end=turn_end)

    return True


if __name__ == "__main__":
    main()
