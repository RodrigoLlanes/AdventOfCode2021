# [Día 21](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 21  | 00:25:03 | 2633 | 0     | 00:46:19 | 885  | 0     |

## [Parte 1](./Sol1.py)
Esta primera parte es sospechosamente fácil, simplemente tenemos que ir tirando el dado, moviendo las fichas y contando la puntuación,
hasta que uno de los dos jugadores supere los 1000 puntos.
```python3
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
```

La función roll dice, recibe como entrada el siguiente resultado del dado y calcula su suma con las dos siguientes tiradas.
```python3
def roll_dice(dice):
    res = 0
    for _ in range(3):
        if dice == 101:
            dice = 1
        res += dice
        dice += 1
    return res
```

La función principal es muy sencilla, se lee la posición inicial de cada jugador, y se crean dos diccionarios, uno con las posiciones y
otro con las puntuaciones de cada jugador.

Posteriormente se crea un contador para el número de tiradas del dado y otro para llevar la cuenta del siguiente resultado del dado. Una vez hemos
definido todas las variables, iteramos eternamente en los turnos de cada jugador, calculamos su movimiento, incrementamos su posición, su puntuación y si
esta última supera los 1000 puntos devolvemos la puntuación del otro jugador multiplicada por el número de tiradas.
```python3
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
```

## [Parte 2](./Sol2.py)
Como sospechábamos esta segunda parte se complica considerablemente, ahora, cada tirada del dado [divide los universos](https://es.wikipedia.org/wiki/Universos_paralelos), 
nosotros deberemos calcular en cuantos universos gana cada jugador, reduciendo la puntuación requerida a 21.
```python3
import re
from functools import cache


def roll_dice():
    return [a + b + c for a in range(1, 4) for b in range(1, 4) for c in range(1, 4)]


@cache
def play(p0, p1, s0, s1):
    res = [0, 0]
    for i in roll_dice():
        np0 = ((p0 - 1 + i) % 10) + 1
        ns0 = s0 + np0
        if ns0 >= 21:
            res[0] += 1
        else:
            for j in roll_dice():
                np1 = ((p1 - 1 + j) % 10) + 1
                ns1 = s1 + np1
                if ns1 >= 21:
                    res[1] += 1
                else:
                    part = play(np0, np1, ns0, ns1)
                    res = [x + y for (x, y) in zip(res, part)]
    return tuple(res)


def main():
    data = [re.findall("[0-9]+", line.strip()) for line in open("input.txt", "r").readlines()]
    positions = {int(player)-1: int(pos) for (player, pos) in data}
    print(max(play(positions[0], positions[1], 0, 0)))


if __name__ == "__main__":
    main()
```

La función ```roll_dice()``` ahora devuelve una lista con todos los resultados posibles de tirar tres dados de tres caras.
```python3
def roll_dice():
    return [a + b + c for a in range(1, 4) for b in range(1, 4) for c in range(1, 4)]
```

Definimos también una función que dada la posición de cada jugador y su puntuación, devuelve el número de universos en los que gana cada uno.

Para ello, calcula el resultado de cada posible tirada del
primer jugador, calcula su puntuación, si ha ganado, incrementa un contador relativo a sus victorias, si no gana, se calcula lo mismo
para el segundo jugador, si este sí que gana, incrementa su respectivo contador, si no, hace una llamada recursiva 
e incrementa los contadores con el resultado.

Incluimos el decorador ```@cache``` a la función para que se guarde en memoria el resultado de su ejecución para cada parámetros de entrada,
de modo que si se vuelve a llamar a la función con los mismos parámetros, se ahorre el cálculo.
```python3
@cache
def play(p0, p1, s0, s1):
    res = [0, 0]
    for i in roll_dice():
        np0 = ((p0 - 1 + i) % 10) + 1
        ns0 = s0 + np0
        if ns0 >= 21:
            res[0] += 1
        else:
            for j in roll_dice():
                np1 = ((p1 - 1 + j) % 10) + 1
                ns1 = s1 + np1
                if ns1 >= 21:
                    res[1] += 1
                else:
                    part = play(np0, np1, ns0, ns1)
                    res = [x + y for (x, y) in zip(res, part)]
    return tuple(res)
```

La función principal obtiene los datos igual que en el apartado anterior, llama a la función ```play``` y muestra por pantalla el máximo.
```python3
def main():
    data = [re.findall("[0-9]+", line.strip()) for line in open("input.txt", "r").readlines()]
    positions = {int(player)-1: int(pos) for (player, pos) in data}
    print(max(play(positions[0], positions[1], 0, 0)))
```