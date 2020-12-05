"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 05/12/2020
"""
import os

from solutions.config import Config


def get_row(row_sequence: str, row_indices: list) -> list:
    if not len(row_indices) <= 1:
        if row_sequence[0] == "F":
            return get_row(row_sequence=row_sequence[1:], row_indices=row_indices[:len(row_indices) // 2])
        return get_row(row_sequence=row_sequence[1:], row_indices=row_indices[len(row_indices) // 2:])
    return row_indices


def get_column(col_sequence: str, col_indices: list) -> list:
    if not len(col_indices) <= 1:
        if col_sequence[0] == "L":
            return get_column(col_sequence=col_sequence[1:], col_indices=col_indices[:len(col_indices) // 2])
        return get_column(col_sequence=col_sequence[1:], col_indices=col_indices[len(col_indices) // 2:])
    return col_indices


def get_seat_id(row: int, column: int) -> int:
    return row * 8 + column


def main():
    config = Config()
    path_file = os.path.join(config.path_data, "day_5", "boarding_passes.txt")

    with open(path_file, "r") as f:
        boarding_passes = [value.strip("\n") for value in f.readlines()]

    print(f"The number of boarding passes equals: {len(boarding_passes)}")

    boarding_passes_test = ["BFFFBBFRRR", "FFFBBBFRRR", "BBFFBBFRLL"]

    row_indices = [*range(0, 128)]
    column_indices = [*range(0, 8)]

    for boarding_pass, row_number_exp, col_number_exp in zip(boarding_passes_test, [70, 14, 102], [7, 7, 4]):
        row, = get_row(row_sequence=boarding_pass[:7], row_indices=row_indices)
        assert row_number_exp == row

        column, = get_column(col_sequence=boarding_pass[7:], col_indices=column_indices)
        assert col_number_exp == column
        seat_id = get_seat_id(row=row, column=column)
        print(f"Boardingpass {boarding_pass}, sits on row {row} and column {column}, with seat id {seat_id}")

    seat_ids = []
    for boarding_pass in boarding_passes:
        row, = get_row(row_sequence=boarding_pass[:7], row_indices=row_indices)
        column, = get_column(col_sequence=boarding_pass[7:], col_indices=column_indices)
        seat_ids.append(get_seat_id(row=row, column=column))

    print(f"The seat with the highest seat ID equals: {max(seat_ids)}")

    # PART TWO
    missing_seat_ids = set(range(0, max(seat_ids))).difference(set(seat_ids))
    for seat_id in missing_seat_ids:
        if seat_id - 1 in seat_ids and seat_id + 1 in seat_ids:
            print(f"Your seat ID: {seat_id}")

    return True


if __name__ == "__main__":
    main()
