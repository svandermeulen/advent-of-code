"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 16/12/2020
"""
import os
from math import prod
from typing import Tuple

import numpy as np

from solutions.config import Config
from solutions.year_2020.utils.file_manager import read_txt_file


def parse_ticket_info(path_file: str) -> Tuple[dict, list, list]:
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

    notes = parse_notes(notes=notes)
    ticket_mine = parse_tickets(ticket_mine)[0]
    tickets_nearby = parse_tickets(tickets_nearby)

    return notes, ticket_mine, tickets_nearby


def parse_note_values(value: str) -> list:
    if "or" not in value:
        raise ValueError

    ranges = value.split(" or ")
    value_range = [*range(int(ranges[0].split("-")[0]), int(ranges[0].split("-")[1]) + 1)]
    value_range.extend([*range(int(ranges[1].split("-")[0]), int(ranges[1].split("-")[1]) + 1)])

    return value_range


def parse_notes(notes: list) -> dict:
    notes = {note.split(":")[0]: note.split(":")[1] for note in notes}
    notes = {key: parse_note_values(value) for key, value in notes.items()}
    return notes


def parse_tickets(tickets_nearby: list) -> list:
    tickets_nearby = [[int(value) for value in ticket.split(",")] for ticket in tickets_nearby]
    return tickets_nearby


def compute_error_rate(path_ticket_info: str) -> int:
    notes, ticket_mine, tickets_nearby = parse_ticket_info(path_file=path_ticket_info)
    values_valid = set(sorted([item for sublist in notes.values() for item in sublist]))

    values_invalid = [set(ticket).difference(values_valid) for ticket in tickets_nearby if
                      not set(ticket).issubset(values_valid)]
    values_invalid = [item for sublist in values_invalid for item in sublist]
    error_rate = sum(values_invalid)
    return error_rate


def find_field(field_order: np.ndarray, tickets_valid: list, notes: dict) -> list:

    fields_temp = {}
    for i in range(field_order.shape[0]):
        values = set([ticket[i] for ticket in tickets_valid])
        fields = [field for field, note in notes.items() if values.issubset(set(note)) and field not in field_order]
        fields_temp[i] = fields

    field = {field_location: field_list[0] for field_location, field_list in fields_temp.items() if len(field_list) == 1}
    field_order[list(field.keys())[0]] = list(field.values())[0]

    if not set(field_order) == set(notes.keys()):
        field_order = find_field(field_order=field_order, tickets_valid=tickets_valid, notes=notes)

    return field_order


def get_field_order(notes: dict, tickets_nearby: list) -> list:
    values_valid = set(sorted([item for sublist in notes.values() for item in sublist]))
    tickets_valid = [ticket for ticket in tickets_nearby if set(ticket).issubset(values_valid)]
    field_order = np.empty(max({*map(len, tickets_valid)})).astype(str)
    field_order = find_field(field_order=field_order, tickets_valid=tickets_valid, notes=notes)
    return list(field_order)


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
    assert 24980 == error_rate

    # PART TWO

    # Test
    path_ticket_info = os.path.join(config.path_data, "day_16", "ticket_info_test_two.txt")
    notes, ticket_mine, tickets_nearby = parse_ticket_info(path_file=path_ticket_info)
    field_order = get_field_order(notes=notes, tickets_nearby=tickets_nearby)
    assert ["row", "class", "seat"] == field_order

    # Real deal
    path_ticket_info = os.path.join(config.path_data, "day_16", "ticket_info.txt")
    notes, ticket_mine, tickets_nearby = parse_ticket_info(path_file=path_ticket_info)
    field_order = get_field_order(notes=notes, tickets_nearby=tickets_nearby)
    fields_departure = [i for i, f in enumerate(field_order) if "departure" in f]
    print(f"The product of the departure fields equals: {prod([ticket_mine[i] for i in fields_departure])}")
    assert 809376774329 == prod([ticket_mine[i] for i in fields_departure])

    return True


if __name__ == "__main__":
    main()
