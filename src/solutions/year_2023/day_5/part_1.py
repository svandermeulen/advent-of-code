import re
from enum import Enum
from typing import Iterable


class Category(Enum):
    Seed = 0
    Soil = 1
    Fertilizer = 2
    Water = 3
    Light = 4
    Temperature = 5
    Humidity = 6
    Location = 7


class MappingType(Enum):
    SeedToSoil = 0
    SoilToFertilizer = 1
    FertilizerToWater = 2
    WaterToLight = 3
    LightToTemperature = 4
    TemperatureToHumidity = 5
    HumidityToLocation = 6


class Mapping:
    def __init__(self, mapping_info: list[str]):
        self.mapping_info = mapping_info

    @property
    def name(self) -> str:
        return re.findall(string=self.mapping_info[0], pattern=r"\w+-\w+-\w+")[0]

    @property
    def mapping_type(self) -> MappingType:
        return MappingType["To".join([self.source.name, self.destination.name])]

    @property
    def source(self) -> Category:
        return Category[self.name.split("-")[0].capitalize()]

    @property
    def destination(self) -> Category:
        return Category[self.name.split("-")[-1].capitalize()]

    @property
    def source_ranges(self) -> list[list[int, int]]:
        source_ranges = []
        for line in self.mapping_info[1:]:
            _, source_start, step = map(int, line.split(" "))
            source_ranges.append([source_start, source_start + step - 1])
        return source_ranges

    @property
    def dest_ranges(self) -> list[list[int, int]]:
        dest_ranges = []
        for line in self.mapping_info[1:]:
            dest_start, _, step = map(int, line.split(" "))
            dest_ranges.append([dest_start, dest_start + step - 1])
        return dest_ranges


def apply_mappings(mappings: list[Mapping], source_number: int) -> int:
    if mappings:
        mapping = mappings[0]
        source_range_id = [
            i
            for i, source_range in enumerate(mapping.source_ranges)
            if (source_number >= source_range[0] and source_number <= source_range[1])
        ]
        if not source_range_id:
            return apply_mappings(mappings=mappings[1:], source_number=source_number)
        source_range_id = source_range_id[0]
        dest_number = mapping.dest_ranges[source_range_id][0] + (
            source_number - mapping.source_ranges[source_range_id][0]
        )
        return apply_mappings(mappings=mappings[1:], source_number=dest_number)
    return source_number


def get_mappings(puzzle_input: list[str]) -> list[Mapping]:
    mappings = [*map(lambda x: x.split("|"), "|".join(puzzle_input[2:]).split("||"))]
    return [Mapping(mapping) for mapping in mappings]


def run(puzzle_input: Iterable[str]):
    puzzle_input = list(puzzle_input)
    seeds = [*map(int, puzzle_input[0].split(": ")[1].split(" "))]
    mappings = get_mappings(puzzle_input=puzzle_input)
    locations = []
    for seed in seeds:
        location = apply_mappings(mappings=mappings, source_number=seed)
        locations.append(location)
    return min(locations)
