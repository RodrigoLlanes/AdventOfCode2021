import re
from copy import deepcopy


def overlap(x00, x01, y00, y01, z00, z01, x10, x11, y10, y11, z10, z11):
    if x01 < x10 or x11 < x00 or y01 < y10 or y11 < y00 or z01 < z10 or z11 < z00:
        return [], [(x00, x01, y00, y01, z00, z01)]
    x_min = max(x00, x10)
    y_min = max(y00, y10)
    z_min = max(z00, z10)
    x_max = min(x01, x11)
    y_max = min(y01, y11)
    z_max = min(z01, z11)

    x_slices = [(x00, x01)]
    if x00 < x_min:
        x_slices = [(x00, x_min - 1), (x_min, x01)]
    if x01 > x_max:
        x_slices = x_slices[:-1] + [(x_slices[-1][0], x_max), (x_max + 1, x01)]

    y_slices = [(y00, y01)]
    if y00 < y_min:
        y_slices = [(y00, y_min - 1), (y_min, y01)]
    if y01 > y_max:
        y_slices = y_slices[:-1] + [(y_slices[-1][0], y_max), (y_max + 1, y01)]

    z_slices = [(z00, z01)]
    if z00 < z_min:
        z_slices = [(z00, z_min - 1), (z_min, z01)]
    if z01 > z_max:
        z_slices = z_slices[:-1] + [(z_slices[-1][0], z_max), (z_max + 1, z01)]

    intersect, rest = [], []
    for (x_min, x_max) in x_slices:
        for (y_min, y_max) in y_slices:
            for (z_min, z_max) in z_slices:
                if x_max < x10 or x11 < x_min or y_max < y10 or y11 < y_min or z_max < z10 or z11 < z_min:
                    rest.append((x_min, x_max, y_min, y_max, z_min, z_max))
                else:
                    intersect.append((x_min, x_max, y_min, y_max, z_min, z_max))
    return intersect, rest


class Figure:
    def __init__(self, cubes=[]):
        self.cubes = cubes

    def intersect(self, other):
        res = []
        for self_cube in self.cubes:
            for other_cube in other.cubes:
                res.extend(overlap(*self_cube, *other_cube)[0])
        return Figure(res)

    def __sub__(self, other):
        res = []
        for self_cube in self.cubes:
            rest = Figure([self_cube])
            for other_cube in other.cubes:
                rest = rest.intersect(Figure(overlap(*self_cube, *other_cube)[1]))
            res.extend(rest.cubes)
        return Figure(res)

    def union(self, other):
        res = (deepcopy(self) - (self.intersect(other))).cubes
        res.extend(other.cubes)
        return Figure(res)

    def volume(self):
        res = 0
        for x0, x1, y0, y1, z0, z1 in self.cubes:
            res += (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1)
        return res


def main():
    data = [re.match(r"(on|off) x=(-?[0-9]+)..(-?[0-9]+),y=(-?[0-9]+)..(-?[0-9]+),z=(-?[0-9]+)..(-?[0-9]+)", line.strip()).groups()
            for line in open("input.txt", "r").readlines()]
    data = [(act == "on", Figure([(int(x0), int(x1), int(y0), int(y1), int(z0), int(z1))])) for (act, x0, x1, y0, y1, z0, z1) in data]

    res = Figure()
    for act, fig in data:
        if act:
            res = res.union(fig)
        else:
            res = res - fig
    print(res.volume())


if __name__ == "__main__":
    main()
