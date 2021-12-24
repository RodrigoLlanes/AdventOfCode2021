# [Día 23](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 23  | 04:59:46 | 3992 | 0     | 08:06:31 | 2897 | 0     |

## [Parte 1](./Sol1b.py)
Esta primera parte viene cargadita, el objetivo parece sencillo, llevar a todos los anfípodos, a sus respectivas habitaciones,
pero este problema aparentemente sencillo, debido a las normas del reto, tiene un coste computacional altísimo, por lo que hay
que tirar de estructuras de datos y algoritmos lo más eficientes posibles.

[Mi primera solución](./Sol1a.py) para este reto no era tan bonita como esta que veis a continuación, y muchísimo menos eficiente, 
motivo por el cual tras casi 6h de programación infructuosas, decidí ojear soluciones de otros usuarios para ver su método de resolución,
y así es como me topé con la [solución Allan Taylor](https://github.com/AllanTaylor314/AdventOfCode/blob/main/2021/23a.py), que tras un rato de lectura calmada
y habiéndola entendido por fin, implementé a mi manera, como tenéis a continuación.
```python3
import math
from functools import cache

A, B, C, D = 'A', 'B', 'C', 'D'

TARGET_STATE = (
    (None,) * 11,
    (A, A),
    (B, B),
    (C, C),
    (D, D)
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
    while i < 1:
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
    data = [line[:-1] for line in open("input.txt", "r").readlines()]
    original_state = [
        [None, ] * 11,
        [None, None],
        [None, None],
        [None, None],
        [None, None]
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
```

#### TODO

## [Parte 2](./Sol2.py)

Con una solución como la anterior, adaptarla al segundo reto fue tan simple como añadir las dos líneas al input, modificar el 
estado objetivo y la plantilla del estado inicial.
```python3
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
```