# [Día 5](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 5   | 00:07:49 | 356  | 0     | 00:19:21 | 878  | 0     |

## [Parte 1](./Sol1.py)
Esta primera parte no es especialmente complicada, simplemente hay que recorrer la entrada, comprobar si
coinciden las equis o las íes e incrementar los contadores correspondientes a cada punto de la recta.
```python3
from collections import defaultdict
import re

if __name__ == "__main__":
    data = [list(map(int, re.findall(r"(\d+)", line.strip()))) for line in open("input.txt", "r").readlines()]

    over = defaultdict(int)

    for x1, y1, x2, y2 in data:
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2)+1):
                over[x1, y] += 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2)+1):
                over[x, y1] += 1

    print(sum(v > 1 for v in over.values()))
```

Para leer la entrada empleamos regex, buscamos todos los números de cada línea y los convertimos a int.
```python3
data = [list(map(int, re.findall(r"(\d+)", line.strip()))) for line in open("input.txt", "r").readlines()]
```

Tras leer el input, creamos un defaultdict de enteros y recorremos la entrada, si coinciden las equis, recorremos
desde la y más pequeña hasta la más grande incrementando los contadores correspondientes a cada punto, aplicamos el
procedimiento homónimo si las íes son iguales.
```python3
over = defaultdict(int)

for x1, y1, x2, y2 in data:
    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2)+1):
            over[x1, y] += 1
    elif y1 == y2:
        for x in range(min(x1, x2), max(x1, x2)+1):
            over[x, y1] += 1
```

Por último sumamos la cantidad de valores del diccionario cuyo valor sea superior a 1 y los mostramos por pantalla.
```python3
print(sum(v > 1 for v in over.values()))
```

## [Parte 2](./Sol2.py)
Ligera ampliación del ejercicio anterior, ya no solo hay que tener en cuenta las rectas verticales y horizontales,
sino que también aceptamos diagonales.
```python3
from collections import defaultdict
import re

if __name__ == "__main__":
    data = [list(map(int, re.findall(r"(\d+)", line.strip()))) for line in open("input.txt", "r").readlines()]

    over = defaultdict(int)

    for x1, y1, x2, y2 in data:
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2)+1):
                over[x1, y] += 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2)+1):
                over[x, y1] += 1
        else:
            dx = -1 if x1 > x2 else 1
            dy = -1 if y1 > y2 else 1

            for x, y in zip(range(x1, x2+dx, dx), range(y1, y2+dy, dy)):
                over[x, y] += 1

    print(sum(v > 1 for v in over.values()))
```

Vamos a comentar únicamente el contenido del else, que es lo que cambia con respecto al apartado anterior.

Lo primero es calcular si la recta va de derecha a izquierda o de izquierda a derecha y si va de arriba a abajo o 
de abajo a arriba, de este modo sabemos si hay que incrementar o decrementar el valor de x e y en cada iteración
del bucle.

Para despues calcular los valores de x e y en cada punto, unirlos con un zip e incrementar los contadores.
```python3
dx = -1 if x1 > x2 else 1
dy = -1 if y1 > y2 else 1

for x, y in zip(range(x1, x2+dx, dx), range(y1, y2+dy, dy)):
    over[x, y] += 1
```
