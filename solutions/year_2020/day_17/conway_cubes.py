"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 21/12/2020
"""
import itertools
import numpy as np
import os
import re

from copy import deepcopy
from solutions.config import Config
from solutions.year_2020.utils.file_manager import read_txt_file


def update_cube_state(state: np.ndarray, coordinates: tuple) -> int:
    coords_neighbors = itertools.product(
        *[list(range(c - 1, min(c + 2, state.shape[i]))) for i, c in enumerate(coordinates)])

    coords_neighbors = [n for n in coords_neighbors if not any([v < 0 for v in n]) and n != coordinates]

    states_active = np.sum(state[tuple(np.moveaxis(np.array(coords_neighbors), -1, 0))])
    if state[coordinates] == 1 and states_active not in (2, 3):
        return 0
    elif state[coordinates] == 0 and states_active == 3:
        return 1

    return state[coordinates]


def simulate_cycles(state_initial: np.ndarray, n_cycles: int = 6, dims: int = 3) -> np.ndarray:
    state_final = deepcopy(state_initial)
    while state_initial.shape[-1] < (n_cycles * 2) + 3:
        state_expanded = expand_state(state=state_initial, dims=dims)
        state_final = deepcopy(state_expanded)
        for coord in itertools.product(*[list(range(i)) for i in state_final.shape]):
            state_final[coord] = update_cube_state(state=state_expanded, coordinates=coord)

        return simulate_cycles(state_initial=state_final, n_cycles=n_cycles)

    return state_final


def parse_initial_state(path_file: str, dims: int = 3) -> np.ndarray:
    data = read_txt_file(path_file=path_file)
    data = [re.split("", line)[1:-1] for line in data]
    data = np.array(data)

    data_shape_new = [s for s in data.shape]
    data_shape_new = data_shape_new if len(data_shape_new) == dims else data_shape_new + [1] * (dims - len(data_shape_new))
    data = data.reshape(data_shape_new)
    data[data == "#"] = 1
    data[data == "."] = 0
    data = data.astype(int)
    data = expand_state(state=data)
    return data


def expand_state(state: np.ndarray, dims: int = 3) -> np.ndarray:
    coords_init = state.shape
    coords_expand = [c + 2 if c != 0 else c for c in coords_init]
    coords_expand_offset = [(c_exp - c_init) // 2 for c_exp, c_init in zip(coords_expand, coords_init)]

    state_expanded = np.zeros(coords_expand).astype(int)

    slicing = [slice(c_offset, c - c_offset) if c != 1 else slice(c_offset) for c_offset, c in zip(coords_expand_offset, coords_expand)]

    state_expanded[tuple(slicing)] = state
    return state_expanded


def main():
    config = Config(day=17)

    # PART ONE

    # Test
    state_initial = parse_initial_state(path_file=os.path.join(config.path_data, 'initial_state_test.txt'))
    state_final = simulate_cycles(state_initial=state_initial, n_cycles=6)
    assert 112 == state_final.sum().sum()

    # Real deal
    state_initial = parse_initial_state(path_file=os.path.join(config.path_data, 'initial_state.txt'))
    state_final = simulate_cycles(state_initial=state_initial, n_cycles=6)
    print(f"The number of active states upon 6 cycles equals: {state_final.sum().sum()}")
    assert 255 == state_final.sum().sum()

    # PART TWO

    # Test
    state_initial = parse_initial_state(path_file=os.path.join(config.path_data, 'initial_state_test.txt'), dims=4)
    state_final = simulate_cycles(state_initial=state_initial, n_cycles=6, dims=4)
    assert 848 == state_final.sum().sum()

    # Real deal
    state_initial = parse_initial_state(path_file=os.path.join(config.path_data, 'initial_state.txt'), dims=4)
    state_final = simulate_cycles(state_initial=state_initial, n_cycles=6, dims=4)
    print(f"PART TWO: The number of active states upon 6 cycles equals: {state_final.sum().sum()}")

    return True


if __name__ == "__main__":
    main()
