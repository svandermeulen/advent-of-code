"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 21/12/2020
"""
import re
from copy import deepcopy

import numpy as np
import os

from solutions.config import Config
from solutions.year_2020.utils.file_manager import read_txt_file


def update_cube_state(state: np.ndarray, coord: tuple) -> int:
    x, y, z = coord

    neighbors = [
        [
            [
                (abs(i), abs(j), abs(k)) for k in range(z - 1, min(z + 2, state.shape[2]))
            ]
            for j in range(y - 1, min(y + 2, state.shape[1]))
        ]
        for i in range(x - 1, min(x + 2, state.shape[0]))
    ]
    neighbors = [group for subgroup in neighbors for group in subgroup]
    neighbors = [group for subgroup in neighbors for group in subgroup if group != coord]
    neighbors = list(set(neighbors))

    state_new = deepcopy(state)

    states_active = np.sum(state[tuple(np.moveaxis(np.array(neighbors), -1, 0))])
    if state_new[x, y, z] == 1 and states_active not in (2, 3):
        return 0
    elif state_new[x, y, z] == 0 and states_active == 3:
        return 1

    return state_new[x, y, z]


def simulate_cycles(state_initial: np.ndarray, n_cycles: int = 6) -> np.ndarray:
    assert 3 == len(state_initial.shape)
    state_final = deepcopy(state_initial)
    while state_initial.shape[2] < (n_cycles*2) + 3:
        state_expanded = expand_state(state=state_initial)
        x, y, z = state_expanded.shape

        state_final = deepcopy(state_expanded)
        for i in range(x):
            for j in range(y):
                for k in range(z):
                    state_final[i, j, k] = update_cube_state(state=state_expanded, coord=(i, j, k))

        # spaceviewer(state_final)
        return simulate_cycles(state_initial=state_final, n_cycles=n_cycles)

    return state_final


def parse_initial_state(path_file: str) -> np.ndarray:
    data = read_txt_file(path_file=path_file)
    data = [re.split("", line)[1:-1] for line in data]
    data = np.array(data)
    data = data.reshape([data.shape[0], data.shape[1], 1])
    data[data == "#"] = 1
    data[data == "."] = 0
    data.astype(int)

    data = expand_state(state=data)
    spaceviewer(data)
    return data


def expand_state(state: np.ndarray) -> np.ndarray:
    x_init, y_init, z_init = state.shape

    x = x_init + 2 if state.shape[2] != 1 else x_init
    y = y_init + 2 if state.shape[2] != 1 else y_init
    z = z_init + 2

    x_offset = (x - x_init) // 2
    y_offset = (y - y_init) // 2
    z_offset = (z - z_init) // 2 if state.shape[2] != 1 else 1
    state_expanded = np.zeros([x, y, z]).astype(int)

    state_expanded[x_offset:x - x_offset, y_offset:y - y_offset, z_offset:z - z_offset] = state
    return state_expanded


def spaceviewer(space: np.ndarray):  # Take a look at the current state of the system
    c = 0
    for z in np.rollaxis(space, axis=2):
        print(c)
        c += 1
        [print(y) for y in z]

    return True


def main():
    config = Config(day=17)

    # PART ONE

    # Test
    state_initial = parse_initial_state(path_file=os.path.join(config.path_data, 'initial_state_test.txt'))
    state_final = simulate_cycles(state_initial=state_initial, n_cycles=6)
    assert 112 == state_final.sum().sum()

    state_initial = parse_initial_state(path_file=os.path.join(config.path_data, 'initial_state.txt'))
    state_final = simulate_cycles(state_initial=state_initial, n_cycles=6)
    print(f"The number of active states upon 6 cycles equals: {state_final.sum().sum()}")

    return True


if __name__ == "__main__":
    main()
