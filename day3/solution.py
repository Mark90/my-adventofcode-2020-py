def part1(lines):
    x = trees = 0
    for line in [i.strip() for i in lines]:
        trees += line[x] == "#"
        x = (x + 3) % len(line)
    print(f"[part1] Trees: {trees}")


from itertools import islice
from functools import reduce


def findmesometrees(lines, slopex, slopey):
    x = trees = 0
    for line in islice((i.strip() for i in lines), None, None, slopey):
        trees += line[x] == "#"
        x = (x + slopex) % len(line)
    return trees


def part2(lines):
    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
    all_trees = [findmesometrees(lines, *slope) for slope in slopes]
    # print(all_trees)
    print("[part2] Result:", reduce(lambda x, y: x * y, all_trees))
