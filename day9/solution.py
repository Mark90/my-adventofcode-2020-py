from collections import defaultdict


def update(preamble_sums, numbers, preamble_len, position):
    # An 'old' number leaves and a 'new' number joins the preamble.
    # Decrement sums made with the old number, and increment those made with the new.
    old_num = numbers[position - preamble_len]
    new_num = numbers[position]
    for number in numbers[position - preamble_len + 1 : position]:
        preamble_sums[old_num + number] = max(0, preamble_sums[old_num + number] - 1)
        preamble_sums[new_num + number] += 1


def part1(lines, full, preamble_len=25):
    # 23278925
    numbers = list(map(int, lines))
    preamble_sums = defaultdict(int)
    for ia, a in enumerate(numbers[:preamble_len]):
        for ib, b in enumerate(numbers[:preamble_len]):
            if ia == ib:
                continue
            preamble_sums[a + b] += 1

    # Check the first number after the preamble (just in case)
    position = preamble_len
    while position < len(numbers):
        if preamble_sums[numbers[position]] == 0:
            return numbers[position]
        update(preamble_sums, numbers, preamble_len, position)
        position += 1
    return


def part2(lines, full):
    # 4011064
    weakness = part1(lines, full)
    nums = list(map(int, lines))
    a, b = 0, 2
    while True:
        s = sum(nums[a:b])
        if s == weakness:
            return min(nums[a:b]) + max(nums[a:b])
        if s > weakness:
            a += 1
            b = a + 2
            continue
        b += 1
    return
