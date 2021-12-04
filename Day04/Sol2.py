from copy import copy


def solve(boards):
    for n in numbers:
        for board in copy(boards):
            for row in range(5):
                if n in board[row]:
                    index = board[row].index(n)
                    board[row][index] = -1
                    if all(num == -1 for num in board[row]) or all([r[index] == -1 for r in board]):
                        if len(boards) == 1:
                            return sum(sum(c for c in r if c != -1) for r in board) * n
                        else:
                            boards.remove(board)
                            break


if __name__ == "__main__":
    data = [line.strip() for line in open("input.txt", "r").readlines()]

    numbers = list(map(int, data[0].split(",")))

    boards = []
    for i in range(2, len(data), 6):
        boards.append([list(map(int, row.split())) for row in data[i: i + 5]])

    print(solve(boards))



