import re
from collections import defaultdict, Counter
from copy import copy


# Inefficient implementation (Efficient implementation on part 2)
def main():
    data = [line.strip() for line in open("input.txt", "r").readlines()]
    pattern = list(data[0])

    raw_insertions = [list(re.match(r"(\w+) -> (\w+)", line).groups()) for line in data[2:]]
    insertions = defaultdict(dict)
    for (k, v) in raw_insertions:
        insertions[k[0]][k[1]] = v

    for n in range(10):
        new_pattern = copy(pattern)
        d = 0
        for i in range(len(pattern)-1):
            if pattern[i] in insertions and pattern[i+1] in insertions[pattern[i]]:
                new_pattern.insert(i+1+d, insertions[pattern[i]][pattern[i+1]])
                d += 1
        pattern = new_pattern

    count = Counter(pattern).most_common()
    print(count[0][1] - count[-1][1])


if __name__ == "__main__":
    main()
