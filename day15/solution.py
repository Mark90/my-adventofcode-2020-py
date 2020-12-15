from collections import deque


def part1(lines, full, quit=2021):
    # 1015
    startnumbers = list(map(int, lines[0].split(",")))
    spoken = {i: deque([t], maxlen=2) for t, i in enumerate(startnumbers, 1)}
    last_spoken = startnumbers[-1]
    turn = len(startnumbers) + 1
    while turn < quit:
        turns_spoken = spoken.get(last_spoken)
        if not turns_spoken or len(turns_spoken) == 1:
            number_to_speak = 0
        else:
            number_to_speak = turns_spoken[1] - turns_spoken[0]
        turns_spoken = spoken.get(number_to_speak, deque(maxlen=2))
        turns_spoken.append(turn)
        spoken[number_to_speak] = turns_spoken
        last_spoken = number_to_speak
        turn += 1
    return last_spoken


def part2(lines, full, quit=30000001):
    # 201
    # Pretty much same as part1, tiny bit faster
    startnumbers = list(map(int, lines[0].split(",")))
    spoken = {i: [t] for t, i in enumerate(startnumbers, 1)}
    last = startnumbers[-1]
    turn = len(startnumbers) + 1
    while turn < quit:
        turns_spoken = spoken.get(last)
        if not turns_spoken or len(turns_spoken) == 1:
            number_to_speak = 0
        else:
            number_to_speak = turns_spoken[1] - turns_spoken[0]
        if number_to_speak in spoken:
            turns_spoken = spoken[number_to_speak]
            turns_spoken[:2] = turns_spoken[-1], turn
        else:
            spoken[number_to_speak] = [turn]
        last = number_to_speak
        turn += 1
    return last
