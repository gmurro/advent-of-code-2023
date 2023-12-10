from dataclasses import dataclass
from pathlib import Path
import re
from typing import List
from pprint import pprint


@dataclass
class Seed:
    id: int
    soil: int
    fertilize: int
    water: int
    light: int
    temperature: int
    humidity: int
    location: int


class AlmanacMap:
    def __init__(self) -> None:
        self.range_mapping = []

    def add(self, dst_start: int, src_start: int, range_length: int) -> None:
        src_end = src_start + range_length - 1
        self.range_mapping.append((src_start, src_end, dst_start))

    def lookup(self, key):
        for src_start, src_end, dst_start in self.range_mapping:
            if src_start <= key <= src_end:
                return key - src_start + dst_start
        return key

    def __getitem__(self, key):
        return self.lookup(key)


def process_mapping(input: str, pattern: str) -> AlmanacMap:
    mapping = AlmanacMap()
    match = re.search(pattern, input)
    if match:
        matched_lines = match.group(1)
        lines = matched_lines.strip().split("\n")
        for line in lines:
            mapping.add(*[int(v) for v in line.strip().split()])
    return mapping


def read_seeds(input: str) -> List[int]:
    pattern = r"\bseeds:\s*([\d\s]+)"
    match = re.search(pattern, input)
    if match:
        return [int(seed) for seed in match.group(1).strip().split()]
    raise ValueError("Bad format in the seeds definition line")


def process_almanac(input) -> List[Seed]:
    mapping_patterns = {
        "seed_to_soil": r"seed-to-soil map:\s*\n([\d+\s+\d+\s+\d+\s*\n]+)",
        "soil_to_fertilizer": r"soil-to-fertilizer map:\s*\n([\d+\s+\d+\s+\d+\s*\n]+)",
        "fertilizer_to_water": r"fertilizer-to-water map:\s*\n([\d+\s+\d+\s+\d+\s*\n]+)",
        "water_to_light": r"water-to-light map:\s*\n([\d+\s+\d+\s+\d+\s*\n]+)",
        "light_to_temperature": r"light-to-temperature map:\s*\n([\d+\s+\d+\s+\d+\s*\n]+)",
        "temperature_to_humidity": r"temperature-to-humidity map:\s*\n([\d+\s+\d+\s+\d+\s*\n]+)",
        "humidity_to_location": r"humidity-to-location map:\s*\n([\d+\s+\d+\s+\d+\s*\n]+)",
    }

    mappings = {}
    for key, pattern in mapping_patterns.items():
        print(f"Processing mapping {key}...")
        mappings[key] = process_mapping(input, pattern)

    seed_ids = read_seeds(input)

    seeds = []
    for id in seed_ids:
        print(f"Processing seed {id}...")
        soil = mappings["seed_to_soil"][id]
        fertilizer = mappings["soil_to_fertilizer"][soil]
        water = mappings["fertilizer_to_water"][fertilizer]
        light = mappings["water_to_light"][water]
        temperature = mappings["light_to_temperature"][light]
        humidity = mappings["temperature_to_humidity"][temperature]
        location = mappings["humidity_to_location"][humidity]
        seeds.append(
            Seed(
                id=id,
                soil=soil,
                fertilize=fertilizer,
                water=water,
                light=light,
                temperature=temperature,
                humidity=humidity,
                location=location,
            )
        )

    return seeds


if __name__ == "__main__":
    input_path = Path(__file__).parent.parent / "input.txt"
    with open(input_path, "r") as file:
        input_str = file.read()
        seeds = process_almanac(input_str)
        min_location = min([s.location for s in seeds])
        print("\nSEEDS")
        pprint(seeds)
        print(f"Lowest location: {min_location}")
