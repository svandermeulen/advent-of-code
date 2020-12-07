"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 07/12/2020
"""
import os


def read_txt_file(path_file: str) -> list:

    assert os.path.isfile(path_file), f"{path_file} does not exist"

    with open(path_file, "r") as f:
        data = [value.strip("\n") for value in f.readlines()]

    return data


def main():
    pass


if __name__ == "__main__":
    main()
