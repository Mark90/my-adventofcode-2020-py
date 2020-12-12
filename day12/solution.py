def part1(lines, full):
    # 415
    r = 90  # rotated towards east (N 0, S 180, W 270)
    x = 0  # negative is W positive is E
    y = 0  # negative is S positive is N

    move = {
        "N": lambda x, y, v: (x, y + v),
        "S": lambda x, y, v: (x, y - v),
        "W": lambda x, y, v: (x - v, y),
        "E": lambda x, y, v: (x + v, y),
    }
    move[0] = move["N"]
    move[180] = move["S"]
    move[270] = move["W"]
    move[90] = move["E"]
    for l in lines:
        action, value = l[0], int(l[1:])
        if action == "L":
            r = r - value
        if action == "R":
            r = r + value
        r = (r + 360) % 360
        if action == "F":
            x, y = move[r](x, y, value)
        if action in "NSWE":
            x, y = move[action](x, y, value)
    return abs(x) + abs(y)


def right(wx, wy, r):
    if r == 270:
        return left(wx, wy, 90)
    if r == 180:
        return -wx, -wy
    return wy, -wx


def left(wx, wy, r):
    if r == 270:
        return right(wx, wy, 90)
    if r == 180:
        return -wx, -wy
    return -wy, wx


def part2(lines, full):
    # 29401
    x = 0  # negative is W positive is E
    y = 0  # negative is S positive is N
    wx, wy = 10, 1
    move = {
        "N": lambda x, y, v: (x, y + v),
        "S": lambda x, y, v: (x, y - v),
        "W": lambda x, y, v: (x - v, y),
        "E": lambda x, y, v: (x + v, y),
    }
    for l in lines:
        action, value = l[0], int(l[1:])
        if action == "L":
            wx, wy = left(wx, wy, value)
        if action == "R":
            wx, wy = right(wx, wy, value)
        if action == "F":
            x = x + (wx * value)
            y = y + (wy * value)
        if action in "NSWE":
            wx, wy = move[action](wx, wy, value)
    return abs(x) + abs(y)
