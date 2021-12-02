
if __name__ == "__main__":
    data = [line.strip().split() for line in open("input.txt", "r").readlines()]
    data = [(order, int(x)) for order, x in data]

    depth = pos = aim = 0
    for order, x in data:
        if order == "forward":
            pos += x
            depth += aim * x
        elif order == "up":
            aim -= x
        elif order == "down":
            aim += x

    print(pos * depth)
