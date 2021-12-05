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
        else:
            dx = -1 if x1 > x2 else 1
            dy = -1 if y1 > y2 else 1

            for x, y in zip(range(x1, x2+dx, dx), range(y1, y2+dy, dy)):
                over[x, y] += 1

    print(sum(v > 1 for v in over.values()))
