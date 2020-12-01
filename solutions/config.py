"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 01/12/2020
"""

import os


class Config:

    def __init__(self, year: int = 2020):
        self.path_home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.path_data = os.path.join(self.path_home, "data", f"{year}")


def main():
    config = Config()
    print(config.path_data)


if __name__ == "__main__":
    main()
