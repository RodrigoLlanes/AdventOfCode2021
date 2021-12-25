from copy import deepcopy


def move(data, cucumber, dx, dy):
    new_data = deepcopy(data)
    change = False
    for y, line in enumerate(data):
        for x, sym in enumerate(line):
            if sym == cucumber and data[(y+dy) % len(data)][(x+dx) % len(line)] == '.':
                change = True
                new_data[y][x] = '.'
                new_data[(y+dy) % len(data)][(x+dx) % len(line)] = sym
    return change, new_data


def main():
    data = [list(line.strip()) for line in open("input.txt", "r").readlines()]

    step = 0
    east_change = south_change = True
    while east_change or south_change:
        east_change, data = move(data, '>', 1, 0)
        south_change, data = move(data, 'v', 0, 1)
        step += 1

    print(step)


if __name__ == "__main__":
    main()
