def part1(lines, full):
    maxsid = 0
    for line in lines:
        bpass = (
            line.replace("B", "1").replace("F", "0").replace("R", "1").replace("L", "0")
        )
        row, col = int(bpass[:-3], 2), int(bpass[-3:], 2)
        sid = (row * 8) + col
        maxsid = max(sid, maxsid)
    return maxsid


def part2(lines, full):
    sids = []
    for line in lines:
        bpass = (
            line.replace("B", "1").replace("F", "0").replace("R", "1").replace("L", "0")
        )
        row, col = int(bpass[:-3], 2), int(bpass[-3:], 2)
        sid = (row * 8) + col
        sids.append(sid)
    sids.sort()
    prev = sids[0]
    for cur in sids[1:]:
        if cur > prev + 1:
            return cur - 1
        prev = cur
