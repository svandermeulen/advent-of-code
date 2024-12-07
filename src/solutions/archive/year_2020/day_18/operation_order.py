"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 22/12/2020
"""
import doctest
import os
import re

from collections import Counter
from typing import Tuple, Callable

from solutions.config import Config
from solutions.utils import read_txt_file


def count_parenthesis(expression: str) -> Tuple[int, int]:
    character_count = Counter(expression)
    return character_count["("], character_count[")"]


def evaluate_parenthesis(expression: str) -> str:
    """
    DOCTEST
    >>> evaluate_parenthesis(expression='((2 + 4 * 9)')
    '(2 + 4 * 9)'
    """

    n_parenthesis_left, n_parenthesis_right = count_parenthesis(expression=expression)

    if n_parenthesis_left == n_parenthesis_right:
        return expression

    if n_parenthesis_left > n_parenthesis_right:
        return expression[1:]
    return expression[:-1]


def handle_parenthesis(expression: str, solver: Callable) -> str:
    groups = re.findall(r"\([\d*+]+\)", expression)
    for group in groups:
        group = evaluate_parenthesis(expression=group)
        group_stripped = group[1:-1]
        expression = expression.replace(group, str(solver(expression=group_stripped)))

    return expression


def solve_math_expression_part_one(expression: str) -> int:
    """
    DOCTEST
    >>> solve_math_expression_part_one(expression='1 + 2 * 3 + 4 * 5 + 6')
    71
    >>> solve_math_expression_part_one(expression='1 + (2 * 3) + (4 * (5 + 6))')
    51
    >>> solve_math_expression_part_one(expression='2 * 3 + (4 * 5)')
    26
    >>> solve_math_expression_part_one(expression='5 + (8 * 3 + 9 + 3 * 4 * 3)')
    437
    >>> solve_math_expression_part_one(expression='5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))')
    12240
    >>> solve_math_expression_part_one(expression='9 + (5 * 5 + 2 + (5 * 2 + 6 * 9 * 3 + 6) * 4) + 3 * 5')
    9360
    >>> solve_math_expression_part_one(expression='((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2')
    13632
    """

    if " " in expression:
        expression = expression.replace(" ", "")

    while "(" in expression:
        expression = handle_parenthesis(expression=expression, solver=solve_math_expression_part_one)

    expression_new = re.sub(r"(\d+)", r"\1)", expression)
    parenthesis_left, parenthesis_right = count_parenthesis(expression=expression_new)
    expression_new = (parenthesis_right - parenthesis_left) * "(" + expression_new
    return eval(expression_new)


def solve_math_expression_part_two(expression: str) -> int:
    """
    DOCTEST
    # >>> solve_math_expression_part_two(expression='1 + 2 * 3 + 4 * 5 + 6')
    # 231
    # >>> solve_math_expression_part_two(expression='1 + (2 * 3) + (4 * (5 + 6))')
    # 51
    # >>> solve_math_expression_part_two(expression='2 * 3 + (4 * 5)')
    # 46
    # >>> solve_math_expression_part_two(expression='5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))')
    # 669060
    # >>> solve_math_expression_part_two(expression='((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2')
    # 23340
    # >>> solve_math_expression_part_two(expression='5 + (8 * 3 + 9 + 3 * 4 * 3)')
    # 1445
    # >>> solve_math_expression_part_two(expression='9 + (5 * 5 + 2 + (5 * 2 + 6 * 9 * 3 + 6) * 4) + 3 * 5')
    # 324760
    # >>> solve_math_expression_part_two(expression='9 + (3 + 6 + (3 * 6 * 5 * 2 + 5)) * (9 * 7 * 4 * 6 * 2) + 4 + (7 + 7 + 8 + 5 * 8) * (4 * (3 * 5 + 2))')
    # 176577408
    # >>> solve_math_expression_part_two(expression='5 * 7 + (6 + 7 * 5 * 5 * (9 + 9 * 2 + 8 * 5 * 6)) * 8 * 8 + (9 * (8 * 3 * 7 * 6 + 2 + 2) * 9 + 6 * 4)')
    # 63686255618240
    # >>> solve_math_expression_part_two(expression='((7 * 4) * 9 * 4 + 9 + 4 + (8 * 4 + 6 + 2)) + 2 * 5 + 8 + 6 * 5')
    # 2705410
    >>> solve_math_expression_part_two(expression='((7 + 6 + 8 * 9 * 3 + 8) * 8 + (2 + 4 + 7) + 3 * 2) * 5')
    498960
    """

    if " " in expression:
        expression = expression.replace(" ", "")

    while "(" in expression:
        expression = handle_parenthesis(expression=expression, solver=solve_math_expression_part_two)

    if "*" not in expression:
        return eval(expression)

    while "+" in expression:
        additions = re.findall(r"[*+]?\d+\+\d+[*+]?", expression)

        # To avoid replacing duplicating summations or products, include the pre and/or post operator in the string
        for addition in additions:
            if (addition.endswith("+") or addition.endswith("*")) and (addition.startswith("+") or addition.startswith("*")):
                addition_stripped = addition[1:-1]
                operator_start = addition[0]
                operator_end = addition[-1]
            elif addition.endswith("+") or addition.endswith("*"):
                addition_stripped = addition[:-1]
                operator_end = addition[-1]
                operator_start = ""
            elif addition.startswith("+") or addition.startswith("*"):
                addition_stripped = addition[1:]
                operator_start = addition[0]
                operator_end = ""
            else:
                addition_stripped = addition
                operator_start = ""
                operator_end = ""

            expression = expression.replace(addition, operator_start + str(eval(addition_stripped)) + operator_end)

    return eval(expression)


def execute_homework(path_homework: str, solver: Callable) -> list:
    homework = read_txt_file(path_homework)

    homework_solutions = [*map(solver, homework)]
    return homework_solutions


def main():
    config = Config(day=18)
    path_homework = os.path.join(config.path_data, "homework.txt")

    # PART ONE
    results = execute_homework(path_homework=path_homework, solver=solve_math_expression_part_one)
    print(f"The sum of the resulting values: {sum(results)}")
    assert 131076645626 == sum(results)

    # PART TWO
    results = execute_homework(path_homework=path_homework, solver=solve_math_expression_part_two)
    print(f"The sum of the resulting values (PART TWO): {sum(results)}")
    assert 109418509151782 == sum(results)
    return True


if __name__ == "__main__":
    doctest.testmod()
    main()
