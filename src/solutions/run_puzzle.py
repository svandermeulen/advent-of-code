from solutions.utils.io import read_lines
from solutions.utils.load_module import load_module
from solutions.utils.paths import Paths


def run_puzzle(year: int, day: int, part_nr: int) -> None:
    module = load_module(f"year_{year}\\day_{day}\\part_{part_nr}.py")
    puzzle_input = read_lines(path=Paths(year=year, day=day).path_puzzle_input)
    return module.run(puzzle_input=puzzle_input)


if __name__ == "__main__":
    print(run_puzzle(year=2024, day=3, part_nr=2))
