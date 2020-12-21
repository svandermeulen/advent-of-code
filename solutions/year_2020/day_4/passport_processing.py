"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 04/12/2020
"""
import doctest
import os
import re

from typing import List

from solutions.config import Config

FIELDS_EXPECTED = [
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid"
]


def parse_data(data: list) -> List[dict]:
    data = ";".join(data)
    data = data.replace(";;", ";+;")
    data = data.split("+")
    data = [re.split(";|\s", line.strip(";")) for line in data]
    return [{l.split(":")[0]: l.split(":")[1] for l in d} for d in data]


def validate_birth_year(passport: dict) -> bool:
    """
    Return True if the birthyear in a password is between 1920 and 2002

    DOCTEST
    >>> validate_birth_year(passport={"ecl": "gry", "byr": "1937"})
    True
    >>> validate_birth_year(passport={"ecl": "gry", "byr": "1919"})
    False
    >>> validate_birth_year(passport={"ecl": "gry", "byr": "2003"})
    False
    >>> validate_birth_year(passport={"ecl": "gry"})
    False
    """

    birth_year = passport.get("byr")
    if not birth_year:
        return False

    if 1920 <= int(birth_year) <= 2002:
        return True
    return False


def validate_issue_year(passport: dict) -> bool:
    issue_year = passport.get("iyr")
    if not issue_year:
        return False

    if 2010 <= int(issue_year) <= 2020:
        return True
    return False


def validate_expiration_year(passport: dict) -> bool:
    expiration_year = passport.get("eyr")
    if not expiration_year:
        return False
    if 2020 <= int(expiration_year) <= 2030:
        return True
    return False


def validate_height(passport: dict) -> bool:
    """
    Return True if a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.

    DOCTEST
    >>> validate_height(passport={"ecl": "gry", "hgt": "60in"})
    True
    >>> validate_height(passport={"ecl": "gry", "hgt": "190cm"})
    True
    >>> validate_height(passport={"ecl": "gry", "hgt": "190in"})
    False
    >>> validate_height(passport={"ecl": "gry", "hgt": "190"})
    False
    """

    height = passport.get("hgt")
    if not height:
        return False

    if "cm" in height:
        height = int(height.strip("cm"))
        if 150 <= height <= 193:
            return True
        else:
            return False
    if "in" in height:
        height = int(height.strip("in"))
        if 59 <= height <= 76:
            return True
    return False


def validate_hair_color(passport: dict) -> bool:
    """
    Return True if value of haircolor is a # followed by exactly six characters 0-9 or a-f.

    DOCTEST
    >>> validate_hair_color(passport={"hcl": "#123abc", "byr": "1937"})
    True
    >>> validate_hair_color(passport={"hcl": "#123abz", "byr": "1937"})
    False
    >>> validate_hair_color(passport={"hcl": "123abz", "byr": "1937"})
    False
    """

    hair_color = passport.get("hcl")
    if not hair_color:
        return False

    if re.match("#[0-9a-f]{6}", hair_color):
        return True
    return False


def validate_eye_color(passport: dict) -> bool:
    """
    Return True if value of eyecolor is equal to  amb blu brn gry grn hzl oth

    DOCTEST
    >>> validate_eye_color(passport={"ecl": "brn", "byr": "1937"})
    True
    >>> validate_eye_color(passport={"ecl": "wat", "byr": "1937"})
    False
    """

    eye_colors_exp = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
    eye_color = passport.get("ecl")
    if not eye_color:
        return False

    if eye_color not in eye_colors_exp:
        return False
    return True


def validate_passport_id(passport: dict) -> bool:
    """
    Return True if value of haircolor is a # followed by exactly six characters 0-9 or a-f.

    DOCTEST
    >>> validate_passport_id(passport={"hcl": "#123abc", "pid": "000000001"})
    True
    >>> validate_passport_id(passport={"hcl": "#123abz", "pid": "0123456789"})
    False
    """
    passport_id = passport.get("pid")
    if not passport_id:
        return False

    if len(passport_id) > 9:
        return False

    if re.match("[0-9]{9}", passport_id):
        return True
    return False


def validate_passport_one(passport: dict) -> bool:
    """
    Return True if a password carries all the expected fields else return False

    DOCTEST
    >>> validate_passport_one(passport={"ecl": "gry", "pid": 860033327, "eyr": 2020, "hcl": "#fffffd", "byr": 1937, "iyr": 2017, "cid": 147, "hgt": "183cm"})
    True
    >>> validate_passport_one(passport={"ecl": "gry", "pid": 860033327, "eyr": 2020, "hcl": "#fffffd"})
    False
    """

    if all([key in passport.keys() for key in FIELDS_EXPECTED]):
        return True
    return False


def validate_passport_two(passport: dict) -> bool:
    if not validate_birth_year(passport=passport):
        return False
    if not validate_issue_year(passport=passport):
        return False
    if not validate_expiration_year(passport=passport):
        return False
    if not validate_height(passport=passport):
        return False
    if not validate_hair_color(passport=passport):
        return False
    if not validate_eye_color(passport=passport):
        return False
    if not validate_passport_id(passport=passport):
        return False
    return True


def main():
    config = Config(day=4)
    path_file = os.path.join(config.path_data, "passport_batch_files.txt")
    path_file_invalid = os.path.join(config.path_data, "passport_batch_files_invalid_test.txt")
    path_file_valid = os.path.join(config.path_data, "passport_batch_files_valid_test.txt")

    with open(path_file, "r") as f:
        data = [value.strip("\n") for value in f.readlines()]

    data_parsed = parse_data(data=data)
    passport_validity = [*map(validate_passport_one, data_parsed)]

    print("PART ONE")
    print(f"Number of valid passports: {sum(passport_validity)} / {len(passport_validity)}")

    with open(path_file_invalid, "r") as f:
        data_invalid = [value.strip("\n") for value in f.readlines()]
    data_invalid_parsed = parse_data(data=data_invalid)
    passport_validity = [*map(validate_passport_two, data_invalid_parsed)]
    assert not all(passport_validity)

    with open(path_file_valid, "r") as f:
        data_valid = [value.strip("\n") for value in f.readlines()]
    data_valid_parsed = parse_data(data=data_valid)
    passport_validity = [*map(validate_passport_two, data_valid_parsed)]
    assert all(passport_validity)

    passport_validity = [*map(validate_passport_two, data_parsed)]

    print("PART TWO")
    print(f"Number of valid passports: {sum(passport_validity)} / {len(passport_validity)}")

    return True


if __name__ == "__main__":
    doctest.testmod()
    main()
