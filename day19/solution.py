import re
from itertools import product


def part1(lines, full):
    # 113
    rules, messages = full.split("\n\n")
    letters = {}
    rule_mapping = {}
    for line in rules.splitlines():
        line = line.strip()
        rid, rval = line.split(": ")
        if rval in ('"b"', '"a"'):
            letters[int(rid)] = rval[1]
            continue
        rule_mapping[int(rid)] = [tuple(map(int, i.split())) for i in rval.split(" | ")]

    def create_regex(rule_id):
        # Recursively build the regex pattern
        if rule_id in letters:
            return str(letters[rule_id])
        patterns = [
            "".join(create_regex(r) for r in rulegroup)
            for rulegroup in rule_mapping[rule_id]
        ]
        return "({})".format(
            "|".join(patterns)
        )  # return matchgroup with patterns OR-ed together

    rgx = re.compile("^{}$".format(create_regex(0)))
    return sum(1 for m in messages.splitlines() if rgx.match(m))


def part2(lines, full, addloops=True):
    # 253
    rules, messages = full.split("\n\n")
    letters = {}
    rule_mapping = {}
    for line in rules.splitlines():
        line = line.strip()
        rid, rval = line.split(": ")
        if rval in ('"b"', '"a"'):
            letters[int(rid)] = rval[1]
            continue
        rule_mapping[int(rid)] = [tuple(map(int, i.split())) for i in rval.split(" | ")]

    def create_regex(rule_id=0):
        # Recursively build the regex pattern
        if rule_id in letters:
            return str(letters[rule_id])
        patterns = [
            "".join(create_regex(r) for r in rulegroup)
            for rulegroup in rule_mapping[rule_id]
        ]
        return "({})".format(
            "|".join(patterns)
        )  # return matchgroup with patterns OR-ed together

    prev = matching = 0
    loops = 0

    # Modify the rules as required for part2
    # As the puzzle says the patterns are finite, so instead of loops we generate a finite sequence.
    # I didn't come up with this clever idea, sadly, got stuck on part2 too long and found this hint in the subreddit

    # Improved it a little bit by not hardcoding the maximum number of loops but starting with 1 loop, then comparing
    # to how many messages are matching with 2 loops, etc; until the number doesn't increase anymore.
    rule_mapping[8] = [[42], [42, 8000]]
    rule_mapping[11] = [[42, 31], [42, 11000, 31]]
    while True:
        if loops > 0:
            rule_mapping[8000 + loops - 1] = [[42], [42, 8000 + loops]]
            rule_mapping[11000 + loops - 1] = [[42, 31], [42, 11000 + loops, 31]]
        rule_mapping[8000 + loops] = [[42]]
        rule_mapping[11000 + loops] = [[42, 31]]

        rgx = re.compile("^{}$".format(create_regex()))
        matching = sum(1 for m in messages.splitlines() if rgx.match(m))
        print(f"{matching} messages matching with max {loops+1} loop(s)")
        if matching == prev:
            break
        prev = matching
        loops += 1
    return matching
