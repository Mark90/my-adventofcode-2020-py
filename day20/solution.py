dirs = {d: i for i, d in enumerate("lurd")}
nums = {v: k for k, v in dirs.items()}
from pprint import pformat as pf


def align_grid_to_neighbor(grid, edge_n, edge_s, flip):
    r"""Return difference in orientation between neighbor and self, and generator of the transposed tile lines

    Args:
        grid (str or list): grid to align to the neighbor
        edge_n: side of neighbor that matches tile
        edge_s: side of tile that matches neighbor
        flip: boolean whether the grip should be flipped

    Examples:
    >>> n, l = align_grid_to_neighbor('123\n456\n789', 'r', 'd', False); n, '\n'.join(l)  # 1 cw turn
    (-1, '741\n852\n963')
    >>> n, l = align_grid_to_neighbor('123\n456\n789','r', 'd', True); n, '\n'.join(l)
    (-1, '963\n852\n741')
    >>> n, l = align_grid_to_neighbor('123\n456\n789','r', 'r', False); n, '\n'.join(l)  # 2 cw turns
    (0, '987\n654\n321')
    >>> n, l = align_grid_to_neighbor('123\n456\n789','r', 'r', True); n, '\n'.join(l)
    (0, '321\n654\n987')
    >>> n, l = align_grid_to_neighbor('123\n456\n789', 'r', 'u', False); n, '\n'.join(l) # 3 cw turns
    (1, '369\n258\n147')
    >>> n, l = align_grid_to_neighbor(['123','456','789'], 'r', 'u', False); n, '\n'.join(l)
    (1, '369\n258\n147')
    >>> n, l = align_grid_to_neighbor('123\n456\n789', 'r', 'l', False); n, '\n'.join(l) # 0 turns
    (2, '123\n456\n789')
    >>> n, l = align_grid_to_neighbor('123\n456\n789', 'r', 'l', True); n, '\n'.join(l)
    (2, '789\n456\n123')
    >>>
    >>> n, l = align_grid_to_neighbor('123\n456\n789','d', 'u', False); n, '\n'.join(l)
    (2, '123\n456\n789')
    >>> n, l = align_grid_to_neighbor('123\n456\n789', 'd', 'r', False); n, '\n'.join(l)
    (1, '369\n258\n147')
    """
    lines = grid.splitlines() if not isinstance(grid, list) else grid
    h = len(lines)
    w = len(lines[0])
    difference = dirs[edge_n] - dirs[edge_s]
    if abs(difference) == 2:  # l<>r or u<>d
        res = (line for line in lines)
    if difference == -1 or difference == 3:  # rotate 1 time clockwise, up becomes right
        res = ("".join(lines[y][x] for y in range(h - 1, -1, -1)) for x in range(0, w))
    if difference == 0:  # rotate 2 times clockwise, left becomes right
        res = (
            "".join(lines[y][x] for x in range(w - 1, -1, -1))
            for y in range(h - 1, -1, -1)
        )
    if difference == 1:  # rotate 3 times clockwise, down becomes right
        res = ("".join(lines[y][x] for y in range(0, h)) for x in range(w - 1, -1, -1))
    # print(f"transform {edge_n=} {edge_s=} -> {difference=}")
    return difference, res if not flip else reversed(list(res))


