from collections import defaultdict


def getneight(x, y, z):
    for ix in range(x - 1, x + 2):
        for iy in range(y - 1, y + 2):
            for iz in range(z - 1, z + 2):
                if ix == x and iy == y and iz == z:
                    continue
                yield ix, iy, iz


def update(cube, coord, nn):
    active = cube.setdefault(coord, 0)

    an = 0
    if active:  # active -> keep active for 2 or 3, else inactive
        for n in nn:
            an += cube.setdefault(n, 0)
            # if an > 3:
            # return 0
        return 2 <= an <= 3

    for n in nn:
        an += cube.setdefault(n, 0)
        # if an > 3:
        # return 0
    return an == 3


def part1(lines, full, cycles=6):
    # 293
    cube = defaultdict(int)
    neighbors = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            coord = x, y, 0
            cube[coord] = int(c == "#")
            neighbors[coord] = list(getneight(*coord))

    mmx = 0, len(lines[0]) - 1
    mmy = 0, len(lines) - 1
    mmz = 0, 0
    for cycle in range(cycles):
        mmx = mmx[0] - 1, mmx[1] + 1
        mmy = mmy[0] - 1, mmy[1] + 1
        mmz = mmz[0] - 1, mmz[1] + 1
        print(f"{mmx=} {mmy=} {mmz=}")
        print(f"before {cycle=} total {len(cube.keys())=} active {sum(cube.values())=}")
        newcube = cube.copy()
        for z in range(mmz[0], mmz[1] + 1):
            for y in range(mmy[0], mmy[1] + 1):
                for x in range(mmx[0], mmx[1] + 1):
                    coord = x, y, z
                    nn = neighbors.get(coord)
                    if not nn:
                        nn = list(getneight(*coord))
                        neighbors[coord] = nn
                    newcube[coord] = update(cube, coord, nn)
        cube = newcube

        print(f"after {cycle=} total {len(cube.keys())=} active {sum(cube.values())=}")
    return sum(cube.values())


def p2getneight(x, y, z, w):
    for ix in range(x - 1, x + 2):
        for iy in range(y - 1, y + 2):
            for iz in range(z - 1, z + 2):
                for iw in range(w - 1, w + 2):
                    if ix == x and iy == y and iz == z and iw == w:
                        continue
                    yield ix, iy, iz, iw


def p2update(cube, coord, nn):
    active = cube.setdefault(coord, 0)

    an = 0
    if active:  # active -> keep active for 2 or 3, else inactive
        for n in nn:
            an += cube.setdefault(n, 0)
            if an > 3:
                return 0
        return 2 <= an <= 3

    for n in nn:
        an += cube.setdefault(n, 0)
        if an > 3:
            return 0
    return an == 3


def part2(lines, full, cycles=6):
    # 1816
    cube = defaultdict(int)
    neighbors = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            coord = x, y, 0, 0
            cube[coord] = int(c == "#")
            neighbors[coord] = list(p2getneight(*coord))

    mmx = 0, len(lines[0]) - 1
    mmy = 0, len(lines) - 1
    mmz = 0, 0
    mmw = 0, 0
    for cycle in range(cycles):
        mmx = mmx[0] - 1, mmx[1] + 1
        mmy = mmy[0] - 1, mmy[1] + 1
        mmz = mmz[0] - 1, mmz[1] + 1
        mmw = mmw[0] - 1, mmw[1] + 1
        print(f"{mmx=} {mmy=} {mmz=} {mmw=}")
        print(f"before {cycle=} total {len(cube.keys())=} active {sum(cube.values())=}")
        newcube = cube.copy()
        for w in range(mmw[0], mmw[1] + 1):
            for z in range(mmz[0], mmz[1] + 1):
                for y in range(mmy[0], mmy[1] + 1):
                    for x in range(mmx[0], mmx[1] + 1):
                        coord = x, y, z, w
                        nn = neighbors.get(coord)
                        if not nn:
                            nn = list(p2getneight(*coord))
                            neighbors[coord] = nn
                        newcube[coord] = p2update(cube, coord, nn)
        cube = newcube

        print(f"after {cycle=} total {len(cube.keys())=} active {sum(cube.values())=}")
    return sum(cube.values())
