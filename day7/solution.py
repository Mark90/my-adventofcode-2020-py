import re


class Bag:
    def __init__(self, name):
        self.name = name
        self.children = {}
        self.parents = []

    def __repr__(self):
        return f"<Bag {self.name}>"

    def add_child(self, k, v):
        self.children[k] = v

    def add_parent(self, k):
        self.parents.append(k)

    def __iter__(self):
        for k, v in self.children.items():
            yield k, v


cr = re.compile("(\d+) (\w+ \w+) bag[s]{0,1}")


def create_bags(lines):
    bags = {}
    for line in lines:
        pname, cnames = line.split(" bags contain ")
        bags.setdefault(pname, Bag(pname))
        pbag = bags[pname]
        if cnames.startswith("no"):
            continue
        for l in cnames.split(", "):
            c, name = cr.match(l).groups()
            bags.setdefault(name, Bag(name))
            cbag = bags[name]
            pbag.add_child(cbag, int(c))
            cbag.add_parent(pbag)
    return bags


def count_parents(bags, bag, r=set()):
    for p in bag.parents:
        r.add(p.name)
        r.update(count_parents(bags, p))
    return r


def part1(lines, full):
    # 287
    bags = create_bags(lines)
    return len(count_parents(bags, bags["shiny gold"]))


def count_bags(bag):
    # Recurse through bags, always return 1 for bag itself
    if not bag.children:
        return 1
    r = 0
    for cbag, num in bag:
        r += num * count_bags(cbag)
    return 1 + r


def part2(lines, full):
    # 48160
    bags = create_bags(lines)
    return count_bags(bags["shiny gold"]) - 1  # Deduct for shiny gold
