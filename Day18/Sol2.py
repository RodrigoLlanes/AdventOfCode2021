from copy import deepcopy
from math import ceil


class Node:
    def __init__(self, prev=None, right=None, left=None, value=None):
        self.prev = prev
        self.right = right
        self.left = left
        self.value = value

    def __add__(self, other):
        left = deepcopy(self)
        right = deepcopy(other)
        res = Node(left=left, right=right)
        left.prev = res
        right.prev = res

        while res.reduce():
            continue

        return res

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.right == other.right and self.left == other.left and self.value == other.value
        return False

    def is_leaf(self):
        return self.value is not None

    def level(self):
        level = 0
        node = self
        while node.prev is not None:
            level += 1
            node = node.prev
        return level

    def root(self):
        root = self
        while root.prev is not None:
            root = root.prev
        return root

    def reduce(self):
        if self.reduce_explode():
            return True
        return self.reduce_split()

    def reduce_explode(self):
        if self.is_leaf():
            return False
        if self.right.is_leaf() and self.left.is_leaf() and self.level() >= 4:
            self.explode()
            return True
        if self.left.reduce_explode():
            return True
        if self.right.reduce_explode():
            return True

    def reduce_split(self):
        if self.is_leaf():
            if self.value >= 10:
                self.split()
                return True
            return False

        if self.left.reduce_split():
            return True
        if self.right.reduce_split():
            return True

    def explode(self):
        self.add_near_left(self.left.value)
        self.add_near_right(self.right.value)

        self.right = None
        self.left = None
        self.value = 0

    def split(self):
        self.left = Node(prev=self, value=self.value//2)
        self.right = Node(prev=self, value=ceil(self.value/2))
        self.value = None

    def add_near_left(self, n):
        if self.prev is None:
            return

        if self.prev.left is self:
            return self.prev.add_near_left(n)

        node = self.prev.left
        while not node.is_leaf():
            node = node.right

        node.value += n

    def add_near_right(self, n):
        if self.prev is None:
            return

        if self.prev.right is self:
            return self.prev.add_near_right(n)

        node = self.prev.right
        while not node.is_leaf():
            node = node.left

        node.value += n

    def __str__(self):
        if self.is_leaf():
            return str(self.value)
        return "[" + str(self.left) + ", " + str(self.right) + "]"

    def __repr__(self):
        return str(self)

    def magnitud(self):
        if self.is_leaf():
            return self.value
        return self.left.magnitud() * 3 + self.right.magnitud() * 2


def cast(line):
    res = Node()
    for c in line[1:-1]:
        if c == '[':
            if res.left is None:
                res.left = Node(prev=res)
                res = res.left
            else:
                res.right = Node(prev=res)
                res = res.right
        elif c == ']':
            res = res.prev
        elif c.isalnum():
            if res.left is None:
                res.left = Node(prev=res, value=int(c))
            else:
                res.right = Node(prev=res, value=int(c))
    return res


def main():
    data = [cast(line.strip()) for line in open("input.txt", "r").readlines()]

    res = 0
    for i, a in enumerate(data):
        for j, b in enumerate(data):
            if a != b:
                res = max(res, (a+b).magnitud(), (b+a).magnitud())
    print(res)


if __name__ == "__main__":
    main()
