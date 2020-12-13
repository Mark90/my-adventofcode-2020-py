def part1(lines, full):
    # 2935
    arrival = int(lines[0])
    s = [int(i) for i in lines[1].split(",") if i.isnumeric()]

    t = [arrival % i for i in s]

    m = 10 ** 10
    x = None
    j = None
    for i in range(len(s)):
        z = s[i] - t[i]
        if z < m:
            m = z
            x = s[i]
            j = i

    return x * m


def buses_intersect_at(l, r, d):
    a = 0
    b = 0
    while True:
        i = l * a
        j = r * b
        if (j - i) == d:
            return i
            a += 1
            b += 1
        elif (j - i) > d:
            a += 1
        else:
            b += 1


def part2(lines, full):
    """Spent all day with algorithms that didn't work.
    Had to google for a hint, then found out about the LCM principle.

    In hindsight it's so damn simple."""

    # 836024966345345
    buses = {
        offset: int(v) for offset, v in enumerate(lines[1].split(",")) if v.isnumeric()
    }  # key is offset, value is bus ID

    lcm = {}
    vals = list(buses.items())
    # Compute LCM (Least Common Multiple's) for each bus
    # E.g. for buses 7, 13, 59
    # For buses 7 and 13 the LCM is 7 * 13 = 91
    # For buses 7, 13 and 59 the LCM is 7 * 13 * 59 = 5369
    lcm[0] = vals[0]
    # ugly code incoming.
    for idx, item in enumerate(vals[1:-1], 1):
        offset, busid = item
        # Store the offset for the next bus
        lcm[idx] = vals[idx + 1][0], busid * lcm[idx - 1][1]

    # Start by finding t at which the first 2 buses meet (this is before their LCM)
    t = buses_intersect_at(vals[0][1], vals[1][1], vals[1][0] - vals[0][0])

    # Now for each bus..
    for idx, lcmtup in list(lcm.items())[1:]:
        offset, lcm_for_buses = lcmtup

        # .. keep incrementing time with the LCM (of this and the past buses) until they align
        busid = buses[offset]
        while ((t + offset) % busid) != 0:
            t += lcm_for_buses
    return t
