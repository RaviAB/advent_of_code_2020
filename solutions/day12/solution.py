from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum, unique
from functools import reduce, singledispatch
from typing import Dict, Iterable, Tuple, Union

INSTRUCTION_PATTERN = r"([A-Z])([0-9]+)"

TEST_INPUT = """\
F10
N3
F7
R90
F11
"""


class Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"

    NONE = None


@unique
class Action(Enum):
    LEFT = "L"
    RIGHT = "R"
    FORWARD = "F"


Operation = Union[Direction, Action]


@dataclass
class Instruction:
    operation: Operation
    magnitude: int


@dataclass
class State:
    direction: Direction
    position: Tuple[int, int]

    def __str__(self):
        return f"{self.direction} {self.position}"


MOVEMENT_ORDERING = [
    Direction.NORTH,
    Direction.EAST,
    Direction.SOUTH,
    Direction.WEST,
]

MOVEMENT_MAPPING: Dict[Direction, Tuple[int, int]] = {
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, -1),
    Direction.WEST: (-1, 0),
    Direction.NORTH: (0, 1),
}


def scale_tuple(initial_tuple: Tuple[int, int], scale: int) -> Tuple[int, int]:
    return (initial_tuple[0] * scale, initial_tuple[1] * scale)


def add_tuples(tuple1: Tuple[int, int], tuple2: Tuple[int, int]) -> Tuple[int, int]:
    return (tuple1[0] + tuple2[0], tuple1[1] + tuple2[1])


def get_input() -> Iterable[str]:
    with open("input.txt") as file_handle:
        yield from file_handle.read().splitlines()


def get_test_input() -> Iterable[str]:
    return iter(TEST_INPUT.splitlines())


def get_operation(operation_str: str) -> Operation:
    try:
        return Action(operation_str)
    except ValueError:
        return Direction(operation_str)


def get_instructions(input_lines: Iterable[str]) -> Iterable[Instruction]:
    for line in input_lines:
        if match := re.match(INSTRUCTION_PATTERN, line):
            operation_str, magnitude = match.groups()
            yield Instruction(get_operation(operation_str), int(magnitude))
        else:
            raise AssertionError(f"Cannot match line: '{line}'")


@singledispatch
def do_operation(
    _operation: Operation, _magnitude: int, _initial_state: State
) -> State:
    pass


@do_operation.register
def do_direction(direction: Direction, magnitude: int, initial_state: State) -> State:
    movement_vector = MOVEMENT_MAPPING[direction]
    displacement_vector = (
        magnitude * movement_vector[0],
        magnitude * movement_vector[1],
    )

    return State(
        initial_state.direction,
        (
            initial_state.position[0] + displacement_vector[0],
            initial_state.position[1] + displacement_vector[1],
        ),
    )


@do_operation.register
def do_action(action: Action, magnitude: int, initial_state: State) -> State:
    if action == Action.FORWARD:
        movement_vector = MOVEMENT_MAPPING[initial_state.direction]
        displacement_vector = (
            magnitude * movement_vector[0],
            magnitude * movement_vector[1],
        )

        return State(
            initial_state.direction,
            (
                initial_state.position[0] + displacement_vector[0],
                initial_state.position[1] + displacement_vector[1],
            ),
        )
    if action in (action.LEFT, action.RIGHT):
        rotation_direction = 1 if action == action.RIGHT else -1
        current_direction_index = MOVEMENT_ORDERING.index(initial_state.direction)
        new_direction_index = (
            current_direction_index + (magnitude // 90) * rotation_direction
        ) % len(MOVEMENT_ORDERING)

        return State(MOVEMENT_ORDERING[new_direction_index], initial_state.position)

    raise AssertionError


def _do_operation(initial_state: State, instruction: Instruction) -> State:
    state = do_operation(instruction.operation, instruction.magnitude, initial_state)
    return state


def get_final_state(initial_state: State, instructions: Iterable[Instruction]) -> State:
    return reduce(_do_operation, instructions, initial_state)


INITIAL_STATE = State(Direction.EAST, (0, 0))
INSTRUCTIONS = get_instructions(get_input())
FINAL_STATE = get_final_state(INITIAL_STATE, INSTRUCTIONS)

print(FINAL_STATE)
print(abs(FINAL_STATE.position[0]) + abs(FINAL_STATE.position[1]))
print()


@dataclass
class States:
    boat_state: State
    wp_state: State


@singledispatch
def do_operation_wp(_operation: Operation, _magnitude: int, _states: States) -> States:
    pass


@do_operation_wp.register
def do_direction_wp(direction: Direction, magnitude: int, states: States) -> States:
    movement_vector = MOVEMENT_MAPPING[direction]
    displacement_vector = scale_tuple(movement_vector, magnitude)
    new_wp_state = State(
        states.wp_state.direction,
        add_tuples(states.wp_state.position, displacement_vector),
    )

    return States(states.boat_state, new_wp_state)


@do_operation_wp.register
def do_action_wp(action: Action, magnitude: int, states: States) -> States:
    if action == Action.FORWARD:
        boat_displacement = scale_tuple(states.wp_state.position, magnitude)
        new_boat_state = State(
            states.boat_state.direction,
            add_tuples(states.boat_state.position, boat_displacement),
        )

        return States(new_boat_state, states.wp_state)

    if action in (action.LEFT, action.RIGHT):
        rotation_functions = [
            lambda x, y: (x, y),
            lambda x, y: (y, -x),
            lambda x, y: (-x, -y),
            lambda x, y: (-y, x),
        ]

        rotation_direction = 1 if action == action.RIGHT else -1
        rotation_index = ((magnitude // 90) * rotation_direction) % len(
            rotation_functions
        )

        new_wp_state = State(
            states.wp_state.direction,
            rotation_functions[rotation_index](*states.wp_state.position),
        )

        return States(states.boat_state, new_wp_state)

    raise AssertionError


def _do_operation_wp(states: States, instruction: Instruction) -> States:
    return do_operation_wp(instruction.operation, instruction.magnitude, states)


def get_final_state_wp(
    initial_states: States, instructions: Iterable[Instruction]
) -> States:
    return reduce(_do_operation_wp, instructions, initial_states)


INSTRUCTIONS = get_instructions(get_input())
INITIAL_STATE = State(Direction.NONE, (0, 0))
INITIAL_WP_STATE = State(Direction.NONE, (10, 1))
FINAL_BOAT_STATES = get_final_state_wp(
    States(INITIAL_STATE, INITIAL_WP_STATE), INSTRUCTIONS
)

print(FINAL_BOAT_STATES)
print(
    abs(FINAL_BOAT_STATES.boat_state.position[0])
    + abs(FINAL_BOAT_STATES.boat_state.position[1])
)
