import math
from functools import cache

A, B, C, D = 'A', 'B', 'C', 'D'

TARGET_STATE = (
    (None,) * 11,
    (A, A, A, A),
    (B, B, B, B),
    (C, C, C, C),
    (D, D, D, D)
)

COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

HALLS = {1: 2, 2: 4, 3: 6, 4: 8}
INVERSE_HALLS = {2: 1, 4: 2, 6: 3, 8: 4}

TARGETS = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
INVERSE_TARGETS = {2: 'A', 4: 'B', 6: 'C', 8: 'D'}

HALLWAY = set(spot for spot in range(11) if spot not in HALLS.values())


def is_solution(state):
    return TARGET_STATE == state


def check_room(state, hall):
    x = HALLS[hall]
    return all(amp is None or amp == INVERSE_TARGETS[x] for amp in state[hall])


def reachable(state, start, end):
    sign = int(math.copysign(1, end - start))
    return all(state[0][step] is None for step in range(start + sign, end + sign, sign))


def insert_last_free(state, hall, amp):
    i = 0
    while i < 3:
        if state[hall][i + 1] is not None:
            break
        i += 1
    state[hall][i] = amp
    return (i + 1) * COSTS[amp]


def available_steps(state):
    for hall, x in HALLS.items():
        for depth, amp in enumerate(state[hall]):
            if amp is None:
                continue
            if amp == INVERSE_TARGETS[x] and check_room(state, hall):
                continue
            cost = COSTS[amp] * (depth + 1)
            available = []
            for spot in HALLWAY:
                if spot > x and state[0][spot] is not None:
                    break
                mutable_state = list(map(list, state))
                mutable_state[0][spot] = amp
                mutable_state[hall][depth] = None
                available.append((tuple(map(tuple, mutable_state)), cost + abs(x - spot) * COSTS[amp]))
                if spot < x and state[0][spot] is not None:
                    available.clear()
            for step in available:
                yield step
            break

    for spot in HALLWAY:
        amp = state[0][spot]
        if amp is None:
            continue
        t = TARGETS[amp]
        hall = INVERSE_HALLS[t]
        if check_room(state, hall) and reachable(state, spot, t):
            mutable_state = list(map(list, state))
            mutable_state[0][spot] = None
            cost = insert_last_free(mutable_state, hall, amp)
            yield tuple(map(tuple, mutable_state)), cost + abs(spot - t) * COSTS[amp]


def main():
    data = [line[:-1] for line in open("input2.txt", "r").readlines()]
    original_state = [
        [None, ] * 11,
        [None] * 4,
        [None] * 4,
        [None] * 4,
        [None] * 4
    ]
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char.isalpha():
                original_state[INVERSE_HALLS[x-1]][y - 2] = char

    @cache
    def branch(state):
        if is_solution(state):
            return 0
        costs = []
        for step, cost in available_steps(state):
            costs.append(cost + branch(step))
        return min(costs, default=math.inf)

    print(branch(tuple(map(tuple, original_state))))


if __name__ == "__main__":
    main()
