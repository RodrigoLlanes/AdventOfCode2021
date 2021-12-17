import re


def main():
    left, right, bottom, top = \
        [list(map(int, list(re.findall("-?[0-9]+", line)))) for line in open("input.txt", "r").readlines()][0]

    vy = abs(bottom) - 1

    print(vy*(vy+1)/2)


if __name__ == "__main__":
    main()
