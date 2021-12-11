# [Día 11](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 11  | 00:18:00 | 1016 | 0     | 00:21:12 | 1049 | 0     |

## [Parte 1](./Sol1.py)
Esta primera parte ya es un poco más engorrosa en lo que a implementación se refiere, la idea es:
1. Recorrer la matriz incrementando cada celda en 1.
2. Si alguna celda tiene un valor mayor a 9, se incrementa el contador de flashes y también el valor de todas sus
vecinas.
3. Si la matriz ha cambiado, volver al paso 2 teniendo en cuenta solo las celdas que no eran mayores a 9 ya en la iteración anterior.
4. Todas las celdas mayores a 9 pasan a valer 0.
```python3
if __name__ == "__main__":
    data = [list(map(int, list(line.strip()))) for line in open("input.txt", "r").readlines()]

    flashes = 0
    for _ in range(100):
        flashed = []
        static = False
        data = [[cell + 1 for cell in row] for row in data]
        while not static:
            static = True
            for y, row in enumerate(data):
                for x, cell in enumerate(row):
                    if cell > 9 and (x, y) not in flashed:
                        flashed.append((x, y))
                        flashes += 1
                        static = False
                        for dy in range(-1, 2):
                            for dx in range(-1, 2):
                                if 0 <= y+dy < len(data) and 0 <= x+dx < len(data[y]):
                                    data[y+dy][x+dx] += 1
        data = [[cell if cell <= 9 else 0 for cell in row] for row in data]

    print(flashes)
```

Primero leemos la entrada, típica conversión de cada línea a una lista de enteros.
```python3
data = [list(map(int, list(line.strip()))) for line in open("input.txt", "r").readlines()]
```

Primer paso, definimos el contador de flashes, una lista para guardar un registro de las celdas que ya hemos tenido en cuenta,
una variable booleana para comprobar si la matriz ha variado en la última iteración e incrementamos en 1 el valor de cada celda.
```python3
flashes = 0
for _ in range(100):
    flashed = []
    static = False
    data = [[cell + 1 for cell in row] for row in data]
```

Segundo y tercer paso, mientras la matriz cambie, comprobar para cada celda si es mayor que 9 y no la hemos considerado ya, en ese 
caso, la marcamos como tenida en cuenta, incrementamos el contador, indicamos que la matriz ha cambiado e incrementamos los 
vecinos.
```python3
while not static:
    static = True
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if cell > 9 and (x, y) not in flashed:
                flashed.append((x, y))
                flashes += 1
                static = False
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if 0 <= y+dy < len(data) and 0 <= x+dx < len(data[y]):
                            data[y+dy][x+dx] += 1
```

Por último, ponemos a 0 toda celda mayor que 9.
```python3
data = [[cell if cell <= 9 else 0 for cell in row] for row in data]
```

## [Parte 2](./Sol2.py)
Esta segunda parte no es complicada si has implementado la primera eficientemente, simplemente debes cambiar el for por
un while y esperar a que la cantidad de celdas que han “brillado” en la iteración anterior sea igual al número total de celdas.
```python3
if __name__ == "__main__":
    data = [list(map(int, list(line.strip()))) for line in open("input.txt", "r").readlines()]

    flashes = 0
    flashed = []
    step = 0
    while len(flashed) < sum(len(row) for row in data):
        step += 1
        flashed = []
        static = False
        data = [[cell + 1 for cell in row] for row in data]
        while not static:
            static = True
            for y, row in enumerate(data):
                for x, cell in enumerate(row):
                    if cell > 9 and (x, y) not in flashed:
                        flashed.append((x, y))
                        flashes += 1
                        static = False
                        for dy in range(-1, 2):
                            for dx in range(-1, 2):
                                if 0 <= y+dy < len(data) and 0 <= x+dx < len(data[y]):
                                    data[y+dy][x+dx] += 1
        data = [[cell if cell <= 9 else 0 for cell in row] for row in data]

    print(step)
```

Con respecto al apartado anterior, lo único que cambia es la cabecera del while, que comprueba que el número de elementos
que han “brillado” en la iteración anterior sea igual al número total de celdas y añadimos un contador step para saber
en cuantas iteraciones.
```python3
flashes = 0
flashed = []
step = 0
while len(flashed) < sum(len(row) for row in data):
    step += 1
```
