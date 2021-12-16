# [Día 15](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 15  | 01:03:17 | 4059 | 0     | 01:14:12 | 2486 | 0     |

## [Parte 1](./Sol1.py)
Mis resultados de hoy son un claro ejemplo de que es mejor pararse y pensar un poco, que ponerte a implementar lo primero 
que se te viene a la cabeza a toda prisa.

El reto de hoy no era en absoluto complicado, simplemente había que encontrar el camino que minimizara el riesgo, un caso
evidente de camino más corto, que se puede solucionar con uno de los algoritmos más famosos, el algoritmo de [dijkstra](https://es.wikipedia.org/wiki/Algoritmo_de_Dijkstra).
```python3
from heapq import heappop, heappush


def main():
    data = [list(map(int, list(line.strip()))) for line in open("input.txt", "r").readlines()]
    end = (len(data[0])-1, len(data)-1)

    heap = [(0, (0, 0))]
    visited = set()

    while len(heap) > 0:
        risk, pos = heappop(heap)
        if pos in visited:
            continue
        visited.add(pos)

        if pos == end:
            print(risk)
            break

        for (x, y) in [(pos[0]+dx, pos[1]+dy) for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]]:
            if (0 <= x <= end[0]) and (0 <= y <= end[1]):
                heappush(heap, (risk + data[y][x], (x, y)))


if __name__ == "__main__":
    main()
```

La lectura de los datos no tiene ninguna complicación, simplemente convertimos cada linea a una lista de enteros y nos guardamos
el punto al que queremos llegar (la esquina inferior derecha).
```python3
data = [list(map(int, list(line.strip()))) for line in open("input.txt", "r").readlines()]
end = (len(data[0])-1, len(data)-1)
```

Hecho esto ya solo queda implementar el algoritmo, cosa que no voy a explicar en detalle, pues existe muchísima documentación
al respecto, pero básicamente es ir acumulando todos los caminos y dar siempre el salto más pequeño, hasta encontrar el final.
```python3
    heap = [(0, (0, 0))]
    visited = set()

    while len(heap) > 0:
        risk, pos = heappop(heap)
        if pos in visited:
            continue
        visited.add(pos)

        if pos == end:
            print(risk)
            break

        for (x, y) in [(pos[0]+dx, pos[1]+dy) for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]]:
            if (0 <= x <= end[0]) and (0 <= y <= end[1]):
                heappush(heap, (risk + data[y][x], (x, y)))
```



## [Parte 2](./Sol2.py)
Con la primera parte hecha, la segunda es trivial, lo único que tenemos que hacer es modificar la entrada como nos piden.
```python3
from heapq import heappop, heappush


def main():
    def increase(i):
        def f(a):
            if a + i > 9:
                return a - 9 + i
            return a + i
        return f

    data = [list(map(int, list(line.strip()))) for line in open("input.txt", "r").readlines()]
    data = [sum([list(map(increase(i), line)) for i in range(5)], []) for line in data]
    data = sum([[list(map(increase(i), line)) for line in data] for i in range(5)], [])
    end = (len(data[0])-1, len(data)-1)

    heap = [(0, (0, 0))]
    visited = set()

    while len(heap) > 0:
        risk, pos = heappop(heap)
        if pos in visited:
            continue
        visited.add(pos)

        if pos == end:
            print(risk)
            break

        for (x, y) in [(pos[0]+dx, pos[1]+dy) for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]]:
            if (0 <= x <= end[0]) and (0 <= y <= end[1]):
                heappush(heap, (risk + data[y][x], (x, y)))


if __name__ == "__main__":
    main()
```

La modificación de la entrada es lo único distinto, así que lo voy a explicar, la función increase, recibe un entero i y devuelve
una función que recibe a su vez otro entero a, lo incrementa en i y lo acota en el rango 1..9.

Después de leer el input, se añaden primero 4 copias de el mismo incrementadas de 1 a 4 en fila y después se hace lo mismo
en columna.
```python3
    def increase(i):
        def f(a):
            if a + i > 9:
                return a - 9 + i
            return a + i
        return f

    data = [list(map(int, list(line.strip()))) for line in open("input.txt", "r").readlines()]
    data = [sum([list(map(increase(i), line)) for i in range(5)], []) for line in data]
    data = sum([[list(map(increase(i), line)) for line in data] for i in range(5)], [])
    end = (len(data[0])-1, len(data)-1)
```
