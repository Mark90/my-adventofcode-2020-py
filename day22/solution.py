def part1(lines, full):
    # 33403
    p1, p2 = full.split("\n\n")
    cards_p1 = list(map(int, p1.splitlines()[1:]))
    cards_p2 = list(map(int, p2.splitlines()[1:]))

    while cards_p1 and cards_p2:
        dp1 = cards_p1.pop(0)
        dp2 = cards_p2.pop(0)
        if dp1 > dp2:
            cards_p1.append(dp1)
            cards_p1.append(dp2)
        else:
            cards_p2.append(dp2)
            cards_p2.append(dp1)
    winner = cards_p1 if cards_p1 else cards_p2
    return sum((card * pos) for pos, card in enumerate(reversed(winner), 1))


def part2(lines, full):
    p1, p2 = full.split("\n\n")
    o_cards_p1 = list(map(int, p1.splitlines()[1:]))
    o_cards_p2 = list(map(int, p2.splitlines()[1:]))

    def play_recursive(cards_p1, cards_p2):
        states = set()
        while cards_p1 and cards_p2:
            state = tuple(cards_p1 + [None] + cards_p2)
            if state in states:
                return True  # p1 wins by default
            states.add(state)

            p1_draw = cards_p1.pop(0)
            p2_draw = cards_p2.pop(0)
            if p1_draw <= len(cards_p1) and p2_draw <= len(cards_p2):
                p1_won = play_recursive(cards_p1[:p1_draw], cards_p2[:p2_draw])
            else:
                p1_won = p1_draw > p2_draw

            if p1_won:
                cards_p1.append(p1_draw)
                cards_p1.append(p2_draw)
            else:
                cards_p2.append(p2_draw)
                cards_p2.append(p1_draw)
        return len(cards_p1) > 0  # p1 has cards -> wins game, else p2

    winner = o_cards_p1 if play_recursive(o_cards_p1, o_cards_p2) else o_cards_p2
    return sum((card * pos) for pos, card in enumerate(reversed(winner), 1))
