import pytest
from typing_extensions import Iterable

from solutions.year_2023.day_5.part_1 import run
from solutions.utils.io import read_lines
from solutions.utils.paths import Paths


@pytest.mark.parametrize(
    "test_input, expected", [(read_lines(path=Paths(year=2023, day=5).path_data_tests / "example_1.txt"), 35)]
)
def test_run(test_input: Iterable[str], expected: int) -> None:
    assert run(puzzle_input=test_input) == expected
