from collections import defaultdict


def pupdate(p, nums, preamble, i):
    # delete the first number before the preamble
    # add the new one
    todel = nums[i - preamble - 1]
    toadd = nums[i]
    for b in nums[i - preamble : i]:
        p[todel + b] = max(0, p[todel + b] - 1)
        p[toadd + b] += 1


def part1(lines, full, preamble=25):
    # 23278925
    nums = list(map(int, lines))
    p = defaultdict(int)
    for ia, a in enumerate(nums[:preamble]):
        for ib, b in enumerate(nums[:preamble]):
            if ia == ib:
                continue
            p[a + b] += 1

    # main loop
    i = preamble
    if p[nums[i]] == 0:
        return nums[i]

    pupdate(p, nums, preamble, i)
    i += 1
    while i < len(nums):
        pupdate(p, nums, preamble, i)
        if p[nums[i]] == 0:
            return nums[i]
        i += 1
    return


def part2(lines, full):
    # 4011064
    n = part1(lines, full)
    nums = list(map(int, lines))
    a, b = 0, 2
    s = sum(nums[a:b])
    a = 0

    b = 2
    while True:
        s = sum(nums[a:b])
        if s == n:
            return min(nums[a:b]) + max(nums[a:b])
        if s > n:
            a += 1
            b = a + 2
            continue
        b += 1

    return
