from collections import defaultdict

if __name__ == "__main__":
    data = [list(map(int, line.strip().split(","))) for line in open("input.txt", "r").readlines()][0]
    data = {c: data.count(c) for c in set(data)}

    for _ in range(256):
        new_data = defaultdict(int)
        for c, v in data.items():
            if c > 0:
                new_data[c-1] += v
            else:
                new_data[6] += v
                new_data[8] += v
        data = new_data

    print(sum(v for v in data.values()))

