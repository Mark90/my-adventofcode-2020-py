dir_to_idx = {d: i for i, d in enumerate("lurd")}
idx_to_dir = {v: k for k, v in dir_to_idx.items()}


def rotate_1(grid):
    lines = grid.splitlines() if not isinstance(grid, list) else grid
    h = len(lines)
    w = len(lines[0])
    return ("".join(lines[y][x] for y in range(h - 1, -1, -1)) for x in range(0, w))


def rotate_2(grid):
    lines = grid.splitlines() if not isinstance(grid, list) else grid
    h = len(lines)
    w = len(lines[0])
    return (
        "".join(lines[y][x] for x in range(w - 1, -1, -1)) for y in range(h - 1, -1, -1)
    )


def rotate_3(grid):
    lines = grid.splitlines() if not isinstance(grid, list) else grid
    h = len(lines)
    w = len(lines[0])
    return ("".join(lines[y][x] for y in range(0, h)) for x in range(w - 1, -1, -1))


def align_grid_to_neighbor(grid, edge_prev, edge_curr):
    r"""Return difference in orientation between neighbor and self, and generator of the transposed tile lines

    Args:
        grid (str or list): grid of current tile
        edge_prev: side of previous tile, the reference point
        edge_curr: side of of current tile to be aligned

    Examples:
    >>> n, l = align_grid_to_neighbor('123\n456\n789', 'r', 'd'); n, '\n'.join(l)  # 1 cw turn
    (-1, '741\n852\n963')
    >>> n, l = align_grid_to_neighbor('123\n456\n789','r', 'r'); n, '\n'.join(l)  # 2 cw turns
    (0, '987\n654\n321')
    >>> n, l = align_grid_to_neighbor('123\n456\n789', 'r', 'u'); n, '\n'.join(l) # 3 cw turns
    (1, '369\n258\n147')
    >>> n, l = align_grid_to_neighbor(['123','456','789'], 'r', 'u'); n, '\n'.join(l)
    (1, '369\n258\n147')
    >>> n, l = align_grid_to_neighbor('123\n456\n789', 'r', 'l'); n, '\n'.join(l) # 0 turns
    (2, '123\n456\n789')
    >>> n, l = align_grid_to_neighbor('123\n456\n789','d', 'u'); n, '\n'.join(l)
    (2, '123\n456\n789')
    >>> n, l = align_grid_to_neighbor('123\n456\n789', 'd', 'r'); n, '\n'.join(l)
    (1, '369\n258\n147')
    """
    lines = grid.splitlines() if not isinstance(grid, list) else grid
    h = len(lines)
    w = len(lines[0])
    rotation = dir_to_idx[edge_prev] - dir_to_idx[edge_curr]
    if abs(rotation) == 2:  # l<>r or u<>d
        res = (line for line in lines)
    if rotation == -1 or rotation == 3:  # rotate 1 time clockwise, up becomes right
        res = rotate_1(lines)
    if rotation == 0:  # rotate 2 times clockwise, left becomes right
        res = rotate_2(lines)
    if rotation == 1:  # rotate 3 times clockwise, down becomes right
        res = rotate_3(lines)
    return rotation, res


