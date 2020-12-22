from collections import defaultdict, deque
from typing import Dict, MutableSequence, Sequence


def get_input() -> Sequence[int]:
    return (0, 14, 6, 20, 1, 4)


def get_test_input() -> Sequence[int]:
    return (0, 3, 6)


def get_final_number_spoken(input_sequence: Sequence[int], num_turns: int) -> int:
    last_spoken = input_sequence[-1]
    last_seen: Dict[int, MutableSequence[int]] = defaultdict(lambda: deque([], 2))

    for index, num in enumerate(input_sequence):
        last_seen[num].append(index + 1)

    for turn in range(len(input_sequence) + 1, num_turns + 1):
        if len(last_seen[last_spoken]) == 1:
            last_spoken = 0
        elif len(last_seen[last_spoken]) == 2:
            last_spoken = abs(last_seen[last_spoken][0] - last_seen[last_spoken][1])

        last_seen[last_spoken].append(turn)

    return last_spoken


print(get_final_number_spoken(get_input(), 2020))
print(get_final_number_spoken(get_input(), 30000000))
