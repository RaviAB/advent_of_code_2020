import itertools
from collections import Counter
from enum import Enum, unique
from functools import partial
from typing import Callable, Dict, Iterable, Tuple

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


Position = Tuple[int, int]
Board = Dict[Position, State]
Neighbors = Iterable[Position]
GetNeighborsFunc = Callable[[int, int, Board], Neighbors]


def get_input() -> Iterable[str]:
    with open("input.txt") as file_handle:
        yield from file_handle.read().splitlines()


def get_test_input() -> Iterable[str]:
    return iter(TEST_INPUT.splitlines())


def get_board(input_lines: Iterable[str]) -> Board:
    return {
        (row, col): State(character)
        for row, line in enumerate(input_lines)
        for col, character in enumerate(line)
    }


def get_neighbors(row: int, col: int, _: Board) -> Neighbors:
    return (
        (row + row_offset, col + col_offset)
        for row_offset in (-1, 0, 1)
        for col_offset in (-1, 0, 1)
        if not (row_offset == col_offset == 0)
    )


def get_positions(
    initial_position: Position, movement_vector: Position
) -> Iterable[Position]:
    for index in itertools.count(start=1):
        yield (
            initial_position[0] + (movement_vector[0] * index),
            initial_position[1] + (movement_vector[1] * index),
        )


def get_first_seat(
    initial_position: Position, movement_vector: Position, board: Board
) -> Position:
    for position in get_positions(initial_position, movement_vector):
        if position not in board:
            return position
        if board[position] != State.FLOOR:
            return position

    raise AssertionError


def get_visible_neighbors(row: int, col: int, board: Board) -> Neighbors:
    for row_offset in (-1, 0, 1):
        for col_offset in (-1, 0, 1):
            if not row_offset == col_offset == 0:
                yield get_first_seat((row, col), (row_offset, col_offset), board)


def is_alive(row: int, col: int, board: Board) -> bool:
    return board.get((row, col), State.FLOOR) == State.FULL


def get_new_state(
    row: int,
    col: int,
    board: Board,
    threshold: int,
    get_neighbors_func: GetNeighborsFunc,
) -> State:
    current_state = board[(row, col)]
    alive_neighbors_count = sum(
        is_alive(row, col, board) for row, col in get_neighbors_func(row, col, board)
    )

    if current_state == State.EMPTY and alive_neighbors_count == 0:
        return State.FULL
    if current_state == State.FULL and alive_neighbors_count >= threshold:
        return State.EMPTY

    return current_state


def get_new_board(
    board: Board, state_transition_func: Callable[[int, int, Board], State]
) -> Board:
    return {
        position: state_transition_func(*position, board) for position in board.keys()
    }


def get_final_board(initial_board: Board, state_transition_func) -> Board:
    old_board = initial_board
    new_board = initial_board

    while (new_board := get_new_board(new_board, state_transition_func)) != old_board:
        old_board = new_board

    return new_board


INITIAL_BOARD = get_board(get_input())
FINAL_BOARD = get_final_board(
    INITIAL_BOARD,
    partial(get_new_state, threshold=4, get_neighbors_func=get_neighbors),
)

FINAL_ALIVE = Counter(FINAL_BOARD.values())
print(FINAL_ALIVE[State.FULL])

FINAL_BOARD2 = get_final_board(
    INITIAL_BOARD,
    partial(get_new_state, threshold=5, get_neighbors_func=get_visible_neighbors),
)

FINAL_ALIVE2 = Counter(FINAL_BOARD2.values())
print(FINAL_ALIVE2[State.FULL])
