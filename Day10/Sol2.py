from statistics import median

opening = {")": "(", "]": "[", "}": "{", ">": "<"}
completion_points = {"(": 1, "[": 2, "{": 3, "<": 4}

if __name__ == "__main__":
    data = [list(line.strip()) for line in open("input.txt", "r").readlines()]

    scores = []
    for line in data:
        stack = []
        for c in line:
            if c in opening.values():
                stack.append(c)
            else:
                last = stack.pop()
                if last != opening[c]:
                    break
        else:
            score = 0
            while len(stack) > 0:
                score *= 5
                score += completion_points[stack.pop()]
            scores.append(score)

    print(median(scores))
