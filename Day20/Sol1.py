from copy import deepcopy


def parse(x, y, data, default):
    res = [data.get((x + dx, y + dy), default) for dy in range(-1, 2) for dx in range(-1, 2)]
    res = ''.join(['1' if sym == '#' else '0' for sym in res])
    return int(res, 2)


def print_data(data):
    min_y, max_y = min(y for _, y in data.keys()), max(y for _, y in data.keys())
    min_x, max_x = min(x for x, _ in data.keys()), max(x for x, _ in data.keys())
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            print(data[x, y], end="")
        print()


def main():
    inp = [line.strip() for line in open("input.txt", "r").readlines()]

    alg = inp[0]
    min_y, max_y = 0, len(inp) - 2
    min_x, max_x = 0, len(inp[2])
    data = {}
    for y, line in enumerate(inp[2:]):
        for x, sym in enumerate(line):
            data[x, y] = sym

    for step in range(2):
        min_y, max_y = min_y-1, max_y+1
        min_x, max_x = min_x-1, max_x+1
        background = "." if step % 2 == 0 else "#"
        new_data = deepcopy(data)
        for x in range(min_x-1, max_x+2):
            for y in range(min_y - 1, max_y + 2):
                new_data[x, y] = alg[parse(x, y, data, background)]
        data = new_data

    print(sum(1 for sym in data.values() if sym == "#"))


if __name__ == "__main__":
    main()
