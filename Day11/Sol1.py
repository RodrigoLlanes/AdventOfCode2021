
if __name__ == "__main__":
    data = [list(map(int, list(line.strip()))) for line in open("input.txt", "r").readlines()]

    flashes = 0
    for _ in range(100):
        flashed = []
        static = False
        data = [[cell + 1 for cell in row] for row in data]
        while not static:
            static = True
            for y, row in enumerate(data):
                for x, cell in enumerate(row):
                    if cell > 9 and (x, y) not in flashed:
                        flashed.append((x, y))
                        flashes += 1
                        static = False
                        for dy in range(-1, 2):
                            for dx in range(-1, 2):
                                if 0 <= y+dy < len(data) and 0 <= x+dx < len(data[y]):
                                    data[y+dy][x+dx] += 1
        data = [[cell if cell <= 9 else 0 for cell in row] for row in data]

    print(flashes)
