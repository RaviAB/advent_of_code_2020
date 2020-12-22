import itertools
import operator
import re
from dataclasses import dataclass, field
from functools import reduce
from typing import Dict, Iterable, Sequence, Tuple, TypeVar

MEMORY_PATTERN = r"mem\[([0-9]+)\] = ([0-9]+)"

TEST_INPUT = """\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""


T = TypeVar("T")  # pylint: disable=invalid-name


def powerset(sequence: Sequence[T]) -> Iterable[Sequence[T]]:
    for combination_len in range(len(sequence) + 1):
        for combination in itertools.combinations(sequence, combination_len):
            yield combination


@dataclass
class Mask:
    on_bitmask: int
    off_bitmask: int
    floating_bits: Sequence[int]
    masks: Sequence[Tuple[int, int]] = field(init=False)

    def __post_init__(self):
        empty_floating_bits = reduce(operator.xor, self.floating_bits, 0xFFFFFFFFF)

        self.masks = [
            (
                reduce(operator.or_, combination, empty_floating_bits),
                reduce(operator.or_, combination, 0),
            )
            for combination in powerset(self.floating_bits)
        ]


def get_input() -> Iterable[str]:
    with open("input.txt") as file_handle:
        yield from file_handle.read().splitlines()


def get_test_input() -> Iterable[str]:
    return iter(TEST_INPUT.splitlines())


def str_to_mask(mask_string: str) -> Mask:
    on_bitmask = 0
    off_bitmask = 0xFFFFFFFFF
    floating_bits = []

    for index, bit in enumerate(reversed(mask_string)):
        if bit == "1":
            on_bitmask |= 1 << index
        elif bit == "0":
            off_bitmask ^= 1 << index
        elif bit == "X":
            floating_bits.append(1 << index)

    return Mask(on_bitmask, off_bitmask, floating_bits)


def get_mask(current_line: str, current_mask: Mask) -> Mask:
    if current_line.startswith("mask"):
        return str_to_mask(current_line.split(" ")[-1])

    return current_mask


def get_memory_dict(input_lines: Iterable[str], current_mask: Mask) -> Dict[int, int]:
    memory_values: Dict[int, int] = {}

    for input_line in input_lines:
        current_mask = get_mask(input_line, current_mask)

        if match := re.match(MEMORY_PATTERN, input_line):
            location, bits = match.groups()

            memory_values[int(location)] = (
                int(bits) | current_mask.on_bitmask
            ) & current_mask.off_bitmask

    return memory_values


INITIAL_MASK = Mask(0, 0xFFFFFFFFF, tuple())
MEMORY_DICT = get_memory_dict(get_test_input(), INITIAL_MASK)
print(sum(MEMORY_DICT.values()))


def get_memory_dict_part2(
    input_lines: Iterable[str], current_mask: Mask
) -> Dict[int, int]:
    memory_values: Dict[int, int] = {}

    for input_line in input_lines:
        current_mask = get_mask(input_line, current_mask)

        if match := re.match(MEMORY_PATTERN, input_line):
            location, bits = match.groups()
            on_bits_location = int(location) | current_mask.on_bitmask

            for mask_and, mask_or in current_mask.masks:
                memory_values[(on_bits_location & mask_and) | mask_or] = int(bits)

    return memory_values


MEMORY_DICT = get_memory_dict_part2(get_input(), INITIAL_MASK)
print(sum(MEMORY_DICT.values()))
