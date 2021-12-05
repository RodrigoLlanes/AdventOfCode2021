from collections import defaultdict
import re

if __name__ == "__main__":
    data = [list(map(int, re.findall(r"(\d+)", line.strip()))) for line in open("input.txt", "r").readlines()]

    over = defaultdict(int)

    for x1, y1, x2, y2 in data:
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2)+1):
                over[x1, y] += 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2)+1):
                over[x, y1] += 1

    print(sum(v > 1 for v in over.values()))