class Tile:
    r"""
    Examples:
    >>> t = Tile("Tile 1:\n123\n456\n789")
    >>> t.sides["u"]["edge"]
    '123'
    >>> t.sides["r"]["edge"]
    '369'
    >>> t.sides["d"]["edge"]
    '987'
    >>> t.sides["l"]["edge"]
    '741'
    >>> t.rotate_sides(-1)  # 1 clockwise rotation (Down->Left)
    >>> t.sides["u"]["edge"]  # previous left side
    '741'
    >>> t.sides["r"]["edge"]  # previous up side
    '123'
    >>> t.sides["d"]["edge"]  # previous right side
    '369'
    >>> t.sides["l"]["edge"]  # previous down side
    '987'
    >>> t = Tile("Tile 1:\n123\n456\n789")
    >>> t.rotate_sides(1)  # 1 counter-clockwise rotation (Up->Left)
    >>> t.sides["l"]["edge"]  # previous up side
    '123'
    >>> t = Tile("Tile 1:\n123\n456\n789")
    >>> t.rotate_sides(0)  # 2 clockwise rotations (Right->Left)
    >>> t.sides["l"]["edge"]  # previous right side
    '369'
    """

    def __init__(self, text):
        self.id = None
        self._grid = None
        self.aligned = False
        self.final_grid = None
        self.sides = {
            side: {
                "tile": None,
                "edge": None,
            }
            for side in "lurd"
        }
        self.parse(text)

    def rotate_sides(self, rotation):
        self.sides = {
            side: self.sides[idx_to_dir[(dir_to_idx[side] - rotation + 2) % 4]]
            for side in self.sides
        }

    def flip_horizontal(self):
        # Should be called after the alignment
        self.sides["u"], self.sides["d"] = self.sides["d"], self.sides["u"]
        self.sides["l"]["edge"] = self.sides["l"]["edge"][::-1]
        self.sides["r"]["edge"] = self.sides["r"]["edge"][::-1]
        return reversed(self._grid)

    def flip_vertical(self):
        # Should be called after the alignment
        grid_lines = reversed(self._grid)
        self.sides["l"], self.sides["r"] = self.sides["r"], self.sides["l"]
        self.sides["u"]["edge"] = self.sides["u"]["edge"][::-1]
        self.sides["d"]["edge"] = self.sides["d"]["edge"][::-1]
        return (line[::-1] for line in grid_lines)

    def __repr__(self):
        links = "".join(k if v["tile"] else "." for k, v in self.sides.items())
        return f"<Tile {self.id} {links}>"

    def parse(self, text):
        header, *body = text.replace("#", "1").replace(".", "0").splitlines()
        self._grid = [line[1:-1] for line in body[1:-1]]  # remove edges
        self.id = int(header.split(" ")[1][:-1])
        # Read all edges in clockwise fashion
        # Then an adjacent edge should always be the reverse
        self.sides["u"]["edge"] = body[0]
        self.sides["r"]["edge"] = "".join(i[-1] for i in body)
        self.sides["d"]["edge"] = body[-1][::-1]
        self.sides["l"]["edge"] = "".join(i[0] for i in body[::-1])


