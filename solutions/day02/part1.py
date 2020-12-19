import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable


@dataclass
class Record:
    minimum: int
    maximum: int
    character: str
    password: str

    def __post_init__(self):
        self.minimum = int(self.minimum)
        self.maximum = int(self.maximum)


PATTERN = r"([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)"


def get_data() -> Iterable[Record]:
    with open("./input.txt") as file_handle:
        for line in file_handle.read().splitlines():
            if match := re.match(PATTERN, line):
                groups = match.groups()
                yield Record(int(groups[0]), int(groups[1]), groups[2], groups[3])


def is_valid(record: Record) -> bool:
    return (
        record.minimum <= Counter(record.password)[record.character] <= record.maximum
    )


def is_valid2(record: Record) -> bool:
    return (record.password[record.minimum - 1] == record.character) ^ (
        record.password[record.maximum - 1] == record.character
    )


print(sum(1 for record in get_data() if is_valid(record)))
print(sum(1 for record in get_data() if is_valid2(record)))
