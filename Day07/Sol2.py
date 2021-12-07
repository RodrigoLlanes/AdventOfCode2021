
if __name__ == "__main__":
    data = [list(map(int, line.strip().split(","))) for line in open("input.txt", "r").readlines()][0]
    best = sum(d * (d+1) // 2 for d in data)
    for i in range(min(data), max(data)+1):
        best = min(best, sum(abs(d-i) * (abs(d-i)+1) // 2 for d in data if abs(d-i) > 0))
    print(best)