def part2(lines, full):
    unlinked_tiles = []
    for i in full.split("\n\n"):
        if not i.strip():
            break
        unlinked_tiles.append(Tile(i))

    # First link everything
    for tile1 in unlinked_tiles:
        for tile1_side in tile1.sides.values():
            if tile1_side["tile"]:
                # edge already linked
                continue
            for tile2 in unlinked_tiles:
                if tile1 is tile2:
                    continue

                for tile2_side in tile2.sides.values():
                    if tile2_side["tile"]:
                        # edge already linked
                        continue

                    if (
                        tile1_side["edge"] == tile2_side["edge"]
                        or tile1_side["edge"] == tile2_side["edge"][::-1]
                    ):
                        # link it
                        tile1_side["tile"], tile2_side["tile"] = tile2, tile1
                        break

    corners = []
    for t in unlinked_tiles:
        if sum(1 for v in t.sides.values() if v["tile"]) == 2:
            corners.append(t)

    print("corners:", corners)
    top_left = [c for c in corners if c.sides["r"]["tile"] and c.sides["d"]["tile"]][0]
    print(f"chose {top_left} as topleft, mark as aligned")
    top_left.aligned = True
    top_left.final_grid = top_left._grid
    left = top_left

    while True:
        aligned = [t for t in unlinked_tiles if t.aligned]
        if len(unlinked_tiles) == len(aligned):
            print("All tiles are aligned")
            break

        aligned_right = 0
        for tile_a in aligned:
            tile_r = tile_a.sides["r"]["tile"]
            if tile_r is None:
                # has no right neighbor
                continue
            if tile_r.aligned:
                # already done
                continue
            # find the edge with which tile_r is linked to tile_a.R
            for tile_r_dir, tile_r_side in tile_r.sides.items():
                if tile_r_side["tile"] is tile_a:
                    # found it
                    break
            else:
                1 / 0

            # rotate tile_r so that `rile_r_side` is on the LEFT
            grid_lines = tile_r._grid
            if tile_r_dir == "l":
                grid_lines = (line for line in grid_lines)  # no rotation needed
            else:
                rotation, grid_lines = align_grid_to_neighbor(
                    grid_lines, "r", tile_r_dir
                )
                tile_r.rotate_sides(rotation)

            if tile_a.sides["r"]["edge"] == tile_r.sides["l"]["edge"][::-1]:
                pass  # we're good!
            elif tile_a.sides["r"]["edge"] == tile_r.sides["l"]["edge"]:
                # flip (because they should be opposite to each other)
                grid_lines = tile_r.flip_horizontal()
            else:
                1 / 0

            tile_r.final_grid = list(grid_lines)
            tile_r.aligned = True
            aligned_right += 1

        if aligned_right == 0:
            # expand down/up
            direction = (
                "d"
                if (left.sides["d"]["tile"] and not left.sides["d"]["tile"].aligned)
                else "u"
            )
            opposite = "d" if direction == "u" else "u"
            tile_d = left.sides[direction]["tile"]
            if tile_d is None or tile_d.aligned:
                1 / 0  # impossible
                continue

            # find the edge with which tile_d is linked to left.D
            for tile_d_dir, tile_d_side in tile_d.sides.items():
                if tile_d_side["tile"] is left:
                    # found it
                    break
            else:
                1 / 0

            # rotate tile_d.U to match left.D
            grid_lines = tile_d._grid
            if tile_d_dir == opposite:
                grid_lines = (line for line in grid_lines)  # no rotation needed
            else:
                rotation, grid_lines = align_grid_to_neighbor(
                    grid_lines, direction, tile_d_dir
                )
                tile_d.rotate_sides(rotation)

            if left.sides[direction]["edge"] == tile_d.sides[opposite]["edge"][::-1]:
                pass  # we're good!
            elif left.sides[direction]["edge"] == tile_d.sides[opposite]["edge"]:
                # flip (because they should be opposite to each other)
                grid_lines = tile_d.flip_vertical()
            else:
                1 / 0

            tile_d.final_grid = list(grid_lines)
            tile_d.aligned = True

            left = tile_d

    real_top_left = [
        t
        for t in unlinked_tiles
        if not t.sides["u"]["tile"] and not t.sides["l"]["tile"]
    ]
    real_top_left = real_top_left[0]

    # combine all tiles into world grid
    cur = None
    world_rows = []
    while True:
        if cur is None:
            cur = real_top_left
        elif cur.sides["d"]["tile"]:
            cur = cur.sides["d"]["tile"]
        else:
            break
        row = list(i for i in cur.final_grid)
        prev_tile = cur
        while prev_tile.sides["r"]["tile"]:
            next_tile = prev_tile.sides["r"]["tile"]
            # Add tile grid lines to row lines
            row = ["".join(i) for i in zip(row, next_tile.final_grid)]
            prev_tile = next_tile
        world_rows.extend(row)

    print("Done with world!")

    world_rows = [line.replace("1", "#").replace("0", ".") for line in world_rows]

    import re

    rl1 = re.compile("^.{18}#.{1}$")
    rl2 = re.compile("(#.{4}##.{4}##.{4}###)")
    # rl3 = re.compile("(.{1}#.{2}#.{2}#.{2}#.{2}#.{2}#.{3})")
    rl3 = re.compile("^.{1}#.{2}#.{2}#.{2}#.{2}#.{2}#.{3}$")

    def searchmonsters(worldlines):
        m = 0
        for i in range(len(worldlines) - 2):
            line1, line2, line3 = worldlines[i : i + 3]
            for l2match in rl2.finditer(line2):
                # print("monster middle match")
                start, stop = l2match.span()
                if rl3.match(line3[start:stop]) and rl1.match(line1[start:stop]):
                    m += 1
        return m

    monsters = []
    # all 4 rotations and each one flipped 
    for func in (list, rotate_1, rotate_2, rotate_3):
        world1 = list(func(world_rows))
        world2 = list(reversed(world1))
        m1 = searchmonsters(world1)
        m2 = searchmonsters(world2)
        monsters.append(m1)
        monsters.append(m2)
        print(f"world {func=} normal {m1=}")
        print(f"world {func=} hflip {m2=}")

    print(monsters)
    m = max(monsters)
    return ''.join(world_rows).count("#") - 15 * m

# 1949 too high
