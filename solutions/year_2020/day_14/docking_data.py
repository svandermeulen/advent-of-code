"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 15/12/2020
"""
import doctest
import itertools
import os
import re
from collections import Counter
from copy import copy
from typing import List

from solutions.config import Config
from solutions.year_2020.utils.file_manager import read_txt_file


def parse_program(path_program: str) -> (str, list):
    program = read_txt_file(path_program)

    mask_lines = [i for i, line in enumerate(program) if line.startswith("mask")]

    if len(mask_lines) == 1:
        return [program]

    tasks_list = [program[mask_lines[i]:mask_lines[i + 1]] for i in range(len(mask_lines) - 1)] + [
        program[mask_lines[-1]:]]
    return tasks_list


def parse_task(tasks_list: list) -> (str, list):
    mask = tasks_list[0]
    operations = tasks_list[1:]
    mask = parse_mask(mask=mask)
    operations = parse_operations(operations=operations)

    return mask, operations


def parse_mask(mask: str) -> str:
    return mask.lstrip("mask = ")


def parse_operations(operations: list) -> list:
    operations_list = []
    for operation in operations:
        location, value = operation.split(" = ")
        location = int(location.lstrip("mem[").rstrip("]"))
        value = int(value)
        operations_list.append([location, value])

    return operations_list


def convert_int_to_bit(i: int, bitsize: int = 36) -> str:
    return format(i, "b").zfill(bitsize)


def apply_mask(mask: str, to_write: str) -> str:
    return "".join([to_write[i] if mask[i] in ["X", "0"] else mask[i] for i, _ in enumerate(mask)])


def expand_floating_bits(address: str) -> List[int]:
    if "X" not in address:
        return [int(address)]

    addresses = []
    x_indices = [i for i, char in enumerate(address) if char == "X"]
    n_x = Counter(address)["X"]
    combinations = itertools.product("01", repeat=n_x)
    for combination in combinations:
        address_new = re.split("", copy(address))[1:-1]
        for x_index, replacement in zip(x_indices, combination):
            address_new[x_index] = replacement
        addresses.append(int("".join(address_new), 2))

    return addresses


def apply_mask_v2(mask: str, address: str) -> str:
    """
    DOCTEST

    >>> apply_mask_v2(mask='000000000000000000000000000000X1001X', address='000000000000000000000000000000101010')
    '000000000000000000000000000000X1101X'
    """
    output = "".join([address[i] if mask[i] == "0" else mask[i] for i, _ in enumerate(mask)])
    return output


def execute_operations(operations: list, mask: str, memory: dict) -> dict:
    for (location, value) in operations:
        value_bits = convert_int_to_bit(i=value)
        value_new = apply_mask(mask=mask, to_write=value_bits)
        memory[location] = int(value_new, 2)

    return memory


def execute_program(program: list) -> dict:
    memory = {}
    for tasks in program:
        mask, operations = parse_task(tasks_list=tasks)

        memory = execute_operations(operations=operations, mask=mask, memory=memory)
    return memory


def execute_operations_v2(operations, mask, memory) -> dict:
    for (address, value) in operations:
        address_bits = convert_int_to_bit(i=address)
        address_masked = apply_mask_v2(mask=mask, address=address_bits)
        addresses = expand_floating_bits(address=address_masked)
        for address in addresses:
            memory[address] = value

    return memory


def execute_program_v2(program: list) -> dict:
    memory = {}
    for tasks in program:
        mask, operations = parse_task(tasks_list=tasks)
        memory = execute_operations_v2(operations=operations, mask=mask, memory=memory)

    return memory


def get_memory_sum(memory: dict) -> int:
    return sum(list(memory.values()))


def main():
    config = Config(day=14)

    # PART ONE

    # Test
    path_file_test = os.path.join(config.path_data, "program_test.txt")
    program = parse_program(path_file_test)
    memory = execute_program(program=program)
    assert 165 == get_memory_sum(memory=memory)

    # Real deal
    path_file = os.path.join(config.path_data, "program.txt")
    program = parse_program(path_file)
    memory = execute_program(program=program)
    memory_sum = get_memory_sum(memory=memory)
    print(f"The sum of memory equals: {memory_sum}")
    assert 9619656261720 == memory_sum

    # PART TWO

    # Test
    path_file_test = os.path.join(config.path_data, "program_test_two.txt")
    program = parse_program(path_file_test)
    memory = execute_program_v2(program=program)
    assert 208 == get_memory_sum(memory=memory)

    # Real deal
    program = parse_program(path_file)
    memory = execute_program_v2(program=program)
    memory_sum = get_memory_sum(memory)
    print(f"The sum of memory for part 2 equals: {memory_sum}")
    assert 4275496544925 == sum(list(memory.values()))

    return True


if __name__ == "__main__":
    doctest.testmod()
    main()
