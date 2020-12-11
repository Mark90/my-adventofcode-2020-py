z = {}


def pr(s, w, h):
    for i in range(1, h + 1):
        left = (i * (w + 2)) + 1
        right = (i * (w + 2)) + w + 1
        print("".join(s[left:right]))


def pv(s, w, h):
    for i in range(0, h + 2):
        left = i * (w + 2)
        right = (i * (w + 2)) + w + 2
        print("".join(s[left:right]))


def part1(lines, full):
    # 2211
    w = full.index("\n")
    h = full.count("\n")
    full = (
        "." * (w + 2) + "\n" + "\n".join(f".{f}." for f in full.split("\n")) + "." * (w)
    )
    seats = list(full.replace("\n", ""))
    loop = 0
    while True:
        newseats = seats.copy()
        change = False
        for i, c in enumerate(seats):
            if i < (w + 2) or (i % (w + 2) == 0) or (i // (w + 2) >= h + 1):
                continue
            if c == ".":
                continue
            if i not in z:
                pos = (
                    i - 1,
                    i + 1,
                    i - (w + 2),
                    i + (w + 2),
                    i - (w + 2) - 1,
                    i - (w + 2) + 1,
                    i + (w + 2) - 1,
                    i + (w + 2) + 1,
                )
                z[i] = pos
            pos = z[i]
            if c == "L":
                if not any(seats[d] == "#" for d in pos):
                    newseats[i] = "#"
                    change = True
            if c == "#":
                mm = 0
                for d in pos:
                    if seats[d] == "#":
                        mm += 1
                if mm >= 4:
                    newseats[i] = "L"
                    change = True

        seats = newseats
        if not change:
            break
        loop += 1
    return sum(1 for i in seats if i == "#")


def look(s, i, advance, log=False):
    while s[i] != "x":
        ni = advance(i)
        if s[ni] not in "x.":
            return s[ni]
        i = ni


def cansee(seats, i, funcs):
    for direction in funcs:
        if look(seats, i, direction) == "#":
            return True
    return False


def toomanypeople(seats, i, funcs):
    mm = 0
    for f in funcs:
        zxc = look(seats, i, f)
        if zxc == "#":
            mm += 1
        if mm == 5:
            return True
    return False


def part2(lines, full):
    # 1995
    w = full.index("\n")
    h = full.count("\n")
    full = (
        "x" * (w + 2) + "\n" + "\n".join(f"x{f}x" for f in full.split("\n")) + "x" * (w)
    )

    def gol(i):
        return i - 1

    def gor(i):
        return i + 1

    def gou(i):
        return i - (w + 2)

    def god(i):
        return i + (w + 2)

    def goul(i):
        return i - (w + 2) - 1

    def gour(i):
        return i - (w + 2) + 1

    def godl(i):
        return i + (w + 2) - 1

    def godr(i):
        return i + (w + 2) + 1

    funcs = [gol, gor, gou, god, goul, gour, godl, godr]
    seats = list(full.replace("\n", ""))
    while True:
        newseats = seats.copy()
        change = False
        for i, c in enumerate(seats):
            if i < (w + 2) or (i % (w + 2) == 0) or (i // (w + 2) >= h + 1):
                continue
            if c == ".":
                continue
            if c == "L":
                if not cansee(seats, i, funcs):
                    newseats[i] = "#"
                    change = True
            if c == "#":
                if toomanypeople(seats, i, funcs):
                    newseats[i] = "L"
                    change = True

        seats = newseats
        if not change:
            break
    return sum(1 for i in seats if i == "#")
