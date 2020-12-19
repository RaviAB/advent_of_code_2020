from typing import Iterable, Sequence, Tuple

TEST_INPUT = """\
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
"""


def get_input() -> Iterable[str]:
    with open("input.txt") as file_handle:
        yield from file_handle.read().splitlines()


def get_test_input() -> Iterable[str]:
    return iter(TEST_INPUT.splitlines())


def get_input_sequence(input_lines: Iterable[str]) -> Sequence[int]:
    return [int(line) for line in input_lines]


def check_sum(test_sum: int, candidates: Sequence[int]) -> bool:
    candidate_set = set(candidates)

    return any((test_sum - candidate) in candidate_set for candidate in candidates)


def get_incorrect_value(input_sequence: Sequence[int], window_size) -> int:
    for index, number in enumerate(input_sequence[window_size:]):
        if not check_sum(number, input_sequence[index : (index + window_size)]):
            return number

    raise AssertionError


def get_contiguous_numbers(test_sum, input_sequence: Sequence[int]) -> Tuple[int, int]:
    for start_index in range(len(input_sequence)):
        for end_index in range(start_index, len(input_sequence)):
            current_slice = input_sequence[start_index : end_index + 1]
            current_sum = sum(current_slice)

            if current_sum > test_sum:
                break
            if current_sum == test_sum and start_index == end_index:
                break
            if current_sum == test_sum:
                return min(current_slice), max(current_slice)

    raise AssertionError


def get_contiguous_numbers_imperative(
    test_sum, input_sequence: Sequence[int]
) -> Tuple[int, int]:
    start_index = 0
    end_index = 0
    current_sum = sum(input_sequence[start_index : end_index + 1])

    while True:
        if current_sum > test_sum:
            current_sum -= input_sequence[start_index]
            start_index += 1
        elif current_sum < test_sum:
            end_index += 1
            current_sum += input_sequence[end_index]
        elif current_sum == test_sum:
            if start_index == end_index:
                current_sum -= input_sequence[start_index]
                start_index += 1
            else:
                current_slice = input_sequence[start_index : end_index + 1]
                return min(current_slice), max(current_slice)


INPUT_SEQUENCE = get_input_sequence(get_input())
INCORRECT_VALUE = get_incorrect_value(INPUT_SEQUENCE, 25)

print(sum(get_contiguous_numbers_imperative(INCORRECT_VALUE, INPUT_SEQUENCE)))
