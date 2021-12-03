from collections import Counter

if __name__ == "__main__":
    data = [list(line.strip()) for line in open("input.txt", "r").readlines()]
    data = [Counter(bit) for bit in zip(*data)]

    gamma = "".join([max(bit, key=bit.get) for bit in data])
    epsilon = "".join([min(bit, key=bit.get) for bit in data])

    print(int(gamma, 2) * int(epsilon, 2))

