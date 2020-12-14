def part1(lines, full):
    # 9879607673316
    m = None
    mem = {}
    for line in lines:
        if "mask" in line:
            m = {k: v for k, v in enumerate(line.split(" = ")[1]) if v != "X"}
            continue

        a, v = line.split(" = ")
        a = int("".join(c for c in a if c.isnumeric()))
        v = int(v)
        newv = "".join(m.get(pos, c) for pos, c in enumerate(format(v, "b").zfill(36)))
        mem[a] = int(newv, 2)

    return sum(mem.values())


def part2(lines, full):
    # 3435342392262
    m = None
    mline = None
    x = None
    xx = None
    mem = {}
    for line in lines:
        if "mask" in line:
            mline = line
            m = {k: v for k, v in enumerate(line.split(" = ")[1]) if v == "1"}

            x = mline.count("X")
            xx = [k for k, v in enumerate(mline.split(" = ")[1]) if v == "X"]
            continue

        a, v = line.split(" = ")
        a = int("".join(c for c in a if c.isnumeric()))
        v = int(v)

        for i in range(0, 2 ** x):
            repl = dict(zip(xx, format(i, "b").zfill(x)))

            newa = "".join(
                m.get(pos, repl.get(pos, c))
                for pos, c in enumerate(format(a, "b").zfill(36))
            )
            mem[newa] = v

    return sum(mem.values())
