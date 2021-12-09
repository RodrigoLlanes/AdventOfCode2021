
if __name__ == "__main__":
    data = [list(map(int, list(line.strip()))) for line in open("input.txt", "r").readlines()]
    res = 0
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if all(data[ny][nx] > c for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] if
                   (len(data) > ny >= 0) and (len(data[ny]) > nx >= 0)):
                res += 1 + c
    print(res)
