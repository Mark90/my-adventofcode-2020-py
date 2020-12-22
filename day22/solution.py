from functools import reduce

print_func = print


def part1(lines, full, dbg=False):
    # 33403
    print = print_func if dbg else lambda *x: None  # poor man's logger

    p1, p2 = full.split("\n\n")
    cards_p1 = list(map(int, p1.splitlines()[1:]))
    cards_p2 = list(map(int, p2.splitlines()[1:]))
    print(f"START {cards_p1=} {cards_p2=}")
    rnd = 0
    import time

    while cards_p1 and cards_p2:
        # time.sleep(1)
        rnd += 1
        dp1 = cards_p1.pop(0)
        dp2 = cards_p2.pop(0)
        print(f"ROUND {rnd}: {dp1=} {dp2=}")
        if dp1 > dp2:
            cards_p1.append(dp1)
            cards_p1.append(dp2)

            print(f"ROUND {rnd}: p1 wins {cards_p1=} {cards_p2=}")
        else:
            cards_p2.append(dp2)
            cards_p2.append(dp1)
            print(f"ROUND {rnd}: p2 wins {cards_p1=} {cards_p2=}")
    winner = cards_p1 if cards_p1 else cards_p2
    return sum((card * pos) for pos, card in enumerate(reversed(winner), 1))


def part2(lines, full, dbg=False):
    # 29177
    print = print_func if dbg else lambda *x: None  # poor man's logger

    p1, p2 = full.split("\n\n")
    o_cards_p1 = list(map(int, p1.splitlines()[1:]))
    o_cards_p2 = list(map(int, p2.splitlines()[1:]))

    def play_recursive(cards_p1, cards_p2, rnd=0, game=1):
        print(f"\n=== Game {game} ===")
        subgame = game
        states = set()
        while cards_p1 and cards_p2:
            rnd += 1
            print(f"\n-- Round {rnd} (Game {game}) --")
            print(f"Player 1's deck: {', '.join(map(str, cards_p1))}")
            print(f"Player 2's deck: {', '.join(map(str, cards_p2))}")
            print(f"Player 1 plays: {cards_p1[0]}")
            print(f"Player 2 plays: {cards_p2[0]}")

            state = ".".join(map(str, cards_p1)) + "_" + ".".join(map(str, cards_p2))
            if state in states:
                print(f"The winner of game {game} is player 1! (infinite game)\n")
                return True  # p1 wins by default
            states.add(state)

            p1_draw = cards_p1.pop(0)
            p2_draw = cards_p2.pop(0)
            if p1_draw <= len(cards_p1) and p2_draw <= len(cards_p2):
                subgame += 1
                print("Playing a sub-game to determine the winner...")
                p1_won = play_recursive(
                    cards_p1[:p1_draw], cards_p2[:p2_draw], game=subgame
                )
                print(f"...anyway, back to game {game}.")
            else:
                p1_won = p1_draw > p2_draw

            if p1_won:
                cards_p1.append(p1_draw)
                cards_p1.append(p2_draw)
            else:
                cards_p2.append(p2_draw)
                cards_p2.append(p1_draw)
            print(f"Player {'1' if p1_won else '2'} wins round {rnd} of game {game}!")

        print(f"The winner of game {game} is player {'1' if cards_p1 else '2'}!\n")
        return len(cards_p1) > 0  # True p1, False p2

    winner = o_cards_p1 if play_recursive(o_cards_p1, o_cards_p2) else o_cards_p2
    print_func("\n== Post-game results ==")
    print_func(f"Player 1's deck:", ", ".join(map(str, o_cards_p1)))
    print_func(f"Player 2's deck:", ", ".join(map(str, o_cards_p2)))
    return sum((card * pos) for pos, card in enumerate(reversed(winner), 1))
