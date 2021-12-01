
if __name__ == "__main__":
    data = [int(line.strip()) for line in open("input.txt", "r").readlines()]

    inc = 0
    for i in range(1, len(data)):
        if data[i-1] < data[i]:
            inc += 1

    print(inc)
