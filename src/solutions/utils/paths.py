from pathlib import Path


class Paths:
    def __init__(self, year: int, day: int) -> None:
        self.path_home = Path(__file__).parents[3]
        path_data = self.path_home / "data"
        self.path_data = path_data / f"year_{year}" / f"day_{day}"
        self.path_data_tests = path_data / "tests" / f"year_{year}" / f"day_{day}"
        self.path_puzzle_input = self.path_data / "puzzle_input.txt"
