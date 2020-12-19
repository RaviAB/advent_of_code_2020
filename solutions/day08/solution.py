from dataclasses import dataclass
from enum import Enum, unique
from typing import Callable, Dict, Iterable, Sequence, Set, Union

HOLDER_PATTERN = r"^([a-z]+ [a-z]+)"
CONTENTS_PATTERN = r"([0-9]+) ([a-z]+ [a-z]+) bag"

TEST_INPUT = """\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""


@unique
class Operation(Enum):
    NOP = "nop"
    ACC = "acc"
    JMP = "jmp"


@dataclass
class Instruction:
    operation: Operation
    count: int


@dataclass
class State:
    instruction_ptr: int
    current_accumulator: int
    instructions: Sequence[Instruction]

    def __str__(self):
        return f"Ptr: {self.instruction_ptr} Acc: {self.current_accumulator}"


def get_input() -> Iterable[str]:
    with open("input.txt") as file_handle:
        yield from file_handle.read().splitlines()


def get_test_input() -> Iterable[str]:
    return iter(TEST_INPUT.splitlines())


def get_instructions(input_lines: Iterable[str]) -> Iterable[Instruction]:
    for line in input_lines:
        operation, val = line.split(" ")
        yield Instruction(Operation(operation), int(val))


def acc(count: int, state: State):
    return State(
        state.instruction_ptr + 1, state.current_accumulator + count, state.instructions
    )


def nop(_: int, state: State) -> State:
    return State(
        state.instruction_ptr + 1, state.current_accumulator, state.instructions
    )


def jmp(count: int, state: State) -> State:
    return State(
        state.instruction_ptr + count, state.current_accumulator, state.instructions
    )


JUMP_TABLE: Dict[Operation, Callable[[int, State], State]] = {
    Operation.NOP: nop,
    Operation.ACC: acc,
    Operation.JMP: jmp,
}

FLIP_OPERATION: Dict[Operation, Operation] = {
    Operation.NOP: Operation.JMP,
    Operation.JMP: Operation.NOP,
}


def next_state(current_state: State) -> State:
    current_instruction = current_state.instructions[current_state.instruction_ptr]

    return JUMP_TABLE[current_instruction.operation](
        current_instruction.count, current_state
    )


def get_last_state(current_state: State, visited: Set[int]) -> State:
    if current_state.instruction_ptr in visited:
        return current_state

    return get_last_state(
        next_state(current_state), visited.union({current_state.instruction_ptr})
    )


def terminates(current_state: State, visited: Set[int]) -> Union[int, None]:
    instruction_length = len(current_state.instructions)
    if current_state.instruction_ptr in visited:
        return None
    if current_state.instruction_ptr > instruction_length:
        return None
    if current_state.instruction_ptr == instruction_length:
        return current_state.current_accumulator

    return terminates(
        next_state(current_state), visited.union({current_state.instruction_ptr})
    )


INSTRUCTIONS = list(get_instructions(get_input()))
START_STATE = State(0, 0, INSTRUCTIONS)

print(get_last_state(START_STATE, set()))

assert terminates(START_STATE, set()) is None
assert terminates(State(len(INSTRUCTIONS) + 1, 0, INSTRUCTIONS), set()) is None
assert terminates(State(len(INSTRUCTIONS), 0, INSTRUCTIONS), set()) is not None


def toggle(
    target_index: int, instructions: Iterable[Instruction]
) -> Iterable[Instruction]:
    for index, instruction in enumerate(instructions):
        if index == target_index:
            yield Instruction(FLIP_OPERATION[instruction.operation], instruction.count)
        else:
            yield instruction


def get_terminating_accumulator(starting_instructions: Sequence[Instruction]) -> int:
    for index, instruction in enumerate(starting_instructions):
        if instruction.operation == Operation.ACC:
            continue

        return_value = terminates(
            State(0, 0, list(toggle(index, starting_instructions))), set()
        )

        if return_value is not None:
            return return_value

    raise AssertionError


print(get_terminating_accumulator(INSTRUCTIONS))
