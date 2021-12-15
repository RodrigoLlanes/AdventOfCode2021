from heapq import heappop, heappush


def main():
    data = [list(map(int, list(line.strip()))) for line in open("input.txt", "r").readlines()]
    end = (len(data[0])-1, len(data)-1)

    heap = [(0, (0, 0))]
    visited = set()

    while len(heap) > 0:
        risk, pos = heappop(heap)
        if pos in visited:
            continue
        visited.add(pos)

        if pos == end:
            print(risk)
            break

        for (x, y) in [(pos[0]+dx, pos[1]+dy) for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]]:
            if (0 <= x <= end[0]) and (0 <= y <= end[1]):
                heappush(heap, (risk + data[y][x], (x, y)))


if __name__ == "__main__":
    main()
