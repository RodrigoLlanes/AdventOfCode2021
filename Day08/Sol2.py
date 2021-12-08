
if __name__ == "__main__":
    data = [line.strip().split("|") for line in open("input.txt", "r").readlines()]
    inputs = [[set(list(digit)) for digit in inp.split()] for inp, _ in data]
    outputs = [[set(list(digit)) for digit in out.split()] for _, out in data]

    res = 0
    for inp, out in zip(inputs, outputs):
        code = [set()] * 10
        code[1] = [digit for digit in inp if len(digit) == 2][0]
        code[4] = [digit for digit in inp if len(digit) == 4][0]
        code[7] = [digit for digit in inp if len(digit) == 3][0]
        code[8] = [digit for digit in inp if len(digit) == 7][0]

        code[9] = [digit for digit in inp if len(digit) == 6 and len(digit - set.union(code[4], code[7])) == 1][0]
        code[6] = [digit for digit in inp if len(digit) == 6 and len(set.intersection(digit, code[1])) == 1][0]
        code[0] = [digit for digit in inp if len(digit) == 6 and digit != code[6] and digit != code[9]][0]

        code[5] = [digit for digit in inp if len(digit) == 5 and len(code[6] - digit) == 1][0]
        code[3] = [digit for digit in inp if len(digit) == 5 and digit != code[5] and len(code[9] - digit) == 1][0]
        code[2] = [digit for digit in inp if len(digit) == 5 and digit != code[3] and digit != code[5]][0]

        value = 0
        for digit in out:
            value *= 10
            value += code.index(set(list(digit)))
        res += value
    print(res)
