import re
from functools import reduce

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


class Tile:
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
        """
        Flip the grid horizontally.
        This also reverses all edges.
        Upper and bottom edge swap places.
        """
        self.final_grid = list(reversed(self.final_grid))
        self.sides["u"], self.sides["d"] = self.sides["d"], self.sides["u"]
        for v in self.sides.values():
            v["edge"] = v["edge"][::-1]

    def flip_vertical(self):
        """
        Flip the grid vertically.
        This also reverses all edges.
        Left and right edge swap places.
        """
        self.final_grid = [line[::-1] for line in self.final_grid]
        self.sides["l"], self.sides["r"] = self.sides["r"], self.sides["l"]
        for v in self.sides.values():
            v["edge"] = v["edge"][::-1]

    def align_to_neighbor(self, edge_prev, edge_curr):
        r"""

        Args:
            edge_prev: side of previous tile, the reference point
            edge_curr: side of of current tile to be aligned
        """
        rotation = dir_to_idx[edge_prev] - dir_to_idx[edge_curr]
        if abs(rotation) == 2:  # l<>r or u<>d
            res = (line for line in self._grid)
        elif rotation == -1 or rotation == 3:  # r<>d or d<>l -> rotate 1 CW
            res = rotate_1(self._grid)
        elif rotation == 0:  # r<>r or d<>d ... -> rotate twice
            res = rotate_2(self._grid)
        elif rotation == 1:  # d<>r or r<>u -> rotate 3 CW
            res = rotate_3(self._grid)
        self.final_grid = list(res)
        self.rotate_sides(rotation)

    def __repr__(self):
        links = "".join(k if v["tile"] else "." for k, v in self.sides.items())
        return f"<Tile {self.id} {links}>"

    def parse(self, text):
        header, *body = text.splitlines()
        self._grid = [line[1:-1] for line in body[1:-1]]  # remove edges
        self.id = int(header.split(" ")[1][:-1])
        # Read all edges in clockwise fashion
        # Then an adjacent edge should be equal to the reverse
        self.sides["u"]["edge"] = body[0]
        self.sides["r"]["edge"] = "".join(i[-1] for i in body)
        self.sides["d"]["edge"] = body[-1][::-1]
        self.sides["l"]["edge"] = "".join(i[0] for i in body[::-1])


def part1(lines, full):
    # 18449208814679
    unlinked_tiles = []
    for i in full.split("\n\n"):
        if not i.strip():
            break
        unlinked_tiles.append(Tile(i))

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
            corners.append(t.id)

    return reduce(lambda x, y: x * y, corners)


def part2(lines, full):
    # 1559
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

    top_left = [c for c in corners if c.sides["r"]["tile"] and c.sides["d"]["tile"]][0]
    top_left.aligned = True
    top_left.final_grid = top_left._grid
    left = top_left

    while True:
        aligned = [t for t in unlinked_tiles if t.aligned]
        if len(unlinked_tiles) == len(aligned):
            break  # All tiles are aligned

        aligned_right = 0
        for tile_a in aligned:
            tile_r = tile_a.sides["r"]["tile"]
            if tile_r is None:
                continue  # has no right neighbor
            if tile_r.aligned:
                continue  # already done

            # find the edge with which tile_r is linked to tile_a.R
            for tile_r_dir, tile_r_side in tile_r.sides.items():
                if tile_r_side["tile"] is tile_a:
                    break

            tile_r.align_to_neighbor("r", tile_r_dir)

            if tile_a.sides["r"]["edge"] == tile_r.sides["l"]["edge"]:
                # flip (because they should be opposite to each other)
                tile_r.flip_horizontal()

            tile_r.aligned = True
            aligned_right += 1

        if aligned_right == 0:
            # Move to next grid row
            direction = (
                "d"
                if (left.sides["d"]["tile"] and not left.sides["d"]["tile"].aligned)
                else "u"
            )
            opposite = "d" if direction == "u" else "u"
            tile_d = left.sides[direction]["tile"]

            # find the edge with which tile_d is linked to left.D
            for tile_d_dir, tile_d_side in tile_d.sides.items():
                if tile_d_side["tile"] is left:
                    break

            tile_d.align_to_neighbor(direction, tile_d_dir)

            if left.sides[direction]["edge"] == tile_d.sides[opposite]["edge"]:
                # flip (because they should be opposite to each other)
                tile_d.flip_vertical()
            tile_d.aligned = True
            left = tile_d

    top_left = [
        t
        for t in unlinked_tiles
        if not t.sides["u"]["tile"] and not t.sides["l"]["tile"]
    ][0]

    # combine all tiles into world grid
    cur = None
    world_rows = []
    while True:
        if cur is None:
            cur = top_left
        elif cur.sides["d"]["tile"]:
            cur = cur.sides["d"]["tile"]
        else:
            break
        row = list(i for i in cur.final_grid)
        prev_tile = cur
        while prev_tile.sides["r"]["tile"]:
            next_tile = prev_tile.sides["r"]["tile"]
            row = ["".join(i) for i in zip(row, next_tile.final_grid)]
            prev_tile = next_tile
        world_rows.extend(row)

    rl1 = re.compile("^.{18}#.{1}$")
    rl2 = re.compile("(#.{4}##.{4}##.{4}###)")
    rl3 = re.compile("^.{1}#.{2}#.{2}#.{2}#.{2}#.{2}#.{3}$")

    def searchmonsters(worldlines):
        monsters_found = 0
        for i in range(len(worldlines) - 2):
            line1, line2, line3 = worldlines[i : i + 3]
            for l2match in rl2.finditer(line2):
                start, stop = l2match.span()
                if rl3.match(line3[start:stop]) and rl1.match(line1[start:stop]):
                    monsters_found += 1
        return monsters_found

    monsters = None
    # all 4 rotations and each one flipped
    for func in (list, rotate_1, rotate_2, rotate_3):
        world1 = list(func(world_rows))
        world2 = list(reversed(world1))
        m1 = searchmonsters(world1)
        m2 = searchmonsters(world2)
        if m1:
            monsters = m1
            break
        if m2:
            monsters = m2
            break

    return "".join(world_rows).count("#") - 15 * monsters