class Tile:
    def __init__(self, text):
        self.id = None
        self.grid = None
        self.diff = None
        self.n = {
            d: {
                "tile": None,
                "edge": None,
            }
            for d in "lrud"
        }
        self.parse(text)

    def __repr__(self):
        return f"<Tile {self.id}>"

    def parse(self, text):
        header, *body = text.replace("#", "1").replace(".", "0").splitlines()
        self._grid = [line[1:-1] for line in body[1:-1]]  # drop edges (ludr)
        self.id = int(header.split(" ")[1][:-1])
        l = "".join(i[0] for i in body)

        r = "".join(i[-1] for i in body[::-1])  # reverse for orientation
        self.n["u"]["edge"] = body[0][::-1]  # reverse for orientation
        # r = "".join(i[-1] for i in body)
        # self.n["u"]["edge"] = body[0]

        self.n["d"]["edge"] = body[-1]
        self.n["l"]["edge"] = l
        self.n["r"]["edge"] = r

    # def try_link(self, other):
    #     if any(self is ov["tile"] for ov in other.n.values()):
    #         return True
    #     for sd, sv in self.n.items():
    #         if sv["tile"]:
    #             continue
    #         for od, ov in other.n.items():
    #             if ov["tile"]:
    #                 continue
    #             if sv["edge"] == ov["edge"] or sv["edge"] == ov["edge"][::-1]:
    #                 sv["tile"] = other
    #                 ov["tile"] = self
    #                 return True
    #     return False

    # def orient_to(self, neighbor, edge_n):
    #     """Check which side maps to neighbor's specified edge
    #     Args:
    #         neighbor: adjacent tile
    #     """
    #     rotate_to = None
    #     flip = False
    #     for sd, sv in self.n.items():
    #         if neighbor.n[edge_n]["edge"] == sv["edge"]:
    #             return align_grid_to_neighbor(self.innergrid, edge_n, sd, False)
    #         elif neighbor.n[edge_n]["edge"] == sv["edge"][::-1]:
    #             return align_grid_to_neighbor(self.innergrid, edge_n, sd, True)

    def link_and_orient(self, other):
        if any(self is ov["tile"] for ov in other.n.values()):
            # Already aligned
            return True
        for sd, sv in self.n.items():
            if sv["tile"]:
                continue
            for od, ov in other.n.items():
                if ov["tile"]:
                    continue
                if sv["edge"] == ov["edge"]:
                    print(
                        f"Found {self=} edge {sv['edge']} to match with {other=} edge {ov['edge']}"
                    )
                    sv["tile"] = other
                    ov["tile"] = self
                    if not self.grid:

                        self.diff, lines = align_grid_to_neighbor(
                            self._grid, od, sd, False
                        )
                        print(
                            f"Used {other} {od} to align {self} {sd} with {self.diff=} flip=NO"
                        )

                        self.grid = list(lines)

                        print(f"BEFORE {pf(self.n)}")
                        self.n = {
                            k: self.n[nums[(dirs[k] - self.diff + 2) % 4]]
                            for k in self.n
                        }
                        print(f"AFTER {pf(self.n)} ")
                    else:
                        print(f"Linked {self} {sd} to {other} {od}")
                    return True
                if sv["edge"] == ov["edge"][::-1]:
                    print(
                        f"Found {self=} edge {sv['edge']} to match with {other=} edge {ov['edge']} REVERSED"
                    )
                    sv["tile"] = other
                    ov["tile"] = self
                    if not self.grid:
                        self.diff, lines = align_grid_to_neighbor(
                            self._grid, od, sd, True
                        )
                        print(
                            f"Used {other} {od} to align {self} {sd} with {self.diff=} flip=YES"
                        )
                        self.grid = list(lines)  # [''.join(i) for i in zip(row, lines)]
                        print(f"BEFORE {pf(self.n)}")
                        # self.n['u'], self.n['d'] = self.n['d'], self.n['u']
                        top, bottom = (
                            nums[(dirs[sd] + 1) % 4],
                            nums[(dirs[sd] - 1 + 4) % 4],
                        )
                        self.n = {
                            k: self.n[nums[(dirs[k] - self.diff + 2) % 4]]
                            for k in self.n
                        }
                        self.n[top], self.n[bottom] = self.n[bottom], self.n[top]
                        print(f"AFTER {pf(self.n)} (replaced {top=} and {bottom=})")
                        sv["edge"] = sv["edge"][::-1]
                        print(
                            f"Flipped {self} edge {sd} from {sv['edge'][::-1]} to {sv['edge']}"
                        )
                    else:
                        print(f"Linked {self} {sd} to {other} {od}")
                    return True
        return False


