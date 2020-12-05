from pathlib import Path

from .solution import part1, part2

with (Path(__file__).parent / "input.txt").open() as f:
    _lines = f.readlines()

part1(_lines)
part2(_lines)
