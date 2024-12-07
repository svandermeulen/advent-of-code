import re
from typing import Iterable

WORD_2_NUMBER = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}


def parse_number(txt: str) -> int:
    if txt.isnumeric():
        return int(txt)
    if txt.lower() in WORD_2_NUMBER:
        return WORD_2_NUMBER[txt]
    raise ValueError


def find_first_and_last_digit(txt: str) -> int:
    digits_spelled = [key for key in WORD_2_NUMBER.keys() if key in txt.lower()]
    digits = [str(val) for val in WORD_2_NUMBER.values() if str(val) in txt.lower()]

    digit_positions = {d: [match.span()[0] for match in re.finditer(d, txt)] for d in digits + digits_spelled}
    first_pos = min([val for d in digit_positions.values() for val in d])
    last_pos = max([val for d in digit_positions.values() for val in d])
    digits_desired = [key for key, val in digit_positions.items() if first_pos in val]
    digits_desired += [key for key, val in digit_positions.items() if last_pos in val]
    numeric_chars = [str(parse_number(digit)) for digit in digits_desired]
    if len(numeric_chars) == 1:
        numeric_chars = numeric_chars * 2
    return int("".join(numeric_chars))


def run(puzzle_input: Iterable[str]) -> int:
    return sum(find_first_and_last_digit(txt=item) for item in puzzle_input)
