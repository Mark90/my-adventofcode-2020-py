import json
import os
import sys
import unicodedata
from pathlib import Path

import bs4
import requests

YEAR = 2020

solution_py = r"""
def part1(lines, full):
    return


def part2(lines, full):
    return
"""

main_py = r"""from pathlib import Path

from .solution import part1, part2

with (Path(__file__).parent / "input.txt").open() as f:
    _full = f.read()

_lines = _full.splitlines()
if p1 := part1(_lines, _full):
    print(f"[part1] Result: {p1}")
if p2 := part2(_lines, _full):
    print(f"[part1] Result: {p2}")
"""


def wrap_lines(lines, maxlength=80):
    """Would have used `textwrap.wrap` but it replaces \n which I don't want."""
    for line in lines:
        if len(line) < maxlength:
            yield f"{line}\n"
            continue

        new_line_parts = []
        for old_line_part in map(str, line.split(" ")):
            if (
                len(old_line_part) + sum(len(w) + 1 for w in new_line_parts)
            ) >= maxlength:
                yield "{}\n".format(" ".join(new_line_parts))
                new_line_parts = []
            new_line_parts.append(old_line_part)

        if new_line_parts:
            yield "{}\n".format(" ".join(new_line_parts))


def update_puzzle_text(filepath, num, cookies):
    """Retrieve the puzzle text for day `num` and create puzzle.txt in the corresponding module.

    Args:
        filepath (Path): path to puzzle.txt to create / update
        num (int): day to retrieve puzzle text for
        cookies (dict): nom
    """
    response = requests.get(
        f"https://adventofcode.com/{YEAR:d}/day/{num:d}", cookies=cookies
    )
    assert response.ok, "Failed response {}".format(response)
    if "[log out]" not in response.text.lower():
        os.unlink(".auth.json")
        raise Exception("Cookies have expired")

    soup = bs4.BeautifulSoup(response.text, "html.parser")

    def tag_to_text(tag):
        return unicodedata.normalize("NFKD", tag.text.rstrip())

    with filepath.open(mode="w") as f:
        for part in (i.contents for i in soup.find_all("article")):
            html_as_text = "\n".join(
                tag_to_text(i) if hasattr(i, "text") else i.rstrip() for i in part
            ).splitlines()
            f.writelines(wrap_lines(html_as_text))
            f.write("\n")


def get_puzzle_input(filepath, num, cookies):
    """

    Args:
        puzzlepath (Path): path to input.txt to create
        num (int): day to retrieve input text for
        cookies (dict): nom
    """
    r = requests.get(
        f"https://adventofcode.com/{YEAR:d}/day/{num:d}/input", cookies=cookies
    )
    assert r.ok, "Failed response {}".format(r)
    with filepath.open(mode="w") as f:
        f.write(r.text)


def main(num, cookies):
    """Create directory for given day and/or update files in it."""
    daydir = Path(__file__).parent.parent / f"day{num:d}"
    if daydir.exists():
        print("Update puzzle.txt in ", daydir)
        update_puzzle_text(daydir / "puzzle.txt", num, cookies)
        return

    print("Init directory", daydir)
    daydir.mkdir()
    update_puzzle_text(daydir / "puzzle.txt", num, cookies)
    (daydir / "__init__.py").touch()
    with (daydir / "solution.py").open(mode="w") as f:
        f.write(solution_py)
    with (daydir / "__main__.py").open(mode="w") as f:
        f.write(main_py)

    get_puzzle_input(daydir / "input.txt", num, cookies)


if __name__ == "__main__":
    try:
        _day_num = int(sys.argv[1])
    except (ValueError, IndexError):
        print("Day parameter should be an int")
        exit(1)

    authfile = Path(__file__).parent.parent / ".auth.json"
    if not authfile.exists():
        _cookies = {
            "_ga": input("Enter cookie_ga: ").strip(),
            "session": input("Enter cookie_session: ").strip(),
        }
        with authfile.open(mode="w") as f:
            json.dump(_cookies, f)

    with authfile.open() as f:
        _cookies = json.load(f)

    main(_day_num, _cookies)
