from functools import reduce

if __name__ == "__main__":
    data = [list(map(int, list(line.strip()))) for line in open("input.txt", "r").readlines()]

    basins = {}
    res = 0
    for level in range(0, 9):
        for y, row in enumerate(data):
            for x, c in enumerate(row):
                if c != level:
                    continue
                if all(data[ny][nx] > c for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] if
                       (len(data) > ny >= 0) and (len(data[ny]) > nx >= 0)):
                    data[y][x] = min(basins.keys(), default=0)-1
                    basins[data[y][x]] = 1
                else:
                    for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                        if (len(data) > ny >= 0) and (len(data[ny]) > nx >= 0):
                            if data[ny][nx] < 0:
                                data[y][x] = data[ny][nx]
                                basins[data[ny][nx]] += 1
                                break

    basins = list(sorted(list(basins.values()), reverse=True))
    print(reduce(lambda a, b: a * b, basins[:3]))
