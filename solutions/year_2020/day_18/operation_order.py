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
from solutions.year_2020.utils.file_manager import read_txt_file


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
        handle_parenthesis(expression=expression, solver=solve_math_expression_part_one)

    expression_new = re.sub(r"(\d+)", r"\1)", expression)
    parenthesis_left, parenthesis_right = count_parenthesis(expression=expression_new)
    expression_new = (parenthesis_right - parenthesis_left) * "(" + expression_new
    return eval(expression_new)


def solve_math_expression_part_two(expression: str) -> int:
    """
    DOCTEST
    >>> solve_math_expression_part_one(expression='1 + 2 * 3 + 4 * 5 + 6')
    231
    >>> solve_math_expression_part_one(expression='1 + (2 * 3) + (4 * (5 + 6))')
    51
    >>> solve_math_expression_part_one(expression='2 * 3 + (4 * 5)')
    46
    >>> solve_math_expression_part_one(expression='5 + (8 * 3 + 9 + 3 * 4 * 3)')
    1445
    >>> solve_math_expression_part_one(expression='5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))')
    669060
    >>> solve_math_expression_part_one(expression='((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2')
    23340
    """

    if " " in expression:
        expression = expression.replace(" ", "")

    while "(" in expression:
        expression = handle_parenthesis(expression=expression, solver=solve_math_expression_part_two)

    expression_new = re.sub(r"(\d+)", r"\1)", expression)
    parenthesis_left, parenthesis_right = count_parenthesis(expression=expression_new)
    expression_new = (parenthesis_right - parenthesis_left) * "(" + expression_new
    return eval(expression_new)


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

    return True


if __name__ == "__main__":
    doctest.testmod()
    main()
