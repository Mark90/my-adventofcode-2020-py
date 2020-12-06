def parse_passport(lines):
    joined = " ".join(l.strip() for l in lines.splitlines())
    return joined.count(":") == 8 or (joined.count(":") == 7 and "cid:" not in joined)


def part1(lines, full):
    return sum(parse_passport(i) for i in full.split("\n\n"))


import re


def parse_passport2(lines):
    joined = " ".join(l.strip() for l in lines.splitlines())
    if not (
        joined.count(":") == 8 or (joined.count(":") == 7 and "cid:" not in joined)
    ):
        return False

    kv_pairs = (v.split(":") for v in joined.split(" "))
    d = {k: v for k, v in kv_pairs}
    if not 1920 <= int(d["byr"]) <= 2002:
        return False
    if not 2010 <= int(d["iyr"]) <= 2020:
        return False
    if not 2020 <= int(d["eyr"]) <= 2030:
        return False
    if not (d["hgt"].endswith("cm") or d["hgt"].endswith("in")):
        return False
    h = int(d["hgt"][:-2])
    if "cm" in d["hgt"]:
        if not 150 <= h <= 193:
            return False
    elif not 59 <= h <= 76:
        return False
    if not (re.match("#[0-9a-f]{6}", d["hcl"])):
        return False
    if d["ecl"] not in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"):
        return False
    if not (len(d["pid"]) == 9 and d["pid"].isnumeric()):
        return False
    return True


def part2(lines, full):
    return sum(parse_passport2(i) for i in full.split("\n\n"))
