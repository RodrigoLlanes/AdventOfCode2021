import re
from collections import defaultdict
from copy import deepcopy


def main():
    data = [line.strip() for line in open("input.txt", "r").readlines()]
    raw_pattern = data[0]

    values = defaultdict(int, {k: raw_pattern.count(k) for k in set(list(raw_pattern))})

    pattern = defaultdict(int)
    for i in range(len(raw_pattern)-1):
        pair = raw_pattern[i:i+2]
        pattern[pair] += 1

    insertions = [list(re.match(r"(\w+) -> (\w+)", line).groups()) for line in data[2:]]
    insertions = {k: v for (k, v) in insertions}

    for n in range(40):
        new_pattern = deepcopy(pattern)
        for (k, v) in pattern.items():
            if k in insertions:
                inserted = insertions[k]
                new_pattern[k] -= v
                new_pattern[k[0] + inserted] += v
                new_pattern[inserted + k[1]] += v
                values[inserted] += v
        pattern = new_pattern

    print(max(values.values()) - min(values.values()))


if __name__ == "__main__":
    main()
