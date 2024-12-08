import pytest
from typing_extensions import Iterable

from solutions.year_2024.day_3.part_2 import run
from solutions.utils.io import read_lines
from solutions.utils.paths import Paths


@pytest.mark.parametrize(
    "test_input, expected", [(read_lines(path=Paths(year=2024, day=3).path_data_tests / "example_2.txt"), 48)]
)
def test_run(test_input: Iterable[str], expected: int) -> None:
    assert run(puzzle_input=test_input) == expected
