"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 14/12/2020
"""
import doctest
import math
import os

from solutions.config import Config
from solutions.year_2020.utils.file_manager import read_txt_file

COMPASS = {
    0: "N",
    90: "E",
    180: "S",
    270: "W"
}


def change_direction(direction: str, degrees: int) -> str:
    """
    DOCTEST
    >>> change_direction(direction="S", degrees=90)
    'W'
    >>> change_direction(direction="S", degrees=-90)
    'E'
    """
    direction, = [key for key, value in COMPASS.items() if value == direction]

    direction_degrees = (direction + degrees) % 360
    assert direction_degrees in COMPASS
    return COMPASS[direction_degrees]


def action_decoder_one(location: list, direction: str, action: str, value: int) -> (list, str):
    if action[0] == "N":
        location[1] -= value
    elif action[0] == "S":
        location[1] += value
    elif action[0] == "E":
        location[0] += value
    elif action[0] == "W":
        location[0] -= value
    elif action[0] == "R":
        direction = change_direction(direction=direction, degrees=value)
    elif action[0] == 'L':
        direction = change_direction(direction=direction, degrees=-1 * value)
    else:
        raise ValueError

    return location, direction


def execute_actions(actions: list, location_init: list, direction_init: str) -> list:
    location = location_init
    direction = direction_init
    for action in actions:
        action, value = action[0], action[1]
        if action == "F":
            action = direction

        location, direction = action_decoder_one(
            location=location,
            direction=direction,
            action=action,
            value=value
        )

    return location


def rotate_waypoint(waypoint: list, degrees: int) -> list:
    """
    DOCTEST
    >>> rotate_waypoint(waypoint=[10, 4], degrees=90)
    [4, -10]
    >>> rotate_waypoint(waypoint=[10, 4], degrees=180)
    [-10, -4]
    >>> rotate_waypoint(waypoint=[10, 4], degrees=270)
    [-4, 10]

    """
    if degrees == 90 or degrees == -270:
        waypoint[0] = waypoint[0] * -1
        return [*reversed(waypoint)]
    elif abs(degrees) == 180:
        waypoint = [p * -1 for p in waypoint]
        return waypoint
    elif degrees == 270 or degrees == -90:
        waypoint[1] = waypoint[1] * -1
        return [*reversed(waypoint)]
    else:
        raise ValueError


def action_decoder_two(waypoint: list, action: str, value: int) -> list:
    if action[0] == "N":
        waypoint[1] += value
    elif action[0] == "S":
        waypoint[1] -= value
    elif action[0] == "E":
        waypoint[0] += value
    elif action[0] == "W":
        waypoint[0] -= value
    elif action[0] == "R":
        waypoint = rotate_waypoint(waypoint=waypoint, degrees=value)
    elif action[0] == 'L':
        waypoint = rotate_waypoint(waypoint=waypoint, degrees=-1 * value)
    else:
        raise ValueError

    return waypoint


def execute_actions_two(actions: list, location_init: list, waypoint_init: list) -> list:
    location = location_init
    waypoint = waypoint_init
    for action in actions:
        action, value = action[0], action[1]
        if action == "F":
            location = [i + (value * j) for i, j in zip(location, waypoint)]
        else:
            waypoint = action_decoder_two(waypoint=waypoint, action=action, value=value)

    return location


def parse_puzzle_input(path_data: str) -> list:
    data = read_txt_file(path_data)
    return [[l[0], int(l[1:])] for l in data]


def get_manhattan_distance(location: list) -> int:
    return sum([abs(l) for l in location])


def main():
    config = Config()

    # PART ONE

    # Test one
    path_data = os.path.join(config.path_data, "day_12", "evasive_actions_test.txt")
    evasive_actions_test = parse_puzzle_input(path_data=path_data)
    coordinate_final = execute_actions(actions=evasive_actions_test, location_init=[0, 0], direction_init="E")
    manhattan_distance = get_manhattan_distance(location=coordinate_final)
    assert 25 == manhattan_distance

    # Real deal
    path_data = os.path.join(config.path_data, "day_12", "evasive_actions.txt")
    evasive_actions = parse_puzzle_input(path_data=path_data)
    coordinate_final = execute_actions(actions=evasive_actions, location_init=[0, 0], direction_init="E")
    manhattan_distance = get_manhattan_distance(location=coordinate_final)
    print(f"The manhattan distance of the final coordinate equals: {manhattan_distance}")
    assert 2280 == manhattan_distance

    # PART TWO

    # Test
    coordinate_final = execute_actions_two(actions=evasive_actions_test, location_init=[0, 0], waypoint_init=[10, 1])
    manhattan_distance = get_manhattan_distance(location=coordinate_final)
    assert manhattan_distance == 286

    coordinate_final = execute_actions_two(actions=evasive_actions, location_init=[0, 0], waypoint_init=[10, 1])
    manhattan_distance = get_manhattan_distance(location=coordinate_final)
    print(f"The manhattan distance of the final coordinate equals: {manhattan_distance}")
    assert 38693 == manhattan_distance
    return True


if __name__ == "__main__":
    doctest.testmod()
    main()
