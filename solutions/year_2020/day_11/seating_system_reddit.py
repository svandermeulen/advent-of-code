"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 14/12/2020
"""
import os

from solutions.config import Config


def count_occupied2(r, c, grid, deltas, rows, cols):
    count = 0
    for i, j in deltas:
        xi, xj = r + i, c + j
        while 0 <= xi < rows and 0 <= xj < cols:
            if grid[xi][xj] == '#':
                count += 1
                break
            elif grid[xi][xj] == 'L':
                break
            xi += i
            xj += j
    return count


def check_occupied2(lines, deltas, rows, cols, thresh=5):
    while True:
        valid = True
        temp_grid = [r.copy() for r in lines]
        for i, r in enumerate(temp_grid):
            for j, c in enumerate(r):
                count = count_occupied2(i, j, temp_grid, deltas, rows, cols)
                if c == 'L' and count == 0:
                    lines[i][j] = '#'
                elif c == '#' and count >= thresh:
                    lines[i][j] = 'L'
                valid &= (r[j] == lines[i][j])
        if valid:
            break
    ans = 0
    for i in range(rows):
        for j in range(cols):
            if lines[i][j] == '#':
                ans += 1

    return ans


def main():

    """
    Stolen from
    https://dev.to/qviper/advent-of-code-2020-python-solution-day-11-2lkj
    """

    config = Config()

    # PART ONE

    # Test one
    path_data = os.path.join(config.path_data, "day_11", "seating_system.txt")

    with open(path_data, "r") as fp:
        lines = [line.rstrip() for line in fp.readlines()]
        lines = [list(line) for line in lines]

    rows, cols = len(lines), len(lines[0])
    deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    occupancy = check_occupied2(lines, deltas=deltas, rows=rows, cols=cols)
    print(f"There are {occupancy} valid seats.")


if __name__ == "__main__":
    main()
