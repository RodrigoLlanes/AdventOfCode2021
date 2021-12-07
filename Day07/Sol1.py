
if __name__ == "__main__":
    data = [list(map(int, line.strip().split(","))) for line in open("input.txt", "r").readlines()][0]
    best = sum(data)
    for i in range(min(data), max(data)):
        prev = min(best, sum(abs(d-i) for d in data))
    print(best)

