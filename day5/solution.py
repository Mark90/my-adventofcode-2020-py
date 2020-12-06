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
    minsid, maxsid, sidsum = 10 ** 10, 0, 0
    for line in lines:
        bpass = (
            line.replace("B", "1").replace("F", "0").replace("R", "1").replace("L", "0")
        )
        row, col = int(bpass[:-3], 2), int(bpass[-3:], 2)
        sid = (row * 8) + col
        minsid = min(minsid, sid)
        maxsid = max(maxsid, sid)
        sidsum += sid
    return ((maxsid * (maxsid + 1)) // 2) - sidsum - (((minsid - 1) * (minsid)) // 2)
