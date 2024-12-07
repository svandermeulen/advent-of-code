import re
from collections import defaultdict
from typing import Iterable


def parse_line(line: str) -> (int, list[str], list[str]):
    card_id, numbers = re.split(pattern=r":\s+", string=line)
    card_id = int(re.findall(pattern=r"\d+", string=card_id)[0])
    winning_numbers, my_numbers = numbers.split(" | ")
    winning_numbers = re.split(string=winning_numbers, pattern=r"\s+")
    my_numbers = re.split(string=my_numbers, pattern=r"\s+")
    return card_id, winning_numbers, my_numbers


def run(puzzle_input: Iterable[str]):
    card_copies = defaultdict(int)
    for i, line in enumerate(puzzle_input):
        card_id, winning_numbers, my_numbers = parse_line(line=line)
        card_copies[card_id] += 1
        overlap = list(map(int, set(winning_numbers).intersection(set(my_numbers))))
        for next_id in range(1, len(overlap) + 1):
            card_copies[card_id + next_id] += card_copies[card_id]
    return sum(card_copies.values())
