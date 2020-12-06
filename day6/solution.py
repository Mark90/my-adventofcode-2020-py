def part1(lines, full):
    return sum(len(set(g.replace("\n", ""))) for g in full.split("\n\n"))


def part2(lines, full):
    yes = 0
    for group in (full + "\n\n\n").split("\n\n"):
        if not group:
            break
        persons = group.count("\n") + 1
        for question in "abcdefghijklmnopqrstuvwxyz":
            yes += group.count(question) == persons
    return yes
