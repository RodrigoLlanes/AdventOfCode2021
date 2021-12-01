if __name__ == "__main__":
    data = [int(line.strip()) for line in open("input.txt", "r").readlines()]

    inc = 0
    for i in range(1, len(data) - 2):
        prev = data[i - 1] + data[i] + data[i + 1]
        curr = data[i] + data[i + 1] + data[i + 2]
        if prev < curr:
            inc += 1

    print(inc)
