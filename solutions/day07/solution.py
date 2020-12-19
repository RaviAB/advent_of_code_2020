import functools
import itertools
import re
from dataclasses import dataclass
from typing import Dict, Iterable, Sequence, Tuple

HOLDER_PATTERN = r"^([a-z]+ [a-z]+)"
CONTENTS_PATTERN = r"([0-9]+) ([a-z]+ [a-z]+) bag"

TEST_INPUT = """\
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""


TEST_INPUT2 = """\
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
"""


@dataclass
class Contents:
    count: int
    name: str

    def __hash__(self):
        return hash(str(self.count) + self.name)


BagsToContents = Iterable[Tuple[str, Sequence[Contents]]]


def get_input() -> Iterable[str]:
    with open("input.txt") as file_handle:
        yield from file_handle.read().splitlines()


def get_test_input() -> Iterable[str]:
    return iter(TEST_INPUT.splitlines())


def get_test_input2() -> Iterable[str]:
    return iter(TEST_INPUT2.splitlines())


def get_contents(input_line: str) -> Iterable[Contents]:
    for match in re.finditer(CONTENTS_PATTERN, input_line):
        number, bag_type = match.groups()
        yield Contents(int(number), bag_type)


def get_holder(input_line: str) -> str:
    if match := re.match(HOLDER_PATTERN, input_line):
        return match.group(1)

    raise Exception(f"No match for {input_line}")


def get_bags_to_contents(input_lines: Iterable[str]) -> BagsToContents:
    for line in input_lines:
        yield get_holder(line), tuple(get_contents(line))


def get_parent_bags(bags_to_contents: BagsToContents) -> Iterable[Tuple[str, str]]:
    for holder_name, contents in bags_to_contents:
        for bag in contents:
            yield bag.name, holder_name


def get_parent_bag_lookup(
    sorted_parent_bags: Iterable[Tuple[str, str]]
) -> Dict[str, Sequence[str]]:
    return {
        key: list(g[1] for g in group)
        for key, group in itertools.groupby(sorted_parent_bags, key=lambda x: x[0])
    }


def get_parents(
    parent_bags_lookup: Dict[str, Sequence[str]], current_bag: str
) -> Iterable[str]:
    yield from parent_bags_lookup[current_bag]

    for parent_bag in parent_bags_lookup[current_bag]:
        if parent_bag in parent_bags_lookup:
            yield from get_parents(parent_bags_lookup, parent_bag)


TARGET_BAG = "shiny gold"
BAGS_TO_CONTENTS = dict(get_bags_to_contents(get_test_input()))
PARENT_BAGS = get_parent_bags(BAGS_TO_CONTENTS.items())
PARENT_BAG_LOOKUP = get_parent_bag_lookup(sorted(PARENT_BAGS))

print(len(set(get_parents(PARENT_BAG_LOOKUP, TARGET_BAG))))


class HDict(dict):
    def __hash__(self):
        return hash(frozenset(self.items()))


# Hilariously, the cache actually slows this down substantially
@functools.lru_cache(maxsize=100, typed=False)
def get_bag_counts(bags_to_contents: Dict[str, Sequence[Contents]], current_bag):
    return 1 + sum(
        bag.count * get_bag_counts(bags_to_contents, bag.name)
        for bag in bags_to_contents[current_bag]
    )


BAGS_TO_CONTENTS2 = HDict(get_bags_to_contents(get_input()))
print(get_bag_counts(BAGS_TO_CONTENTS2, TARGET_BAG) - 1)
