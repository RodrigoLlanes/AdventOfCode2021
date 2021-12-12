# [Día 12](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 12  | 00:19:57 | 1543 | 0     | 00:23:53 | 751  | 0     |

## [Parte 1](./Sol1.py)
Vale, esta primera parte puede parecer difícil así de primeras, pero si te paras un segundo a pensar es un problema
sencillo de [ramificación y poda](https://es.wikipedia.org/wiki/Ramificaci%C3%B3n_y_poda). En concreto en este problema
debemos ir ramificando todos los posibles caminos y podar los estados en los que se vaya a pasar dos veces por la misma
cueva pequeña.
```python3
import re
from collections import defaultdict


def main():
    data = [list(re.findall(r"[a-zA-Z]+", line)) for line in open("input.txt", "r").readlines()]

    graph = defaultdict(set)
    for start, end in data:
        graph[start].add(end)
        graph[end].add(start)

    def ramificate(steps):
        curr = steps[-1]
        if curr == "end":
            return 1
        sols = 0
        for neighbour in graph[curr]:
            if not neighbour.islower() or neighbour not in steps:
                sols += ramificate(steps + [neighbour])
        return sols

    print(ramificate(["start"]))


if __name__ == "__main__":
    main()
```

Primero leemos la entrada, utilizamos [regex](https://es.wikipedia.org/wiki/Expresi%C3%B3n_regular) para separar los identificadores de las cuevas de cada línea, para posteriormente
crear el grafo usando un diccionario donde la clave es un nodo y el valor un set con los nodos a los que se puede llegar
desde este (Utilizamos un set porque la búsqueda en sets con python es más eficiente, pero se podría usar igual una lista).
```python3
data = [list(re.findall(r"[a-zA-Z]+", line)) for line in open("input.txt", "r").readlines()]

graph = defaultdict(set)
for start, end in data:
    graph[start].add(end)
    graph[end].add(start)
```

La resolución no es en absoluto complicada, simplemente creamos la función ramificación, que recibe en forma de lista, 
el camino ya realizado y devuelve el número de posibles caminos desde ese punto hasta la salida cumpliendo las restricciones.
Para ello, comprobamos si el nodo actual (último elemento del camino ya realizado) es el final, en cuyo caso devolvemos 1, si ese no es el caso,
para cada vecino del nodo actual, si es una cueva grande, o no lo hemos visitado todavía, ramificamos añadiendo ese vecino
al camino actual, una vez obtenidos los resultados de todas las ramificaciones, devolvemos la suma.
```python3
def ramificate(steps):
    curr = steps[-1]
    if curr == "end":
        return 1
    sols = 0
    for neighbour in graph[curr]:
        if not neighbour.islower() or neighbour not in steps:
            sols += ramificate(steps + [neighbour])
    return sols
```

## [Parte 2](./Sol2.py)
Esta segunda parte es idéntica a la anterior, salvo por el pequeño detalle de que podemos repetir una cueva pequeña, pero
no la entrada.
```python3
import re
from collections import defaultdict


def main():
    data = [list(re.findall(r"[a-zA-Z]+", line)) for line in open("input.txt", "r").readlines()]

    graph = defaultdict(set)
    for start, end in data:
        if end != "start":
            graph[start].add(end)
        if start != "start":
            graph[end].add(start)

    def ramificate(steps, twice=False):
        curr = steps[-1]
        if curr == "end":
            return 1
        sols = 0
        for neighbour in graph[curr]:
            if not neighbour.islower() or neighbour not in steps:
                sols += ramificate(steps + [neighbour], twice)
            elif not twice:
                sols += ramificate(steps + [neighbour], True)
        return sols

    print(ramificate(["start"]))


if __name__ == "__main__":
    main()
```

En la lectura de los datos solo cabe destacar que comprobamos que el nodo que añadimos como vecino no sea start, de este
modo desde start se pude salir, pero no volver.
```python3
data = [list(re.findall(r"[a-zA-Z]+", line)) for line in open("input.txt", "r").readlines()]

graph = defaultdict(set)
for start, end in data:
    if end != "start":
        graph[start].add(end)
    if start != "start":
        graph[end].add(start)
```

La función de ramificación añade un parámetro twice, que indica si en iteraciones anteriores, se ha repetido una cueva pequeña,
en caso contrario, podemos permitirnos repetir en esta iteración.
```python3
def ramificate(steps, twice=False):
    curr = steps[-1]
    if curr == "end":
        return 1
    sols = 0
    for neighbour in graph[curr]:
        if not neighbour.islower() or neighbour not in steps:
            sols += ramificate(steps + [neighbour], twice)
        elif not twice:
            sols += ramificate(steps + [neighbour], True)
    return sols
```
