def part1(lines, full):
    # 3000: 7 min
    adapters = sorted(list(map(int, lines)))
    d = {1: 0, 2: 0, 3: 1}
    prev = 0
    for a in adapters:
        d[a - prev] += 1
        prev = a
    print(d)
    return d[1] * d[3]


# Cumulative numbers used in calc_permutations()
powers_combined = {0: 0, 1: 0, 2: 0}
for i in range(3, 100):
    powers_combined[i] = 2 ** (i - 3) + powers_combined[i - 1]


def calc_permutations(successive_numbers):
    # Return the possible adapter permutations for successive numbers.
    # For 1 (pair of) successive numbers, return 1
    # for 2 pair, return 2
    # 3 -> 4     2**(3-1)                 ->  2**2      ->  4
    # 4 -> 7     2**(4-1)-2**0            ->  8 - 1     ->  7
    # 5 -> 13    2**(5-1)-2**0-2**1       ->  16-1-2    ->  13
    # 6 -> 25    2**(6-1)-2**0-2**1-2**2  ->  32-1-2-4  ->  25
    if successive_numbers == 0:
        return 1
    return 2 ** (successive_numbers - 1) - powers_combined[successive_numbers - 1]


def part2(lines, full):
    # 193434623148032
    adapters = [0] + sorted(list(map(int, lines)))

    permutations = 1
    successive_numbers = 0
    i = 0
    while i + 1 < len(adapters):
        if adapters[i + 1] - adapters[i] == 3:
            # Difference with next adapter is 3, cannot skip this one.
            permutations *= calc_permutations(successive_numbers)
            successive_numbers = 0
        else:
            # Difference with next adapter is 1, this one could be skipped
            # if there are enough successive numbers.
            successive_numbers += 1
        i += 1
    permutations *= calc_permutations(successive_numbers)
    return permutations
