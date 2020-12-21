"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 21/12/2020
"""

import itertools
import os
from copy import deepcopy

from solutions.config import Config


def spaceviewer(space):  # Take a look at the current state of the system
    c = 0
    for z in space:
        print(c)
        c += 1
        [print(y) for y in z]


def generate_plane(space):
    plane = space[0]
    empty = [['.' for i in range(len(plane[0]))] for j in range(len(plane))]
    space.insert(0, empty)
    space.append(empty)
    return space


def expand_space(space):
    space = generate_plane(space)
    space_ = deepcopy(space)
    empty = ['.' for i in range(len(space[0][0]) + 4)]
    for k in range(len(space) - 1):
        for j in range(len(space[k])):
            space_[k][j] = ['.', '.'] + space[k][j] + ['.', '.']
        space_[k].insert(0, deepcopy(empty))
        space_[k].insert(0, deepcopy(empty))
        space_[k].append(deepcopy(empty))
        space_[k].append(deepcopy(empty))
        # print(empty)
        # print(len(space_[k]))
    return space_


def search(i, j, k, space):
    # print('search',i,j,k)
    c = 0
    for k_ in range(k - 1, k + 2):
        for j_ in range(j - 1, j + 2):
            for i_ in range(i - 1, i + 2):
                if (k_ >= 0 and k_ < len(space) and j_ >= 0 and j_ < len(space[0]) and i_ >= 0 and i_ < len(
                        space[0][0])) and (k_ != k or j_ != j or i_ != i):
                    if space[k_][j_][i_] == '#':
                        c += 1
                    # c+=1
                    # print()
                    # print(c)
    return c


def update_state(c, space):
    space = expand_space(space)
    space_ = deepcopy(space)
    change = False
    for k in range(0, len(space_)):
        for j in range(0, len(space_[0])):
            for i in range(0, len(space_[0][0])):

                if i == 2 and j == 2 and k == 2:
                    print( 'up')

                adj = search(i, j, k, space)
                if space[k][j][i] == '#' and adj not in [2, 3]:
                    space_[k][j][i] = '.'
                    change = True
                elif space[k][j][i] == '.' and adj == 3:
                    space_[k][j][i] = '#'
                    change = True
    if change == True and c < 2:
        c += 1
        spaceviewer(space_)
        space_ = update_state(c, space_)
    return space_


def main():
    config = Config(day=17)
    path_input = os.path.join(config.path_data, "initial_state_test.txt")
    ic = [list(x) for x in open(path_input).read().splitlines()]
    space = generate_plane([ic])
    spaceviewer(space)

    space_ = update_state(0, space)

    return True


if __name__ == "__main__":
    main()
