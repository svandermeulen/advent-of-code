"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 14/12/2020
"""
import os
import numpy as np

from typing import List

from solutions.config import Config
from solutions.year_2020.utils.file_manager import read_txt_file


def parse_notes(path_file: str) -> (int, List[int]):
    notes = read_txt_file(path_file=path_file)
    assert len(notes) == 2

    timestamp = int(notes[0])
    buslines = [int(b) for b in notes[1].split(",") if b != "x"]

    return timestamp, buslines


def parse_notes_two(path_file: str) -> (int, List[int]):
    notes = read_txt_file(path_file=path_file)
    assert len(notes) == 2

    timestamp = int(notes[0])
    buslines = [b for b in notes[1].split(",")]

    return timestamp, buslines


def get_timetable(busline: int, array: np.ndarray, colidx: int) -> np.ndarray:
    array[[range(0, array.shape[0], busline)], colidx] = 1
    return array


def get_earliest_bus(timestamp: int, buslines: list) -> (int, int):
    timetable = np.zeros([timestamp + 50, len(buslines)])
    for i, bus in enumerate(buslines):
        timetable = get_timetable(busline=bus, array=timetable, colidx=i)

    timetable = timetable[timestamp:, :]
    minutes_to_wait = min(np.where(timetable == 1)[0])
    bus_earliest = buslines[min(np.where(timetable[minutes_to_wait, :] == 1)[0])]
    return minutes_to_wait, bus_earliest


def get_coefficient(k1: int, multiplier: int, phase: int, denominator: int) -> float:
    return ((k1 * multiplier) + phase) / denominator % 1 == 0


def get_t(buslines: list) -> int:
    phases = [*range(0, len(buslines))]
    phases = [p for i, p in enumerate(phases) if buslines[i] != "x"]
    denominators = [int(b) for b in buslines if b != "x"]

    all_integers = False
    k1 = 0
    iterator_step = 1
    k1_multiplier = denominators[0]
    n_integers_init = 0
    while not all_integers:
        are_integers = [
            get_coefficient(k1=k1, multiplier=k1_multiplier, phase=p, denominator=d) for p, d in zip(phases[1:], denominators[1:])
        ]

        if all(are_integers):
            break

        if all(are_integers[:n_integers_init+1]):
            n_integers_init += 1
            iterator_step = iterator_step * denominators[n_integers_init]

        k1 += iterator_step

    return k1 * k1_multiplier


def main():
    config = Config(day=13)

    # PART ONE

    # Test
    path_data_test = os.path.join(config.path_data, "notes_test.txt")
    timestamp_test, buslines_test = parse_notes(path_file=path_data_test)
    minutes_to_wait, bus_earliest = get_earliest_bus(timestamp=timestamp_test, buslines=buslines_test)
    assert 295 == bus_earliest * minutes_to_wait

    # Real deal
    path_data = os.path.join(config.path_data, "notes.txt")
    timestamp, buslines = parse_notes(path_file=path_data)
    minutes_to_wait, bus_earliest = get_earliest_bus(timestamp=timestamp, buslines=buslines)
    print(
        f"The earliest bus is {bus_earliest} which arrives in {minutes_to_wait} minutes, making the product equal to: "
        f"{minutes_to_wait * bus_earliest}"
    )
    assert 410 == bus_earliest * minutes_to_wait

    # PART TWO

    # Test

    timestamp_test, buslines_test = parse_notes_two(path_file=path_data_test)
    t = get_t(buslines=buslines_test)
    assert 1068781 == t

    buslines_test = ["17", "x", "13", "19"]
    t = get_t(buslines=buslines_test)
    assert 3417 == t

    buslines_test = ["67", "7", "59", "61"]
    t = get_t(buslines=buslines_test)
    assert 754018 == t

    buslines_test = ["67", "x", "7", "59", "61"]
    t = get_t(buslines=buslines_test)
    assert 779210 == t

    # Real deal

    timestamp, buslines = parse_notes_two(path_file=path_data)
    t = get_t(buslines=buslines)
    print(f"t equals: {t} minutes")
    assert 600691418730595 == t
    return True


if __name__ == "__main__":
    main()
