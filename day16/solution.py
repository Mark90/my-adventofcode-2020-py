from collections import defaultdict


def part1(lines, full):
    # 19087
    possible_names = defaultdict(list)
    paragraphs = full.split("\n\n")
    rules = paragraphs[0]
    for rule in rules.split("\n"):
        rule = rule.strip()
        colon = rule.split(": ")
        field = colon[0]
        ranges = colon[1].split(" or ")
        for positionrange in ranges:
            lo, hi = tuple(map(int, positionrange.split("-")))
            for position in range(lo, hi + 1):
                possible_names[position].append(field)

    othertickets = paragraphs[2].split("\n")[1:]
    suminvalid = 0
    for ticket in othertickets:
        if not ticket.strip():
            break
        for v in map(int, ticket.strip().split(",")):
            if len(possible_names[v]) == 0:
                suminvalid += v

    return suminvalid


def part2(lines, full):
    # 1382443095281
    possible_names = defaultdict(list)
    paragraphs = full.split("\n\n")
    rules = paragraphs[0]
    for rule in rules.split("\n"):
        rule = rule.strip()
        colon = rule.split(": ")
        field = colon[0]
        ranges = colon[1].split(" or ")
        for positionrange in ranges:
            lo, hi = tuple(map(int, positionrange.split("-")))
            for position in range(lo, hi + 1):
                possible_names[position].append(field)

    othertickets = paragraphs[2].split("\n")[1:]
    validtickets = 0
    possible_fieldnames = {position: defaultdict(int) for position in range(0, 20)}
    # Using valid tickets, filter eligible names per ticket field
    for ticket in othertickets:
        ticket = ticket.strip()
        if not ticket:
            break
        numbers = list(map(int, ticket.split(",")))
        for number in numbers:
            if len(possible_names[number]) == 0:
                break  # discard entire ticket
        else:
            validtickets += 1
            for position, number in enumerate(numbers):
                names = possible_names[number]
                for name in names:
                    possible_fieldnames[position][name] += 1

    # Loop over all possible names and filter those occuring in each valid ticket
    # Create set with names for each fiel
    validpos = defaultdict(set)
    for position, number in possible_fieldnames.items():
        for name, count in number.items():
            if count == validtickets:
                validpos[position].add(name)

    # Now there are still many possible names per ticket field.
    # However there should be at least one ticket which tells
    # for 1 position exactly which name it should have.
    # Using that knowledge we can derive the remaining possible names
    # for ther fields.
    know = {}
    names_found = set()
    for loop in range(len(possible_fieldnames)):
        for position, names in validpos.items():
            names -= names_found
            if len(names) == 1:
                know[position] = names.pop()
                names_found.add(know[position])

    # Finally check the departure field positions and multiply those values from
    # our own ticket.
    myt = list(map(int, paragraphs[1].split("\n")[1].strip().split(",")))
    vmul = 1
    for position, number in enumerate(myt):
        name = know[position]
        if name.startswith("departure"):
            vmul *= number

    return vmul
