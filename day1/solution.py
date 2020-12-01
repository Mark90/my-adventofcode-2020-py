def part1(lines):
    lines = list(map(int, lines))
    for i, a in enumerate(lines):
        for j, b in enumerate(lines):
            if i==j: continue
            if (a+b) == 2020:
                print("[part1] {}".format(a*b))
                return


def part2(lines):
    lines = list(map(int, lines))
    for i, a in enumerate(lines):
        for j, b in enumerate(lines):
            for k, c in enumerate(lines):
                if i==j or j==k or i == k: continue
                if (a+b+c) == 2020:
                    print("[part2] {}".format(a*b*c))
                    return

