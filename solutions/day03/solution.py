import functools
import operator
from typing import Iterable, Tuple


def get_input():
    with open("input.txt") as file_handle:
        return file_handle.read().splitlines()


lines = get_input()


def get_positions(
    rows: int, cols: int, down: int, right: int
) -> Iterable[Tuple[int, int]]:
    for iteration, row in enumerate(range(0, rows, down)):
        yield row, (iteration * right) % cols


def get_tree_count(down: int, right: int) -> int:
    return sum(
        1
        for row, col in get_positions(len(lines), len(lines[0]), down, right)
        if lines[row][col] == "#"
    )


print(get_tree_count(1, 3))

inputs = (
    (1, 1),
    (1, 3),
    (1, 5),
    (1, 7),
    (2, 1),
)

print(functools.reduce(operator.mul, (get_tree_count(*pair) for pair in inputs)))
