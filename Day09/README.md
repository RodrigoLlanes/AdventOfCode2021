# [Día 9](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 9   | 00:23:46 | 5543 | 0     | 00:40:27 | 3004 | 0     |

## [Parte 1](./Sol1.py)
Esta primera parte es bastante asequible, simplemente tenemos que encontrar los elementos de la matriz que estén
rodeados de valores mayores y sumarlos (añadiéndole uno a cada valor).
```python3
if __name__ == "__main__":
    data = [list(map(int, list(line.strip()))) for line in open("input.txt", "r").readlines()]
    res = 0
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if all(data[ny][nx] > c for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] if
                   (len(data) > ny >= 0) and (len(data[ny]) > nx >= 0)):
                res += 1 + c
    print(res)
```

La lectura de la entrada ya la tenemos más que vista, simplemente leemos cada línea y la mapeamos a int.
```python3
data = [list(map(int, list(line.strip()))) for line in open("input.txt", "r").readlines()]
```

Tras esto, iteramos en los elementos de la matriz, comprobamos que todos sus vecinos cumplan la condición, y si es 
así, incrementamos el contador del resultado.
```python3
res = 0
for y, row in enumerate(data):
    for x, c in enumerate(row):
        if all(data[ny][nx] > c for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] if
               (len(data) > ny >= 0) and (len(data[ny]) > nx >= 0)):
            res += 1 + c
```

## [Parte 2](./Sol2.py)
Esta segunda parte se complica un poco, porque hay que encontrar regiones estrictamente decrecientes, pero el enunciado
del problema no da una ventaja, nos dice que todos los elementos, salvo los que valen 9, pertenecen a una única región.
Gracias a este dato el código se simplifica muchísimo.
```python3
from functools import reduce

if __name__ == "__main__":
    data = [list(map(int, list(line.strip()))) for line in open("input.txt", "r").readlines()]

    basins = {}
    res = 0
    for level in range(0, 9):
        for y, row in enumerate(data):
            for x, c in enumerate(row):
                if c != level:
                    continue
                if all(data[ny][nx] > c for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] if
                       (len(data) > ny >= 0) and (len(data[ny]) > nx >= 0)):
                    data[y][x] = min(basins.keys(), default=0)-1
                    basins[data[y][x]] = 1
                else:
                    for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                        if (len(data) > ny >= 0) and (len(data[ny]) > nx >= 0):
                            if data[ny][nx] < 0:
                                data[y][x] = data[ny][nx]
                                basins[data[ny][nx]] += 1
                                break

    basins = list(sorted(list(basins.values()), reverse=True))
    print(reduce(lambda a, b: a * b, basins[:3]))
```

La lectura del input es idéntica a la del apartado anterior así que avanzo directamente a la resolución.

Vamos a ir iterando de la parte más baja a la más alta, por capas, de modo que como todos los elementos pertenecen
a una región, si un elemento no es el mínimo, entonces estarán tocando a otro elemento que ya pertenece a una región.
Siguiendo esta lógica, en cada nivel, para cada elemento del nivel, comprobamos si es un mínimo, si si que lo es,
le asignamos un id negativo (el id mínimo menos uno), para diferenciarlo de los niveles y para que ningún elemento vecino
pueda detectarse como mínmimo. En caso de que no sea mínimo, buscamos a un vecino suyo que sea menor que 0 y nos unimos 
a su grupo.
```python3
basins = {}
res = 0
for level in range(0, 9):
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if c != level:
                continue
            if all(data[ny][nx] > c for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)] if
                   (len(data) > ny >= 0) and (len(data[ny]) > nx >= 0)):
                data[y][x] = min(basins.keys(), default=0)-1
                basins[data[y][x]] = 1
            else:
                for nx, ny in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                    if (len(data) > ny >= 0) and (len(data[ny]) > nx >= 0):
                        if data[ny][nx] < 0:
                            data[y][x] = data[ny][nx]
                            basins[data[ny][nx]] += 1
                            break
```

Para terminar, ordenamos los tamaños de las regiones de mayor a menor, y multiplicamos las 3 mayores entre ellas, para 
obtener el resultado.
```python3
basins = list(sorted(list(basins.values()), reverse=True))
print(reduce(lambda a, b: a * b, basins[:3]))
```
