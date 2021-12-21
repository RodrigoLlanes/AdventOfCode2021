import re


def roll_dice(dice):
    res = 0
    for _ in range(3):
        if dice == 101:
            dice = 1
        res += dice
        dice += 1
    return res


def main():
    data = [re.findall("[0-9]+", line.strip()) for line in open("input.txt", "r").readlines()]
    positions = {int(player)-1: int(pos) for (player, pos) in data}
    scores = {int(player)-1: 0 for (player, pos) in data}
    rolls = 0
    dice = 1
    while True:
        for player in range(2):
            rolls += 3
            moves = roll_dice(dice)
            dice = ((dice + 2) % 100) + 1
            positions[player] = ((positions[player] - 1 + moves) % 10) + 1
            scores[player] += positions[player]
            if scores[player] >= 1000:
                return scores[(player + 1) % 2] * rolls


if __name__ == "__main__":
    print(main())
