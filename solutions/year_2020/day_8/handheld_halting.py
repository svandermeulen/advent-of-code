"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 08/12/2020
"""
import doctest

import numpy as np
import os

from solutions.config import Config
from solutions.utils import read_txt_file


def parse_line(line: str) -> (str, int):

    """
    Return the command and value of a line in the boot code.
    Can only parse lines that start with "nop", "jmp" or "acc".
    The command must be followed by a positive or negative integer

    DOCTEST
    >>> parse_line(line="jmp -4")
    ('jmp', -4)
    >>> parse_line(line="acc +4")
    ('acc', 4)
    >>> parse_line(line="nop +0")
    ('nop', 0)
    """

    assert any(line.startswith(command) for command in ["nop", "jmp", "acc"]), f"Invalid input line: {line}"

    command, value = line.split(" ")
    value = int(value.strip("+")) if "+" in value else int(value)
    return command, value


def execute_boot_code(boot_code: list) -> (bool, int):

    execution_counter = np.zeros(len(boot_code))
    accumalator = 0
    line_number = 0
    infinite_loop = False

    while line_number < len(boot_code):

        execution_counter[line_number] += 1

        if any(execution_counter > 1):
            infinite_loop = True
            break

        line = boot_code[line_number]
        command, value = parse_line(line=line)
        if command == "acc":
            accumalator += value
            line_number += 1
        elif command == "jmp":
            line_number += value
        else:
            line_number += 1

    return infinite_loop, accumalator


def fix_boot_code(boot_code: list) -> (bool, int, list):

    """
    Fix input boot code by changing a single line containing 'jmp' or 'nop' to either 'nop' or 'jmp' respectively
    For each change check if boot code runs until termination
    """

    lines_nop_or_jmp = [i for i, line in enumerate(boot_code) if "jmp" in line or "nop" in line]
    infinite_loop = False
    accumulator = 0
    boot_code_original = boot_code.copy()

    for line_number in lines_nop_or_jmp:
        boot_code = boot_code_original.copy()
        if "jmp" in boot_code[line_number]:
            boot_code[line_number] = boot_code[line_number].replace("jmp", "nop")
        elif "nop" in boot_code[line_number]:
            boot_code[line_number] = boot_code[line_number].replace("nop", "jmp")
        else:
            raise ValueError("Invalid line number")

        infinite_loop, accumulator = execute_boot_code(boot_code=boot_code)
        if not infinite_loop:
            break

    return infinite_loop, accumulator, boot_code


def main():
    config = Config(day=8)

    # PART ONE
    path_file_test = os.path.join(config.path_data, "boot_code_test.txt")
    path_file = os.path.join(config.path_data, "boot_code.txt")

    # Test set
    data_test = read_txt_file(path_file=path_file_test)
    print(f"The test boot code has {len(data_test)} lines")
    infinite_loop, accumulator = execute_boot_code(boot_code=data_test)
    assert infinite_loop, f"Execution of bootcode did not enter a infinite loop"
    assert 5 == accumulator, f"Accumulator value is incorrect. 5 != {accumulator}"

    data = read_txt_file(path_file=path_file)
    print(f"The boot code has {len(data)} lines")
    infinite_loop, accumulator = execute_boot_code(boot_code=data)
    print(f"The boot code accumulator equals {accumulator} before it hits an infinite loop")
    assert infinite_loop, f"Execution of bootcode did not enter a infinite loop"
    assert 1939 == accumulator, f"Accumulator value is incorrect. 1939 != {accumulator}"

    # PART TWO
    infinite_loop, accumulator, boot_code = fix_boot_code(boot_code=data_test)
    assert not infinite_loop
    assert 8 == accumulator, f"Accumulator value is incorrect. 8 != {accumulator}"

    infinite_loop, accumulator, boot_code = fix_boot_code(boot_code=data)
    assert not infinite_loop
    print(f"The fixed boot code accumulator equals {accumulator} after running until termination")
    assert 2212 == accumulator, f"Accumulator value is incorrect. 2212 != {accumulator}"

    return True


if __name__ == "__main__":
    doctest.testmod()
    main()
