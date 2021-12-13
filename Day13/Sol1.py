import re


def main():
    dots_re = re.compile(r"([0-9]+),([0-9]+)")
    dots = [list(dots_re.match(line).groups()) for line in open("input.txt", "r").readlines() if dots_re.match(line)]
    dots = set([(int(dot[0]), int(dot[1])) for dot in dots])

    fold_re = re.compile(r"fold along ([xy])=([0-9]+)")
    folds = [list(fold_re.match(line).groups()) for line in open("input.txt", "r").readlines() if fold_re.match(line)]
    folds = [(fold[0], int(fold[1])) for fold in folds]

    for ax, line in folds[0:1]:
        if ax == "x":
            new_dots = set([(x, y) for (x, y) in dots if x < line])
            new_dots.update([(2 * line - x, y) for (x, y) in dots if x > line])
            dots = new_dots
        else:
            new_dots = set([(x, y) for (x, y) in dots if y < line])
            new_dots.update([(x, 2 * line - y) for (x, y) in dots if y > line])
            dots = new_dots

    print(len(dots))


if __name__ == "__main__":
    main()
