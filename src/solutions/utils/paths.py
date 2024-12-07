from pathlib import Path


class Paths:
    def __init__(self, year: int, day: int) -> None:
        self.path_home = Path.cwd().parents[1]
        self.path_data = self.path_home / "data" / f"year_{year}" / f"day_{day}"
        self.path_data_tests = self.path_data / "tests"
        self.path_puzzle_input = self.path_data / "puzzle_input.txt"
