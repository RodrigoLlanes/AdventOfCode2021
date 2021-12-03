from collections import Counter
from copy import copy

if __name__ == "__main__":
    data = [line.strip() for line in open("input.txt", "r").readlines()]

    oxygen = copy(data)
    for i in range(len(data[0])):
        if len(oxygen) == 1:
            break

        c = Counter([line[i] for line in oxygen])
        if c.get("0") > c.get("1"):
            oxygen = list(filter(lambda x: x[i] == "0", oxygen))
        else:
            oxygen = list(filter(lambda x: x[i] == "1", oxygen))

    co2 = copy(data)
    for i in range(len(data[0])):
        if len(co2) == 1:
            break

        c = Counter([line[i] for line in co2])
        if c.get("0") > c.get("1"):
            co2 = list(filter(lambda x: x[i] == "1", co2))
        else:
            co2 = list(filter(lambda x: x[i] == "0", co2))

    print(int("".join(co2), 2) * int("".join(oxygen), 2))

