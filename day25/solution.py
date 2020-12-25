def determine_loopsize(pubkey):

    value = 1
    loop = 0
    while value != pubkey:
        loop += 1
        value = (value * 7) % 20201227
    return loop


def determine_privkey(subnum, loopsize):
    value = 1
    for _ in range(loopsize):
        value = (value * subnum) % 20201227
    return value


def part1(lines, full):
    # 8740494
    cpb = int(lines[0])
    dpb = int(lines[1])

    cl = determine_loopsize(cpb)
    print("card cl", cl)
    dl = determine_loopsize(dpb)
    print("card dl", dl)

    ppk1 = determine_privkey(cpb, dl)
    ppk2 = determine_privkey(dpb, cl)
    print("ppk1", ppk1)
    print("ppk2", ppk2)
    return ppk1


def part2(lines, full):
    return
