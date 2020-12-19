import itertools
from typing import Iterable, List, Set


def get_input() -> Iterable[str]:
    with open("input.txt") as file_handle:
        yield from file_handle.read().splitlines()


def get_record(input_lines: Iterable[str]) -> Iterable[Set[str]]:
    for line in itertools.takewhile(lambda x: x, input_lines):
        yield set(line)


def get_records(input_lines: Iterable[str]) -> Iterable[List[Set[str]]]:
    while record := list(get_record(input_lines)):
        yield record


# print(sum(len(record_set) for record_set in get_records(get_input(), process_record)))
print(sum(len(set.union(*record_set)) for record_set in get_records(get_input())))
print(
    sum(len(set.intersection(*record_set)) for record_set in get_records(get_input()))
)
