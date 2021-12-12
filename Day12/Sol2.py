import re
from collections import defaultdict


def main():
    data = [list(re.findall(r"[a-zA-Z]+", line)) for line in open("input.txt", "r").readlines()]

    graph = defaultdict(set)
    for start, end in data:
        if end != "start":
            graph[start].add(end)
        if start != "start":
            graph[end].add(start)

    def ramificate(steps, twice=False):
        curr = steps[-1]
        if curr == "end":
            return 1
        sols = 0
        for neighbour in graph[curr]:
            if not neighbour.islower() or neighbour not in steps:
                sols += ramificate(steps + [neighbour], twice)
            elif not twice:
                sols += ramificate(steps + [neighbour], True)
        return sols

    print(ramificate(["start"]))


if __name__ == "__main__":
    main()
