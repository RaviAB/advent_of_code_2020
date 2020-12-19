def get_input():
    with open("input.txt") as file_handle:
        for num in file_handle.read().splitlines():
            yield int(num)


target = 2020


def part1(input_nums):
    seen = set()

    for num in input_nums:
        if target - num in seen:
            return num * (target - num)

        seen.add(num)

    return 0


print(part1(get_input()))


def part2(input_nums):
    sorted_nums = sorted(input_nums)

    for index, current in enumerate(sorted_nums):
        start_index = index
        end_index = len(sorted_nums) - 1
        goal = target - current

        while start_index != end_index:
            total = sorted_nums[start_index] + sorted_nums[end_index]

            if total > goal:
                end_index -= 1
            elif total < goal:
                start_index += 1
            else:
                return current * sorted_nums[start_index] * sorted_nums[end_index]


print(part2(get_input()))
