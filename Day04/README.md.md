# [Día 4](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 4   | 00:17:29 | 912  | 0     | 00:30:45 | 1572 | 0     |

## [Parte 1](./Sol1.py)
La cosa ya se empieza a complicar un poco, en esta primera parte deberemos ir marcando las casillas que ya hayan
salido hasta que una fila o columna de un tablero esté completamente marcada.
```python3
def solve(boards):
    for n in numbers:
        for board in boards:
            for row in range(5):
                if n in board[row]:
                    index = board[row].index(n)
                    board[row][index] = -1
                    if all(num == -1 for num in board[row]) or all([r[index] == -1 for r in board]):
                        return sum(sum(c for c in r if c != -1) for r in board) * n


if __name__ == "__main__":
    data = [line.strip() for line in open("input.txt", "r").readlines()]

    numbers = list(map(int, data[0].split(",")))

    boards = []
    for i in range(2, len(data), 6):
        boards.append([list(map(int, row.split())) for row in data[i: i + 5]])

    print(solve(boards))
```

La lectura de la entrada empieza a tener cierta dificultad, lo primero que hago es limpiar cada línea, como
siempre, para después coger la primera línea, hacerle split por comas, y mapearla a int, esta será la lista 
de números que van saliendo en el bingo.

Después leemos los tableros, vamos saltando de 6 en 6 líneas a partir de la tercera y nos guardamos una matriz
de enteros ```boards```, que guarda los números de cada tablero.
```python3
    data = [line.strip() for line in open("input.txt", "r").readlines()]

    numbers = list(map(int, data[0].split(",")))

    boards = []
    for i in range(2, len(data), 6):
        boards.append([list(map(int, row.split())) for row in data[i: i + 5]])
```

Una vez leído correctamente el input, resolvemos iterando en cada número de la primera lista, y marcando la casilla
en la que se encuentra de cada tablero (si es que está) con un -1, cada vez que marcamos una casilla comprobamos si 
acabamos de completar una fila o una columna, y si es así devolvemos el resultado que nos piden (el producto de las
casillas sin marcar por el número que acabamos de marcar)
```python3
for n in numbers:
    for board in boards:
        for row in range(5):
            if n in board[row]:
                index = board[row].index(n)
                board[row][index] = -1
                if all(num == -1 for num in board[row]) or all([r[index] == -1 for r in board]):
                    return sum(sum(c for c in r if c != -1) for r in board) * n
```

## [Parte 2](./Sol2.py)
Como siempre, esta parte es una pequeña vuelta de tuerca al apartado anterior, en este caso en lugar de encontrar
el primer tablero ganador, hay que encontrar el último.
```python3
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
```

La lectura de los datos es identica a la del apartado anterior, así que nos la saltamos y pasamos a la resolución.

El procedimiento no difiere demasiado del anterior, los bucles son los mismos, lo único es que al encontrar un
tablero ganador comprobamos si es el último, si lo es devolvemos el resultado y, sino, lo eliminamos de la lista
de tableros y seguimos. Notar que en el bucle que itera en los tableros, hay que usar una copia de la lista original,
porque si no, al modificarla durante el bucle, producirá resultados erróneos (se saltará tableros).
```python3
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
```
