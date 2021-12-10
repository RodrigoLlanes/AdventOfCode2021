
opening = {")": "(", "]": "[", "}": "{", ">": "<"}
error_points = {")": 3, "]": 57, "}": 1197, ">": 25137}

if __name__ == "__main__":
    data = [list(line.strip()) for line in open("input.txt", "r").readlines()]

    score = 0
    for line in data:
        stack = []
        for c in line:
            if c in opening.values():
                stack.append(c)
            else:
                last = stack.pop()
                if last != opening[c]:
                    score += error_points[c]
                    break

    print(score)
