"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 16/12/2020
"""
import os
from typing import List, Tuple

from solutions.config import Config
from solutions.year_2020.utils.file_manager import read_txt_file


def parse_ticket_info(path_file: str) -> Tuple[list, list, list]:
    data = read_txt_file(path_file)
    notes = []
    ticket_mine = []
    tickets_nearby = []

    line_type = "note"
    for line in data:

        if not line:
            continue

        if not line.startswith("your ticket:") and line_type == "note":
            notes.append(line)
        elif line.startswith("your ticket"):
            line_type = "ticket_mine"
        elif line.startswith("nearby tickets:"):
            line_type = "tickets_nearby"
        elif line_type == "ticket_mine":
            ticket_mine.append(line)
        elif line_type == "tickets_nearby":
            tickets_nearby.append(line)
        else:
            raise ValueError

    return notes, ticket_mine, tickets_nearby


def parse_note_values(value: str) -> list:

    if "or" not in value:
        raise ValueError

    ranges = value.split(" or ")
    value_range = [*range(int(ranges[0].split("-")[0]), int(ranges[0].split("-")[1])+1)]
    value_range.extend([*range(int(ranges[1].split("-")[0]), int(ranges[1].split("-")[1])+1)])

    return value_range


def parse_notes(notes: list) -> dict:
    notes = {note.split(":")[0]: note.split(":")[1] for note in notes}
    notes = {key: parse_note_values(value) for key, value in notes.items()}
    return notes


def parse_tickets_nearby(tickets_nearby: list) -> list:

    tickets_nearby = [{int(value) for value in ticket.split(",")} for ticket in tickets_nearby]
    return tickets_nearby


def compute_error_rate(path_ticket_info: str) -> int:

    notes, ticket_mine, tickets_nearby = parse_ticket_info(path_file=path_ticket_info)
    notes = parse_notes(notes=notes)
    values_valid = set(sorted([item for sublist in notes.values() for item in sublist]))
    tickets_nearby = parse_tickets_nearby(tickets_nearby)
    values_invalid = [ticket.difference(values_valid) for ticket in tickets_nearby if not ticket.issubset(values_valid)]
    values_invalid = [item for sublist in values_invalid for item in sublist]
    error_rate = sum(values_invalid)
    return error_rate


def main():
    config = Config()

    # Test
    path_ticket_info = os.path.join(config.path_data, "day_16", "ticket_info_test.txt")
    error_rate = compute_error_rate(path_ticket_info=path_ticket_info)
    assert 71 == error_rate

    # Real deal
    path_ticket_info = os.path.join(config.path_data, "day_16", "ticket_info.txt")
    error_rate = compute_error_rate(path_ticket_info=path_ticket_info)
    print(f"The ticket scanning error rate equals: {error_rate}")
    # assert 71 == error_rate

    pass


if __name__ == "__main__":
    main()
