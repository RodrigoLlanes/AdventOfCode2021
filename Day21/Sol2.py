import re
from functools import cache


def roll_dice():
    return [a + b + c for a in range(1, 4) for b in range(1, 4) for c in range(1, 4)]


@cache
def play(p0, p1, s0, s1):
    res = [0, 0]
    for i in roll_dice():
        np0 = ((p0 - 1 + i) % 10) + 1
        ns0 = s0 + np0
        if ns0 >= 21:
            res[0] += 1
        else:
            for j in roll_dice():
                np1 = ((p1 - 1 + j) % 10) + 1
                ns1 = s1 + np1
                if ns1 >= 21:
                    res[1] += 1
                else:
                    part = play(np0, np1, ns0, ns1)
                    res = [x + y for (x, y) in zip(res, part)]
    return tuple(res)


def main():
    data = [re.findall("[0-9]+", line.strip()) for line in open("input.txt", "r").readlines()]
    positions = {int(player)-1: int(pos) for (player, pos) in data}
    print(max(play(positions[0], positions[1], 0, 0)))


if __name__ == "__main__":
    main()
