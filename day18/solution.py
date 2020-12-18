from operator import mul, add, sub


def part1(lines, full):
    # 15285807527593
    lines = full.replace(" ", "").splitlines()
    modes = {"+": add, "*": mul}

    def calc(ll, i=0):
        lhs = 0
        mode = add
        while i < len(ll):
            c = ll[i]
            if c == "(":
                i, rhs = calc(ll, i=i + 1)
                lhs = mode(lhs, rhs)
            elif c == ")":
                return i, lhs
            elif c in modes:
                mode = modes[c]
            else:
                lhs = mode(lhs, int(c))
            i += 1
        return lhs

    return sum(calc(l.strip()) for l in lines)


from functools import reduce


def part2(lines, full):
    # 461295257566346
    lines = full.replace(" ", "").splitlines()

    def calc(ll, i=0):
        numbers = [0]
        mode = "+"
        while i < len(ll):
            c = ll[i]
            if c == "(":
                i, rhs = calc(ll, i=i + 1)
                if mode == "+":
                    numbers[-1] += rhs
                else:
                    numbers.append(rhs)
            elif c == ")":
                return i, reduce(mul, numbers)
            elif c in "+*":
                mode = c
            else:
                if mode == "+":
                    numbers[-1] += int(c)
                else:  # *
                    numbers.append(int(c))
            i += 1
        return reduce(mul, numbers)

    return sum(calc(l.strip()) for l in lines)
