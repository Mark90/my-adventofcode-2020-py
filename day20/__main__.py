from pathlib import Path

# from .solution import part1
from .solution2 import part2

with (Path(__file__).parent / "input.txt").open() as f:
    _full = f.read()

_lines = _full.splitlines()
# if p1 := part1(_lines, _full):
#     print(f"[part1] Result: {p1}")
if p2 := part2(_lines, _full):
    print(f"[part2] Result: {p2}")
