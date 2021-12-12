import re
from collections import defaultdict


def main():
    data = [list(re.findall(r"[a-zA-Z]+", line)) for line in open("input.txt", "r").readlines()]

    graph = defaultdict(set)
    for start, end in data:
        graph[start].add(end)
        graph[end].add(start)

    def ramificate(steps):
        curr = steps[-1]
        if curr == "end":
            return 1
        sols = 0
        for neighbour in graph[curr]:
            if not neighbour.islower() or neighbour not in steps:
                sols += ramificate(steps + [neighbour])
        return sols

    print(ramificate(["start"]))


if __name__ == "__main__":
    main()
