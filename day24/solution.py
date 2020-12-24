import re

from collections import defaultdict, Counter


def part1(lines, full):
    # 375
    w = h = 1000
    # g = list(True for _ in range(h * w))
    g = {}
    rgx = re.compile("(e|se|sw|w|nw|ne)")
    for line in lines:
        coord = 500 * 500  # just somewhere in the middle
        for d in rgx.findall(line):
            if d == "e":
                coord += 2
            if d == "se":
                coord += w + 1
            if d == "sw":
                coord += w - 1
            if d == "w":
                coord -= 2
            if d == "nw":
                coord -= w + 1
            if d == "ne":
                coord -= w - 1
        g.setdefault(coord, True)
        g[coord] ^= True
    return sum(1 for v in g.values() if v == False)
    # return (w * h) - sum(g)


def part2(lines, full, days=100):
    # 3937
    w = h = 1000
    # g = list(True for _ in range(h * w))
    g = {}
    rgx = re.compile("(e|se|sw|w|nw|ne)")
    for line in lines:
        coord = 500 * 500  # just somewhere in the middle
        for d in rgx.findall(line):
            if d == "e":
                coord += 2
            if d == "se":
                coord += w + 1
            if d == "sw":
                coord += w - 1
            if d == "w":
                coord -= 2
            if d == "nw":
                coord -= w + 1
            if d == "ne":
                coord -= w - 1
        g.setdefault(coord, True)
        g[coord] ^= True

    # print(f"Day 0: {(w * h) - sum(g)}")
    print(f"Day 0: {sum(1 for v in g.values() if v==False)}")
    for day in range(days):
        gnew = g.copy()
        # for coord in range(w, (w*h) - w):
        for coord in range(0, (w * h) + 1):
            # if (coord%w) <= 2 or (w- (coord%w)) <= 2: continue
            vals = sum(
                g.get(x, True)
                for x in (
                    coord + 2,  # e
                    coord + (w + 1),  # se
                    coord + (w - 1),  # sw
                    coord - 2,  # w
                    coord - (w + 1),  # nw
                    coord - (w - 1),  # ne
                )
            )
            # True -> white, False -> black
            g.setdefault(coord, True)
            if g[coord] and vals == 4:
                gnew[coord] = False
            if not g[coord] and vals != 4 and vals != 5:
                gnew[coord] = True
        g = gnew
        # print(f"Day {day+1}: {(w * h) - sum(g)}")
        print(f"Day {day+1}: {sum(1 for v in g.values() if v==False)}")
    return sum(1 for v in g.values() if v == False)
