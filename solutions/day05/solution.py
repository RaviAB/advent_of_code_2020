import functools
import itertools
import math
import operator
from typing import Iterable, Tuple


def get_input() -> Iterable[str]:
    with open("input.txt") as file_handle:
        yield from file_handle.read().splitlines()


def lower_bound(lower: int, upper: int) -> Tuple[int, int]:
    return (lower, (upper + lower) // 2)


def upper_bound(lower: int, upper: int) -> Tuple[int, int]:
    return (math.ceil((upper + lower) / 2), upper)


def get_seat_id(row: int, col: int) -> int:
    return row * 8 + col


TRANSITIONS = {
    "F": lower_bound,
    "B": upper_bound,
    "R": upper_bound,
    "L": lower_bound,
}


def process_string(initial_bounds: Tuple[int, int], transitions: str) -> int:
    for transition in transitions:
        initial_bounds = TRANSITIONS[transition](*initial_bounds)

    assert initial_bounds[0] == initial_bounds[1]
    return initial_bounds[0]


seating_positions = (
    (process_string((0, 127), input_str[:-3]), process_string((0, 7), input_str[-3:]),)
    for input_str in get_input()
)

seat_ids = [get_seat_id(*seat) for seat in seating_positions]

print(max(seat_ids))

print(
    functools.reduce(
        operator.xor, itertools.chain(seat_ids, range(min(seat_ids), max(seat_ids) + 1))
    )
)
