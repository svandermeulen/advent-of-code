"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 05/12/2022
"""
import os
from copy import deepcopy
from typing import List, Dict

from solutions.config import Config
from solutions.utils.file_manager import read_txt_file

EMPTY_CRATE = "[0]"


def process_cargo_string(cargo_str: str, default_str: str) -> str:

    cargo_str = "".join([cs if cs != " " else ds for cs, ds in zip(cargo_str, default_str)])
    cargo_str = cargo_str.replace("[", "").replace("]", "").replace(" ", "")
    return cargo_str


def process_cargo(cargo: List[str], stack_number: int) -> Dict[int, str]:

    default_string = " ".join([EMPTY_CRATE] * stack_number)
    cargo_initial = [process_cargo_string(cargo_str=ci, default_str=default_string) for ci in cargo]

    cargo_initial = [ci + "0" * (stack_number - len(ci)) for ci in cargo_initial]
    cargo_initial = {i + 1: "".join([cg[i] for cg in reversed(cargo_initial)]).replace("0", "") for i in
                     range(stack_number)}
    return cargo_initial


def process_moves(moves: List[str]) -> List[List[int]]:
    moves = [m.replace("move ", "").replace("from ", "").replace("to ", "").split(" ") for m in moves]
    moves = [[int(val) for val in m] for m in moves]
    return moves


def process_data(data: List[str]) -> (Dict[int, str], List[List[int]]):
    cargo_initial = [line for line in data if not line.startswith("move")][:-2]
    stack_number = max(list(map(lambda x: int(x) if x else 0, data[len(cargo_initial)].split(" "))))
    cargo_initial = process_cargo(cargo=cargo_initial, stack_number=stack_number)

    moves = [line for line in data if line.startswith("move")]
    moves = process_moves(moves=moves)

    return cargo_initial, moves


def apply_moves(cargo: Dict[int, str], moves: List[List[int]], operator: str = "CrateMover9000") -> Dict[int, str]:
    cargo_final = deepcopy(cargo)
    for move in moves:
        number, fr, to = move
        crates = cargo_final[fr][-number:]
        if operator == "CrateMover9000":
            cargo_final[to] += crates[::-1]
        else:
            cargo_final[to] += crates
        cargo_final[fr] = cargo_final[fr][:-number]
    return cargo_final


def main():
    config = Config(year=2022, day=5)

    # Test case
    path_file = os.path.join(config.path_data, "cargo_test.txt")
    data = read_txt_file(path_file=path_file)
    cargo_initial, moves = process_data(data=data)
    cargo_final = apply_moves(cargo=cargo_initial, moves=moves)

    top_crates = "".join([stack[-1] for _, stack in cargo_final.items() if stack])
    assert top_crates == "CMZ"
    print(f"The top crates are: {''.join(top_crates)}")

    # Part 1
    path_file = os.path.join(config.path_data, "cargo.txt")
    data = read_txt_file(path_file=path_file)
    cargo_initial, moves = process_data(data=data)
    cargo_final = apply_moves(cargo=cargo_initial, moves=moves)

    top_crates = "".join([stack[-1] if stack else " " for _, stack in cargo_final.items()])
    print(f"The top crates are: {''.join(top_crates)}")
    assert top_crates == "WHTLRMZRC"

    # Part 2
    cargo_final = apply_moves(cargo=cargo_initial, moves=moves, operator="CrateMove9001")
    top_crates = "".join([stack[-1] if stack else " " for _, stack in cargo_final.items()])
    print(f"The top crates are: {''.join(top_crates)}")
    assert top_crates == "GMPMLWNMG"

    return True


if __name__ == "__main__":
    main()
