import re


def main():
    data = [re.match(r"(on|off) x=(-?[0-9]+)..(-?[0-9]+),y=(-?[0-9]+)..(-?[0-9]+),z=(-?[0-9]+)..(-?[0-9]+)", line.strip()).groups()
            for line in open("input.txt", "r").readlines()]
    data = [(act == "on", int(x0), int(x1), int(y0), int(y1), int(z0), int(z1)) for (act, x0, x1, y0, y1, z0, z1) in data]

    cubes = {}
    _min = -50
    _max = 50
    for act, x0, x1, y0, y1, z0, z1 in data:
        if x1 >= _min and x0 <= _max and y1 >= _min and y0 <= _max and z1 >= _min and z0 <= _max:
            for x in range(max(x0, _min), min(x1, _max)+1):
                for y in range(max(y0, _min), min(y1, _max)+1):
                    for z in range(max(z0, _min), min(z1, _max)+1):
                        cubes[x, y, z] = act

    print(sum(1 for v in cubes.values() if v))


if __name__ == "__main__":
    main()
