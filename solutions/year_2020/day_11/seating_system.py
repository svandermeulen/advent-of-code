"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 11/12/2020
"""
import numpy as np
import os
import scipy.ndimage as ndimage

from collections import Counter
from typing import List

from solutions.config import Config
from solutions.year_2020.utils.file_manager import read_txt_file

SEAT_TYPE = {
    ".": "floor",
    "#": "occupied",
    "L": "empty"
}


def get_adjacent_seats(seat_plan: np.ndarray, rowidx: int, colidx: int, dist: int = 1) -> np.ndarray:
    rowmax, colmax = np.subtract(seat_plan.shape, 1)

    row_ub = min(rowidx + dist, rowmax)
    col_ub = min(colidx + dist, colmax)

    row_lb = max(0, rowidx - dist)
    col_lb = max(0, colidx - dist)

    coordinates = np.array(
        list(
            {
                (row_lb, col_lb),
                (rowidx, col_lb),
                (row_ub, col_lb),
                (row_lb, colidx),
                (row_ub, colidx),
                (row_lb, col_ub),
                (rowidx, col_ub),
                (row_ub, col_ub)
            }
        )
    )

    coordinates = np.array(
        [coordinate for coordinate in coordinates if not np.array_equal(coordinate, np.array([rowidx, colidx]))]
    )
    seats_adjacent_states = np.array([seat_plan[coordinate[0], coordinate[1]] for coordinate in coordinates])
    return seats_adjacent_states

    # seats_adjacent_states = seat_plan[row_lb:row_ub + 1, col_lb:col_ub + 1].flatten()
    # seats_adjacent_states = np.delete(seats_adjacent_states,
    #                                   np.where(seats_adjacent_states == seat_plan[rowidx, colidx])[0][0])
    # return seats_adjacent_states


def fill_seats(seat_plan: np.ndarray) -> np.ndarray:
    seat_plan_new = seat_plan.copy()
    for rowidx, row in enumerate(seat_plan):
        for colidx, col in enumerate(row):

            seats_adjacent = get_adjacent_seats(seat_plan=seat_plan, rowidx=rowidx, colidx=colidx)

            if col == ".":
                continue
            elif col == "L":
                if Counter(seats_adjacent)["#"] == 0:
                    seat_plan_new[rowidx, colidx] = "#"
            else:
                if Counter(seats_adjacent)["#"] >= 4:
                    seat_plan_new[rowidx, colidx] = "L"
    if not np.array_equal(seat_plan, seat_plan_new):
        return fill_seats(seat_plan=seat_plan_new)

    return seat_plan_new


def get_first_visible_seat_state(seats: list) -> str:
    for seat in seats:
        if seat in "#L":
            return seat
    return "."


def get_visible_occupied_seats(seat_plan: np.ndarray, rowidx: int, colidx: int) -> int:
    rowmax, colmax = seat_plan.shape

    directions = {
        "left": [*zip([rowidx] * (colidx + 1), range(colidx - 1, -1, -1))],
        "right": [*zip([rowidx] * (colmax - colidx), range(colidx + 1, colmax))],
        "up": [*zip(range(colidx, -1, -1), [colidx] * rowidx)],
        "down": [*zip(range(rowidx + 1, rowmax), [colidx] * (rowmax - rowidx))],
        "diagonal_right_up": [*zip(range(rowidx - 1, -1, -1), range(colidx + 1, colmax))],
        "diagonal_right_down": [*zip(range(rowidx + 1, rowmax), range(colidx + 1, colmax))],
        "diagonal_left_up": [*zip(range(rowidx - 1, -1, -1), range(colidx - 1, -1, -1))],
        "diagonal_left_down": [*zip(range(rowidx + 1, rowmax), range(colidx - 1, -1, -1))]
    }

    seats_taken = 0
    for direction, coordinates in directions.items():
        if coordinates:
            try:
                seats_visible = [seat_plan[coordinate] for coordinate in coordinates if seat_plan[coordinate]]
            except IndexError:
                print("Help")
            first_seat_visible = get_first_visible_seat_state(seats=seats_visible)
            if first_seat_visible == "#":
                seats_taken += 1

    return seats_taken


def fill_seats_two(seat_plan: np.ndarray) -> np.ndarray:
    seat_plan_new = seat_plan.copy()
    for rowidx, row in enumerate(seat_plan):
        for colidx, col in enumerate(row):
            seats_taken = get_visible_occupied_seats(seat_plan=seat_plan, rowidx=rowidx, colidx=colidx)
            if col == ".":
                continue
            elif col == "L":
                if seats_taken == 0:
                    seat_plan_new[rowidx, colidx] = "#"
            elif col == "#":
                if seats_taken >= 5:
                    seat_plan_new[rowidx, colidx] = "L"
            else:
                raise ValueError

    if not np.array_equal(seat_plan, seat_plan_new):
        return fill_seats_two(seat_plan=seat_plan_new)

    return seat_plan_new


def parse_seat_system(path_file: str) -> np.ndarray:
    seat_system = read_txt_file(path_file=path_file)
    return np.array([[val for val in row] for row in seat_system])


def get_state_counts(seat_system: np.ndarray) -> dict:
    states, state_count = np.unique(seat_system, return_counts=True)

    return {s: c for s, c in zip(states, state_count)}


def main():
    config = Config()

    # PART ONE

    # Test one
    path_data = os.path.join(config.path_data, "day_11", "seating_system_test.txt")
    seat_system_test_one = parse_seat_system(path_file=path_data)

    path_data = os.path.join(config.path_data, "day_11", "seating_system_test_exp.txt")
    seat_system_exp = parse_seat_system(path_file=path_data)
    seat_system_new = fill_seats(seat_plan=seat_system_test_one)
    assert np.array_equal(seat_system_exp, seat_system_new)

    state_count = get_state_counts(seat_system=seat_system_new)
    assert state_count["#"] == 37

    path_data = os.path.join(config.path_data, "day_11", "seating_system.txt")
    seat_system = parse_seat_system(path_file=path_data)
    # seat_system = fill_seats(seat_plan=seat_system)
    # state_count = get_state_counts(seat_system=seat_system)
    #
    # print(f"Number of occupied seats equals: {state_count['#']}")
    # assert state_count["#"] == 2275

    # Test get visible seats
    path_data = os.path.join(config.path_data, "day_11", "seating_system_test_two.txt")
    seat_system_test_two = parse_seat_system(path_file=path_data)
    seats_occupied = get_visible_occupied_seats(seat_plan=seat_system_test_two, colidx=3, rowidx=4)
    assert seats_occupied == 8

    path_data = os.path.join(config.path_data, "day_11", "seating_system_test_three.txt")
    seat_system_test_three = parse_seat_system(path_file=path_data)
    seats_occupied = get_visible_occupied_seats(seat_plan=seat_system_test_three, colidx=1, rowidx=1)
    assert seats_occupied == 0

    path_data = os.path.join(config.path_data, "day_11", "seating_system_test_four.txt")
    seat_system_test_four = parse_seat_system(path_file=path_data)
    seats_occupied = get_visible_occupied_seats(seat_plan=seat_system_test_four, colidx=3, rowidx=3)
    assert seats_occupied == 0

    # Test fill_seats_two
    seat_system_new = fill_seats_two(seat_plan=seat_system_test_one)
    state_count = get_state_counts(seat_system=seat_system_new)
    assert state_count["#"] == 26

    # Real deal
    seat_system_new = fill_seats_two(seat_plan=seat_system)
    state_count = get_state_counts(seat_system=seat_system_new)
    print(f"The number of occupied seats equals: {state_count['#']}")

    return True


if __name__ == "__main__":
    main()
