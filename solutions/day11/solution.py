from collections import Counter
from enum import Enum, unique
from functools import partial
from typing import Iterable, Sequence, Tuple

TEST_INPUT = """\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""


@unique
class State(Enum):
    FLOOR = "."
    FULL = "#"
    EMPTY = "L"


Board = Sequence[Sequence[State]]


def get_input() -> Iterable[str]:
    with open("input.txt") as file_handle:
        yield from file_handle.read().splitlines()


def get_test_input() -> Iterable[str]:
    return iter(TEST_INPUT.splitlines())


def get_board(input_lines: Iterable[str]) -> Board:
    return [[State(character) for character in list(line)] for line in input_lines]


def get_neighbors(row: int, col: int) -> Iterable[Tuple[int, int]]:
    return (
        (row + row_offset, col + col_offset)
        for row_offset in (-1, 0, 1)
        for col_offset in (-1, 0, 1)
        if not (row_offset == col_offset == 0)
    )


def is_alive(row: int, col: int, board: Board) -> bool:
    num_rows = len(board)
    num_cols = len(board[0])

    return 0 <= row < num_rows and 0 <= col < num_cols and board[row][col] == State.FULL


def get_alive_neighbors_count(row: int, col: int, board: Board) -> int:
    return sum(is_alive(row, col, board) for row, col in get_neighbors(row, col))


def get_alive_visible_count(row: int, col: int, board: Board) -> int:
    return sum(is_alive(row, col, board) for row, col in get_neighbors(row, col))


def get_new_state(
    row: int, col: int, board: Board, threshold: int, alive_neighbor_func
) -> State:
    current_state = board[row][col]
    alive_neighbors_count = alive_neighbor_func(row, col, board)
    if current_state == State.EMPTY and alive_neighbors_count == 0:
        return State.FULL
    if current_state == State.FULL and alive_neighbors_count >= threshold:
        return State.EMPTY

    return current_state


def get_new_board(board: Board, state_transition_func) -> Board:
    return [
        [state_transition_func(row, col, board) for col in range(len(board[row]))]
        for row in range(len(board))
    ]


def get_final_board(initial_board: Board, state_transition_func) -> Board:
    old_board = initial_board
    new_board = initial_board

    while True:
        new_board, old_board = (
            get_new_board(new_board, state_transition_func),
            new_board,
        )

        if new_board == old_board:
            return new_board


INITIAL_BOARD = get_board(get_input())
FINAL_BOARD = get_final_board(
    INITIAL_BOARD,
    partial(get_new_state, threshold=4, alive_neighbor_func=get_alive_neighbors_count),
)

FINAL_ALIVE = Counter(state for row in FINAL_BOARD for state in row)

print(FINAL_ALIVE)
