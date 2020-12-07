"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 02/12/2020
"""
import doctest
import os

from typing import List

from solutions.config import Config


def split_policy_and_password(string: str) -> List[str]:
    return string.split(": ")


def split_policy(policy: str) -> (List[int], str):
    policy_integers, character = policy.split(" ")
    policy_integers = [int(v) for v in policy_integers.split("-")]
    return policy_integers, character


def is_valid_rule_one(character_count_range: List[int], character: str, password: str) -> bool:
    """
    Return True if a password is abides to its asscoiated policy else return False
    The policy is represented as follows: [1-3] a --> the character a should occur at least 1 time and at most 3 times

    DOCTEST
    >>> is_valid_rule_one(character_count_range=[6, 10], character='p', password='ctpppjmdpppppp')
    True
    >>> is_valid_rule_one(character_count_range=[6, 10], character='p', password='ctpppjmdpppppppp')
    False

    """
    character_count = sum([c == character for c in password])
    if min(character_count_range) <= character_count <= max(character_count_range):
        return True
    return False


def is_valid_rule_two(character_indices_policy: List[int], character: str, password: str) -> bool:
    """
    Return True if a password is abides to its asscoiated policy else return False
    The policy is represented as follows:
        '[1-3] a' --> the character 'a' should occur either as the first or the third character not both

    DOCTEST
    >>> is_valid_rule_two(character_indices_policy=[6, 10], character='p', password='ctpppjmdpppppp')
    True
    >>> is_valid_rule_two(character_indices_policy=[6, 10], character='p', password='ctppppmdpppppppp')
    False
    >>> is_valid_rule_two(character_indices_policy=[6, 10], character='p', password='ctpppmdpplppppp')
    False
    """
    character_indices = [i + 1 for i, c in enumerate(password) if c == character]
    if len(set(character_indices_policy).intersection(set(character_indices))) == 1:
        return True
    return False


def main():
    config = Config()
    path_file = os.path.join(config.path_data, "day_2", "password_policies.txt")

    with open(path_file, "r") as f:
        data = [value.strip("\n") for value in f.readlines()]

    valid_passwords_one = []
    valid_passwords_two = []
    for string in data:
        policy, password = split_policy_and_password(string=string)
        policy_integers, character = split_policy(policy=policy)
        if is_valid_rule_one(character_count_range=policy_integers, character=character, password=password):
            valid_passwords_one.append(string)
        if is_valid_rule_two(character_indices_policy=policy_integers, character=character, password=password):
            valid_passwords_two.append(string)

    print(f"The number of valid passwords according to rule #1 is: {len(valid_passwords_one)}")
    print(f"The number of valid passwords according to rule #2 is: {len(valid_passwords_two)}")

    return True


if __name__ == "__main__":
    doctest.testmod()
    main()
