from collections import Counter
from typing import Iterable, Sequence

TEST_INPUT = """\
16
10
15
5
1
11
7
19
6
12
4
"""


def get_input() -> Iterable[str]:
    with open("input.txt") as file_handle:
        yield from file_handle.read().splitlines()


def get_test_input() -> Iterable[str]:
    return iter(TEST_INPUT.splitlines())


def get_sorted_input(input_lines: Iterable[str]) -> Sequence[int]:
    return [0] + sorted(int(line) for line in input_lines)


def get_first_differences(sorted_int: Sequence[int]) -> Iterable[int]:
    for second_value, first_value in zip(sorted_int[1:], sorted_int[:-1]):
        yield second_value - first_value


def get_permutations(sorted_int: Sequence[int]) -> int:
    permutations = [0] * (max(sorted_int) + 1)
    permutations[0] = 1

    for index in sorted_int:
        lower_bound = max(index - 3, 0)
        permutations[index] += sum(permutations[lower_bound:index])

    return permutations[-1]


ADAPTERS = get_sorted_input(get_input())
COUNT = Counter(get_first_differences(ADAPTERS))

print(COUNT[1] * (COUNT[3] + 1))
print(get_permutations(ADAPTERS))
