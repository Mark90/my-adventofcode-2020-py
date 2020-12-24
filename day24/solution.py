import re

from collections import defaultdict, Counter


rgx = re.compile("(e|se|sw|w|nw|ne)")


def make_grid(lines, width):
    grid = {}
    for line in lines:
        coord = (width // 2) * (width // 2)  # refence tile in the middle
        for d in rgx.findall(line):
            if d == "e":
                coord += 2
            if d == "se":
                coord += width + 1
            if d == "sw":
                coord += width - 1
            if d == "w":
                coord -= 2
            if d == "nw":
                coord -= width + 1
            if d == "ne":
                coord -= width - 1
        grid.setdefault(coord, True)
        grid[coord] ^= True
    return grid


def part1(lines, full):
    # 375
    width = height = 1000
    grid = make_grid(lines, width)
    return sum(1 for v in grid.values() if v == False)


def part2(lines, full, days=100):
    # 3937
    # Determine the required gridsize based on input
    longest_instruction = max(len(rgx.findall(line)) for line in lines)
    longest_path = (days + longest_instruction) * 2
    width = height = longest_path * 2  # Path could go left or right
    grid = make_grid(lines, width)
    for _ in range(days):
        next_grid = grid.copy()
        # Could probably improve further by keeping track of the lowest
        # and highest coordinate, but eh.
        for coord in range(width, (width * height) + 1 - width):
            adjacent_white = (
                grid.get(coord + 2, 1)  # East
                + grid.get(coord + (width + 1), 1)  # Southeast
                + grid.get(coord + (width - 1), 1)  # Southwest
                + grid.get(coord - 2, 1)  # West
                + grid.get(coord - (width + 1), 1)  # Northwest
                + grid.get(coord - (width - 1), 1)  # Northeast
            )
            if grid.setdefault(coord, True):
                if adjacent_white == 4:
                    next_grid[coord] = False  # white to black
            elif adjacent_white != 4 and adjacent_white != 5:
                next_grid[coord] = True  # black to white
        grid = next_grid
    return sum(1 for v in grid.values() if v == False)
