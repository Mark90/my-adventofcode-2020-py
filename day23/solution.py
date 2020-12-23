class Node:
    def __init__(self, value, current=False):
        self.right = None
        self.value = value

    def __repr__(self):
        return f"{self.value}"

    def link_right(self, other: "Node"):
        self.right = other

    def to_list(self, stop=None):
        # Helper function to traverse the list starting at this node
        res = []
        if stop is self:
            return res
        res.append(self)
        if self.right is None:
            return res
        stop = self if stop is None else stop
        res.extend(self.right.to_list(stop=stop))
        return res


class LinkedList:
    def __init__(self, name="cups"):
        self.values = {}
        self.current = None
        self.min_value = None
        self.max_value = None
        self.name = name

    def setup(self, items):
        nodes = [Node(i) for i in items]
        nodes[-1].right = nodes[0]
        self.current = nodes[0]
        for i, node in enumerate(nodes[:-1]):
            node.link_right(nodes[i + 1])
        self.min_value = min(items)
        self.max_value = max(items)
        self.values = {n.value: n for n in nodes}

    def pickup_next3(self):
        """Removes the 3 next cups from the circle and returns the first node"""
        first_of_3 = self.current.right
        last_of_3 = first_of_3.right.right
        self.current.link_right(last_of_3.right)
        last_of_3.right = None  # not really needed but a good safeguard
        return first_of_3

    def insert_nodes_after_dest(self, dest: Node, first_of_3: Node):
        dest_right = dest.right
        last_of_3 = first_of_3.right.right
        dest.link_right(first_of_3)
        last_of_3.link_right(dest_right)

    def find_destination(self, first_of_3):
        value = self.current.value
        exclude = (
            first_of_3.value,
            first_of_3.right.value,
            first_of_3.right.right.value,
        )
        while True:
            value -= 1
            if value < self.min_value:
                value = self.max_value
            if value in exclude:
                continue
            return self.values[value]


def part1(lines, full, moves=100):
    # 68245739
    cups = [int(c) for c in lines[0]]
    circle = LinkedList()
    circle.setup(cups)
    for _ in range(moves):
        first_of_3 = circle.pickup_next3()
        dest = circle.find_destination(first_of_3)
        circle.insert_nodes_after_dest(dest, first_of_3)
        circle.current = circle.current.right
    return (
        "".join(map(str, circle.values[1].to_list()[1:]))
        .replace("(", "")
        .replace(")", "")
    )


def part2(lines, full, moves=10_000_000, N=1_000_000):
    # 219634632000
    cups = [int(c) for c in lines[0]]
    m = max(cups)
    cups += list(range(m + 1, N + 1))
    circle = LinkedList()
    circle.setup(cups)
    for _ in range(moves):
        first_of_3 = circle.pickup_next3()
        dest = circle.find_destination(first_of_3)  #
        circle.insert_nodes_after_dest(dest, first_of_3)  #
        circle.current = circle.current.right
    cup1 = circle.values[1]
    return cup1.right.value * cup1.right.right.value
