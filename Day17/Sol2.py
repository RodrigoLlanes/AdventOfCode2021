from math import sqrt
import re


def main():
    left, right, bottom, top = \
        [list(map(int, list(re.findall("-?[0-9]+", line)))) for line in open("input.txt", "r").readlines()][0]

    max_vy = abs(bottom) - 1
    min_vy = bottom

    min_vx = int(sqrt(left * 2 + 1 / 4) - 1 / 2)
    max_vx = right

    sols = 0
    for vy in range(min_vy, max_vy + 1):
        for vx in range(min_vx, max_vx + 1):
            x, y = 0, 0
            dvx, dvy = 0, 0
            while x <= right and y >= bottom:
                if left <= x <= right and top >= y >= bottom:
                    sols += 1
                    break
                x += vx - dvx
                y += vy + dvy
                dvy -= 1
                dvx = min(vx, dvx+1)

    print(sols)


if __name__ == "__main__":
    main()
