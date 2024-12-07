from typing import Iterable

import pytest

from solutions.utils.io import read_lines
from solutions.utils.paths import Paths
from solutions.year_2023.day_1.part_1 import run


@pytest.mark.parametrize(
    "test_input, expected", [(read_lines(path=Paths(year=2023, day=1).path_data_tests / "example_1.txt"), 142)]
)
def test_run(test_input: Iterable[str], expected: int) -> None:
    assert run(puzzle_input=test_input) == expected
