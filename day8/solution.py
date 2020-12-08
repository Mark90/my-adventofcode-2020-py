def part1(lines, full):
    # 1753
    acc = 0
    ins = [(l.split(" ")[0], int(l.split(" ")[1])) for l in lines]
    pos = 0
    while True:
        if ins[pos] is None:
            break
        if ins[pos][0] == "nop":
            ins[pos] = None
        elif ins[pos][0] == "acc":
            acc += ins[pos][1]
        elif ins[pos][0] == "jmp":
            v = ins[pos][1]
            ins[pos] = None
            pos += v
            continue
        ins[pos] = None
        pos += 1
    return acc


def run(ins, skip):
    acc = 0
    pos = 0
    unchanged = True
    while pos < len(ins):
        if ins[pos] is None:
            return None
        if ins[pos][0] == "nop":
            if unchanged and (pos not in skip) and ins[pos][1] != 0:
                unchanged = False
                ins[pos] = ("jmp", ins[pos][1])
                skip.add(pos)
                continue
            ins[pos] = None
        elif ins[pos][0] == "acc":
            acc += ins[pos][1]
        elif ins[pos][0] == "jmp":
            if unchanged and pos not in skip:
                unchanged = False
                ins[pos] = ("nop", ins[pos][1])
                skip.add(pos)
                continue
            v = ins[pos][1]
            ins[pos] = None
            pos += v
            continue
        ins[pos] = None
        pos += 1

    return acc


def part2(lines, full):
    # 733
    ins = [(l.split(" ")[0], int(l.split(" ")[1])) for l in lines]
    acc = None
    skip = set()
    while acc is None:
        acc = run(ins.copy(), skip)
    return acc
