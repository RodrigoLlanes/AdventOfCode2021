from copy import deepcopy, copy
from itertools import combinations_with_replacement, combinations, permutations
from math import ceil
import re


def transform(pos, axis, up):
    if up == 0:
        return pos[0] * axis[0], pos[1] * axis[1], pos[2] * axis[2]
    elif up == 1:
        return pos[1] * axis[1], pos[0] * axis[0], pos[2] * axis[2]
    elif up == 2:
        return pos[0] * axis[0], pos[2] * axis[2], pos[1] * axis[1]


def relative(pos, piv=(0, 0, 0), dis=(0, 0, 0)):
    return tuple([a - p + d for (a, p, d) in zip(pos, piv, dis)])


def main():
    inp = [line.strip() for line in open("test.txt", "r").readlines()]

    data = {}
    curr = None
    for line in inp:
        header = re.match(r"--- scanner ([0-9]+) ---", line)
        coord = re.findall(r"-?[0-9]+", line)
        if line == "":
            continue
        elif header:
            curr = int(header.group(1))
            data[curr] = []
        else:
            data[curr].append(tuple([int(d) for d in coord]))

    def find(_beacons, curr):
        for ax in [(1, 1, 1), (1, -1, 1), (1, 1, -1), (-1, 1, 1), (-1, -1, 1), (-1, 1, -1), (1, -1, -1), (-1, -1, -1)]:
            for up in range(3):
                beacons = [transform(beacon, ax, up) for beacon in _beacons]
                for beacon0, beacon1 in combinations(beacons, 2):
                    for known0, known1 in combinations(curr, 2):
                        if relative(beacon0, piv=beacon1) == relative(known0, piv=known1):
                            dis = relative(known0, piv=beacon0)
                            overlap = 0
                            for beacon2 in beacons:
                                if relative(beacon2, dis=dis) in curr:
                                    overlap += 1
                                    if overlap >= 12:
                                        break
                            if overlap >= 12:
                                new = [relative(beacon, dis=dis) for beacon in beacons]
                                return set(new)

                        elif relative(beacon1, piv=beacon0) == relative(known0, piv=known1):
                            dis = relative(known0, piv=beacon1)
                            overlap = 0
                            for beacon2 in beacons:
                                if relative(beacon2, dis=dis) in curr:
                                    overlap += 1
                                    if overlap >= 12:
                                        break
                            if overlap >= 12:
                                new = [relative(beacon, dis=dis) for beacon in beacons]
                                return set(new)

    data = [set(v) for v in data.values()]
    clear = [data[0]]
    queue = list(data[1:])
    while len(queue) > 0:
        print(len(clear))
        b = queue.pop(0)
        for c in clear:
            res = find(b, c)
            if res is not None:
                clear.append(res)
                break
            else:
                queue.append(b)
    print(clear)



if __name__ == "__main__":
    main()
