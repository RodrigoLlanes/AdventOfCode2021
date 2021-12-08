
if __name__ == "__main__":
    data = [line.strip().split("|") for line in open("input.txt", "r").readlines()]
    inputs = [inp.split() for inp, _ in data]
    outputs = [out.split() for _, out in data]

    res = 0
    for line in outputs:
        res += sum((len(out) == 7 or len(out) == 2 or len(out) == 3 or len(out) == 4) for out in line)

    print(res)
