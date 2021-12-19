from copy import deepcopy
import re


def manhattan(p0, p1):
    return sum(abs(d0 - d1) for (d0, d1) in zip(p0, p1))


def transform_set(beacons, orientation):
    return set(transform(pos, orientation) for pos in beacons)


def transform(pt, orientation):
    a, b, c = pt
    return (
        (+a, +b, +c), (+b, +c, +a), (+c, +a, +b), (+c, +b, -a), (+b, +a, -c), (+a, +c, -b),
        (+a, -b, -c), (+b, -c, -a), (+c, -a, -b), (+c, -b, +a), (+b, -a, +c), (+a, -c, +b),
        (-a, +b, -c), (-b, +c, -a), (-c, +a, -b), (-c, +b, +a), (-b, +a, +c), (-a, +c, +b),
        (-a, -b, +c), (-b, -c, +a), (-c, -a, +b), (-c, -b, -a), (-b, -a, -c), (-a, -c, -b)
    )[orientation]


def relative_set(beacons, piv=(0, 0, 0), dis=(0, 0, 0)):
    return set(relative(pos, piv, dis) for pos in beacons)


def relative(pos, piv=(0, 0, 0), dis=(0, 0, 0)):
    return tuple([a - p + d for (a, p, d) in zip(pos, piv, dis)])


def match(_beacons, curr):
    curr_relatives = {piv: relative_set(curr, piv) for piv in curr}
    for orientation in range(24):
        beacons = {piv: transform_set(beacons, orientation) for (piv, beacons) in _beacons.items()}
        for beacon, b_rel in beacons.items():
            for pivot, p_rel in curr_relatives.items():
                if len(set.intersection(b_rel, p_rel)) >= 12:
                    scan = relative(transform(relative((0, 0, 0), piv=beacon), orientation), dis=pivot)
                    return relative_set(b_rel, dis=pivot), scan
    return None


def main():
    inp = [line.strip() for line in open("input.txt", "r").readlines()]

    data = []
    for line in inp:
        header = re.match(r"--- scanner ([0-9]+) ---", line)
        coord = re.findall(r"-?[0-9]+", line)
        if line == "":
            continue
        elif header:
            data.append(set())
        else:
            data[-1].add(tuple([int(d) for d in coord]))

    relatives = [{piv: relative_set(group, piv) for piv in group} for group in data]

    aligned = deepcopy(data[0])
    queue = deepcopy(relatives[1:])
    scanners = [(0, 0, 0)]
    while len(queue) > 0:
        b = queue.pop(0)
        res = match(b, aligned)
        if res is not None:
            al, scan = res
            aligned = aligned.union(al)
            scanners.append(scan)
        else:
            queue.append(b)

    m = manhattan(scanners[0], scanners[1])
    for a in scanners:
        for b in scanners:
            if a != b:
                m = max(m, manhattan(a, b))

    print(m)


if __name__ == "__main__":
    main()
