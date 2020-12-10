def part1(lines, full):
    # 3000: 7 min
    adapters = sorted(list(map(int, lines)))
    d = {1: 0, 2: 0, 3: 1}
    prev = 0
    for a in adapters:
        d[a - prev] += 1
        prev = a
    print(d)
    return d[1] * d[3]


def trav(a, i=0):
    r = 0
    # while i < len(a):
    if i + 1 == len(a):
        return 1
    if i < len(a) + 1 and a[i] + 3 == a[i + 1]:
        return 1 + trav(a, i + 1)

    return 1 + r


d = {}
for i in range(25):
    if i < 3:
        v = 0
    else:
        v = 2 ** (i - 3)
    d[i] = v + (0 if i == 0 else d[i - 1])


def gap1(size):
    if size == 0:
        return 1
    return 2 ** (size - 1) - d[size - 1]


def part2(lines, full):
    adapters = sorted(list(map(int, lines)))
    adapters = (
        [
            0,
        ]
        + adapters
        + [max(adapters) + 3]
    )
    # print(adapters)
    r = 1
    cursize = 0
    i = 0
    a = adapters
    while True:
        if i + 1 == len(a):
            r *= gap1(cursize)
            break
        cur, nex = a[i], a[i + 1]
        if nex - cur == 3:
            r *= gap1(cursize)
            cursize = 0
        else:
            cursize += 1
        i += 1
    return r
    # r = 0
    # i = -1
    # mult = {}  #
    # la = len(adapters)
    # a=adapters
    # from collections import defaultdict
    # p = defaultdict(dict)
    # while i+1 < la:
    #     i += 1

    #     print(f'\n{i=} {a[i]=}')
    #     if i+1<la and a[i] == a[i+1] + 3:
    #         # print(f'{i=} {a[i]=} {a[i+1]=}')
    #         continue
    #     print(a[i:i+4])
    #     if i+3 < la and a[i] +3== a[i+3]:
    #         # print('i',i,'mult',3)
    #         mult[i] = 4
    #         # p[i][i+3] = 3
    #     elif i+2 < la and (a[i+2] - 3 == a[i]  or a[i] == a[i+2] - 2):
    #         # print('i',i,'mult',2)

    #         # p[i][i+2] = 2
    #         mult[i] = 2
    #     # else:
    #         # print('nop')
    # print(mult)
    # r = 1
    # for k,m in mult.items():
    #     r*=m
    # # r = 1
    # # i = len(a)
    # # while i > -1:
    # #     i -= 1
    # #     if i in p:

    # # for k, v in p.items():

    # print("rrrrr",r)
    # return r
    r = trav(adapters)
    return r
