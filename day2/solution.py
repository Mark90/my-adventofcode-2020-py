def part1(lines):
    valid = 0
    for line in lines:
        policy, password = line.split(":")
        minmax, char = policy.split()
        cmin, cmax = list(map(int, minmax.split("-")))
        valid += cmin <= password.count(char) <= cmax
    print(f"[part1] Valid passwords: {valid}")


def part2(lines):
    valid = 0
    for line in lines:
        policy, password = line.split(":")
        password = password.strip()
        minmax, char = policy.split()
        pos1, pos2 = list(map(int, minmax.split("-")))
        valid += (password[pos1 - 1] == char) ^ (password[pos2 - 1] == char)
    print(f"[part2] Valid passwords: {valid}")
