from z3 import *


def main():
    data = [line.strip().split() for line in open("input.txt", "r").readlines()]
    params = [[int(data[i+j][-1]) for j in [4, 5, 15]] for i in range(0, len(data), 18)]
    inputs = [Int(f'inp_{i}') for i in range(14)]

    opt = Optimize()
    val = z = 0
    for inp, (a, b, c) in zip(inputs, params):
        val = val * 10 + inp
        opt.add(And(inp >= 1, inp <= 9))
        z = If(z % 26 + b != inp,
               z / a * 26 + inp + c,
               z / a)
    opt.add(z == 0)

    opt.minimize(val)
    assert opt.check() == sat
    print(opt.model().eval(val))


if __name__ == "__main__":
    main()
