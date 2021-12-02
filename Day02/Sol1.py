
if __name__ == "__main__":
    data = [line.strip().split() for line in open("input.txt", "r").readlines()]
    data = [(order, int(x)) for order, x in data]

    depth = pos = 0
    for order, x in data:
        if order == "forward":
            pos += x
        elif order == "up":
            depth -= x
        elif order == "down":
            depth += x

    print(pos * depth)
