import math
import heapq
from copy import deepcopy


def is_solution(state):
    return {(3, 2): 'A', (3, 3): 'A',
            (5, 2): 'B', (5, 3): 'B',
            (7, 2): 'C', (7, 3): 'C',
            (9, 2): 'D', (9, 3): 'D'} == state


def valid_dest(char, x, y, nx, ny, state):
    char_x = {'A': 3, 'B': 5, 'C': 7, 'D': 9}[char]
    # Overlapping
    if x == nx and y == ny:
        return False
    if (nx, ny) in state:
        return False

    if ny == 1:
        # Go out of valid home
        if x == char_x and ((char_x, 2) not in state or state[char_x, 2] == char) and \
                           ((char_x, 3) not in state or state[char_x, 3] == char):
            return False
        # Moving on hallway
        elif y == 1:
            return False

    # Move inside home
    if ny == 2 and y == 3 and x == char_x:
        return False

    # Move to invalid home
    if ny > 1 and (nx != char_x or ((char_x, 2) in state and state[char_x, 2] != char) or \
                                   ((char_x, 3) in state and state[char_x, 3] != char)):
        return False
    return True


def main():
    data = [line[:-1] for line in open("input.txt", "r").readlines()]
    edges = {}
    length = {}
    state = {}
    char_cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == "#":
                continue
            elif char == ".":
                n = sum(1 for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)] if
                        data[y + dy][x + dx] == "." or data[y + dy][x + dx].isalpha())
                if n == 2 and data[y][x + 2] == "." and data[y][x - 2] == ".":
                    edges[x, y] = [(x - 2, y), (x + 2, y), (x + 1, y + 1), (x - 1, y + 1)]
                    length[x, y] = [2, 2, 2, 2]
                elif n == 2 and data[y][x + 2] == ".":
                    edges[x, y] = [(x - 1, y), (x + 2, y), (x + 1, y + 1)]
                    length[x, y] = [1, 2, 2]
                elif n == 2 and data[y][x - 2] == ".":
                    edges[x, y] = [(x + 1, y), (x - 2, y), (x - 1, y + 1)]
                    length[x, y] = [1, 2, 2]
                elif n == 1 and data[y][x - 1] == ".":
                    edges[x, y] = [(x - 1, y)]
                    length[x, y] = [1]
                elif n == 1 and data[y][x + 1] == ".":
                    edges[x, y] = [(x + 1, y)]
                    length[x, y] = [1]
            elif char.isalpha():
                state[x, y] = char
                n = sum(
                    1 for dx, dy in [(0, -1), (0, 1)] if data[y + dy][x + dx] == "." or data[y + dy][x + dx].isalpha())
                if n == 2:
                    edges[x, y] = [(x, y + 1), (x + 1, y - 1), (x - 1, y - 1)]
                    length[x, y] = [1, 2, 2]
                elif n == 1:
                    edges[x, y] = [(x, y - 1)]
                    length[x, y] = [1]

    def available_jumps(x, y, state):
        available = []
        expand = [(0, x, y)]
        heapq.heapify(expand)
        visited = [(x, y)]
        while len(expand) > 0:
            cost, ex, ey = heapq.heappop(expand)
            for (nx, ny), l in zip(edges[ex, ey], length[ex, ey]):
                if (nx, ny) in visited:
                    continue
                visited.append((nx, ny))
                if (nx, ny) in state:
                    continue
                available.append((nx, ny, cost + l))
                heapq.heappush(expand, (cost + l, nx, ny))
        return sorted(available, key=lambda x: x[2])

    minimum = math.inf
    mem = {}

    def branch(state, score):
        nonlocal minimum
        nonlocal mem
        if score >= minimum:
            return math.inf
        mutable_state = dict(state)
        if is_solution(mutable_state):
            minimum = min(minimum, score)
            return 0
        if state not in mem:
            res_scores = []
            for (x, y), char in mutable_state.items():
                for nx, ny, cost in available_jumps(x, y, mutable_state):
                    if valid_dest(char, x, y, nx, ny, mutable_state):
                        new_state = deepcopy(mutable_state)
                        del new_state[(x, y)]
                        new_state[nx, ny] = char
                        res_scores.append(cost * char_cost[char] + branch(tuple(new_state.items()), score + cost * char_cost[char]))
            mem[state] = min(res_scores, default=math.inf)
        return mem[state]

    print(branch(tuple(state.items()), 0))


if __name__ == "__main__":
    main()
