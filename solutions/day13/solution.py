import itertools
from dataclasses import dataclass
from functools import reduce
from typing import Iterable, Sequence, Tuple

TEST_INPUT = """\
939
7,13,x,x,59,x,31,19
"""


@dataclass
class Notes:
    time: int
    buses: str

    def get_bus_numbers(self) -> Iterable[int]:
        for bus in self.buses.split(","):
            if bus != "x":
                yield int(bus)

    def get_bus_offsets(self) -> Iterable[Tuple[int, int]]:
        for index, bus in enumerate(self.buses.split(",")):
            if bus != "x":
                yield int(bus) - index, int(bus)


def get_input() -> Iterable[str]:
    with open("input.txt") as file_handle:
        yield from file_handle.read().splitlines()


def get_test_input() -> Iterable[str]:
    return iter(TEST_INPUT.splitlines())


def get_notes(input_lines: Iterable[str]) -> Notes:
    bus, notes = input_lines
    return Notes(int(bus), notes)


def get_next_bus(notes: Notes) -> Tuple[int, int]:
    bus_numbers = list(notes.get_bus_numbers())

    for timestamp in itertools.count(start=notes.time):
        for bus in bus_numbers:
            if timestamp % bus == 0:
                return (timestamp - notes.time, bus)

    raise AssertionError


NOTES = get_notes(get_input())
NEXT_BUS = get_next_bus(NOTES)

print(NEXT_BUS[0] * NEXT_BUS[1])


# Functions from Rosetta


def chinese_remainder(n: Sequence[int], a: Sequence[int]) -> int:
    # pylint: disable=invalid-name
    total = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        total += a_i * mul_inv(p, n_i) * p
    return total % prod


def mul_inv(a: int, b: int) -> int:
    # pylint: disable=invalid-name
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        quotient = a // b
        a, b = b, a % b
        x0, x1 = x1 - quotient * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


remainders, moduli = zip(*NOTES.get_bus_offsets())
print(chinese_remainder(moduli, remainders))
