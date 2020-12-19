import itertools
import string
from typing import Dict, Iterable, List, Tuple

EXPECTED_KEYS = [
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
]


def get_input() -> Iterable[str]:
    with open("input.txt") as file_handle:
        yield from file_handle.read().splitlines()


def split_field(field: str) -> Tuple[str, str]:
    pair = field.split(":")
    assert len(pair) == 2
    return (pair[0], pair[1])


def get_record(input_lines: Iterable[str]) -> Iterable[List[str]]:
    for line in itertools.takewhile(lambda x: x, input_lines):
        yield line.split(" ")


def process_record(input_lines: Iterable[str]) -> Dict[str, str]:
    return dict(
        split_field(field) for field in itertools.chain(*get_record(input_lines))
    )


def get_records(input_lines: Iterable[str]):
    while record := process_record(input_lines):
        yield record


print(
    sum(
        1
        for record in get_records(get_input())
        if set(EXPECTED_KEYS).issubset(set(record.keys()))
    )
)


def is_inside_range(value, lower_bound, upper_bound, length):
    return (
        len(value) == length
        and value.isnumeric()
        and (lower_bound <= int(value) <= upper_bound)
    )


def is_valid_record(record: Dict[str, str]) -> bool:
    if not set(EXPECTED_KEYS).issubset(set(record.keys())):
        return False

    if record["ecl"] not in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"):
        return False

    suffix, height = record["hgt"][-2:], record["hgt"][:-2]
    if suffix == "cm" and not is_inside_range(height, 150, 193, 3):
        return False
    if suffix == "in" and not is_inside_range(height, 59, 76, 2):
        return False
    if suffix not in ("in", "cm"):
        return False

    if len(record["hcl"]) != 7 or not set(record["hcl"][1:]).issubset(
        set(string.hexdigits)
    ):
        return False

    return (
        is_inside_range(record["byr"], 1920, 2002, 4)
        and is_inside_range(record["iyr"], 2010, 2020, 4)
        and is_inside_range(record["eyr"], 2020, 2030, 4)
        and is_inside_range(record["pid"], 0, 999999999, 9)
    )


VALID_RECORDS = """
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""

for test_record in get_records(VALID_RECORDS.splitlines()):
    assert is_valid_record(test_record)

INVALID_RECORDS = """
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""

for test_record in get_records(INVALID_RECORDS.splitlines()):
    assert not is_valid_record(test_record)


print(sum(1 for record in get_records(get_input()) if is_valid_record(record)))