def part1(lines, full):
    # 18449208814679
    tiles = []
    for i in full.split("\n\n"):
        if not i.strip():
            break
        tiles.append(Tile(i))
    tl = 0
    for t1 in tiles:
        for t2 in tiles:
            if t1 == t2:
                continue
            if t1.try_link(t2):
                # print(f"{t1}  -  {t2}")
                tl += 1
    print(tl)
    corners = []
    for t in tiles:
        if sum(1 for v in t.n.values() if v["tile"]) == 2:
            corners.append(t.id)
    print(corners)
    from functools import reduce

    return reduce(lambda x, y: x * y, corners)


def part2(lines, full):
    tiles = []
    for i in full.split("\n\n"):
        if not i.strip():
            break
        tiles.append(Tile(i))
    for t1 in tiles:
        for t2 in tiles:
            if t1 == t2:
                continue
            # t1.try_link(t2)
            if t1.link_and_orient(t2):
                print()

    for t in tiles:
        links_to = [(l["tile"], l["edge"]) for l in t.n.values() if l["tile"]]
        print(f"{t} -> {links_to}")

    topleft = None
    for t in tiles:
        # nums[dirs['u'] - diff]
        # matching_edge = dirs[col_edge_n] - diff
        # col_edge_n = nums[(matching_edge +2 )% 4]
        if not t.n["u"]["tile"] and not t.n["l"]["tile"]:
            print("topleft", t)
            topleft = t
    return
    print()

    world_rows = []
    cur = None
    prev = None
    # Start at topleft tile, follow it down
    row_edge_n = "d"
    baill = 0
    while True:
        print()
        if cur is None:
            cur = topleft
            lines = (i for i in cur.innergrid)
        elif not cur.n[row_edge_n]["tile"]:
            print(
                f"{topleft} was topleft and {cur} was the leftmost tile of the last row, world complete"
            )
            break
        else:
            baill += 1
            if baill == 15:
                return "uhoh"
            next_cur = cur.n[row_edge_n]["tile"]
            row_diff, lines = next_cur.orient_to(cur, row_edge_n)
            print(f">>> advance from {cur} to {next_cur} with {row_diff=}")

            matching_edge = dirs[row_edge_n] + row_diff
            row_edge_n = nums[(matching_edge + 2) % 4]
            # continue with down neighbor
            #  -> transform it to current
            # for each right neighbor ...
            cur = next_cur

        row = list(lines)
        #  -> return tile grid WITHOTU EDGES
        # - add to world grid

        col_edge_n = nums[(dirs[row_edge_n] + 3) % 4]
        # col_edge_n = "r"

        prev_tile = cur

        bail = 0
        print(f"New row -> {col_edge_n=}")
        while prev_tile.n[col_edge_n]["tile"]:
            # for each right neighbor
            #  - check which side maps to us
            #    - if edge is direct match -> just rotate (if needed) -> return tile grid  WITHOUT EDGES
            #    - if edge is not direct match -> flip (and rotate if needed) -> return tile grid  WITHOUT EGDES
            next_tile = prev_tile.n[col_edge_n]["tile"]
            bail += 1
            if bail == 15:
                return "uhoh"
            diff, lines = next_tile.orient_to(prev_tile, col_edge_n)

            # using the diff determine which edge from current next_tile to
            # compare to the "next" next_tile
            matching_edge = dirs[col_edge_n] - diff
            removeme_old_col_edge_n = col_edge_n
            col_edge_n = nums[(matching_edge + 2) % 4]

            print(
                f"Aligned {prev_tile} to {next_tile} with {diff=} ; col_edge_n {removeme_old_col_edge_n} -> {col_edge_n}"
            )

            # Add tile grid lines to row lines
            row = ["   ".join(i) for i in zip(row, lines)]
            prev_tile = next_tile

            print()
            print("\n".join(row).replace("1", "#").replace("0", "."))
            print()
        print("Done with row")
        # add row lines to world grid
        world_rows.extend(row)
        world_rows.extend(["", "", ""])

    print()
    fmt = "\n".join(world_rows)
    print(fmt.replace("1", "#").replace("0", "."))
    roughness = full.count("#")
    # grid is done. now find the monsters and deduct them from the total hashes

    # monster has 15 #
    # prevline=None
    # for line in
    # use reges match

    # when no monsters found, try other rotations/flips
    return
