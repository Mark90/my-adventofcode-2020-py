# from dataclasses import Data

# @dataclass
# class Passport:


def parse_passport(lines):
    lines = [l.strip() for l in lines]
    joined = " ".join(lines)
    # print(f'joined {joined} count {joined.count(":")}')
    return joined.count(":") == 8 or (joined.count(":") == 7 and "cid:" not in joined)
    # p = [v.split(':') for v in joined.split(" ")]
    # assert all(len(i) == 2 for i in p) # TODO remove
    # return len(p) == 8 or (len(p)==7 and any(v[0] == )


def yield_pass(lines):
    sublines = []
    for line in lines:
        if not line.strip():
            yield parse_passport(sublines)
            sublines = []
        else:
            sublines.append(line)
    if sublines:
        yield parse_passport(sublines)


def part1(lines):
    # LINE SEPARATORS ARE STILL ATTACHED!
    valid = 0
    for result in yield_pass(lines):
        valid += 1 if result else 0
    print("p1", valid)


# 203 too low
import re

ECL = ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")


def parse_passport2(lines):
    lines = [l.strip() for l in lines]
    joined = " ".join(lines)
    # print(f'joined {joined} count {joined.count(":")}')
    if not (
        joined.count(":") == 8 or (joined.count(":") == 7 and "cid:" not in joined)
    ):
        return False

    p = (v.split(":") for v in joined.split(" "))
    d = {v[0]: v[1] for v in p}
    if not 1920 <= int(d["byr"]) <= 2002:
        print(f"byr {d}")
        return False
    if not 2010 <= int(d["iyr"]) <= 2020:
        print(f"iyr {d}")
        return False
    if not 2020 <= int(d["eyr"]) <= 2030:
        print(f"eyr {d}")
        return False
    if not (d["hgt"].endswith("cm") or d["hgt"].endswith("in")):
        print(f"hgt1 {d}")
        return False
    h = int(d["hgt"][:-2])
    if "cm" in d["hgt"]:
        if not 150 <= h <= 193:
            print(f"hgt2 {d}")
            return False
    elif not 59 <= h <= 76:
        print(f"hgt3 {d}")
        return False
    if not (re.match("#[0-9a-f]{6}", d["hcl"])):
        print(f"hcl {d}")
        return False
    if d["ecl"] not in ECL:
        print(f"ecl {d}")
        return False
    if not (len(d["pid"]) == 9 and d["pid"].isnumeric()):
        print(f"pid {d}")
        return False
    return True


def yield_pass2(lines):
    sublines = []
    for line in lines:
        if not line.strip():
            yield parse_passport2(sublines)
            sublines = []
        else:
            sublines.append(line)
    if sublines:
        yield parse_passport2(sublines)


def part2(lines):

    valid = 0
    for result in yield_pass2(lines):
        valid += 1 if result else 0
    print("p2", valid)

#179 