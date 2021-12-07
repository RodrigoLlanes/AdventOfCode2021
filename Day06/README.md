# [Día 6](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 6   | 00:14:09 | 4836 | 0     | 00:14:32 | 1119 | 0     |

## [Parte 1](./Sol1.py)
Esta primera parte podría parecer sencilla, simplemente hay que llevar la cuenta de todos los peces que hay
y de los que se van creando e ir decrementando sus contadores, hasta que lleguen a -1, entonces resetearlos
a 6 y crear un nuevo pez de 8. Pero si ya has participado alguna vez en el AOC, sabrás que esta solución 
puede valerte para la primera parte, pero la segunda, probablemente requiera de un cálculo más costoso, 
por lo que si optimizas esta parte, ya tendrás la segunda hecha, o muy adelantada.
```python3
from collections import defaultdict

if __name__ == "__main__":
    data = [list(map(int, line.strip().split(","))) for line in open("input.txt", "r").readlines()][0]
    data = {c: data.count(c) for c in set(data)}
    
    for _ in range(80):
        new_data = defaultdict(int)
        for c, v in data.items():
            if c > 0:
                new_data[c-1] += v
            else:
                new_data[6] += v
                new_data[8] += v
        data = new_data
    
    print(sum(v for v in data.values()))
```

Para leer la entrada, primero dividimos cada línea por las comas, convertimos cada elemento a int y cogemos
solo la primera línea. Para después crear un diccionario cuya clave es el valor del contador de un pez
y la clave es la cantidad de peces con ese valor en su contador.
```python3
data = [list(map(int, line.strip().split(","))) for line in open("input.txt", "r").readlines()][0]
data = {c: data.count(c) for c in set(data)}]
```

Una vez tenemos nuestro input limpio, iteramos 80 veces, y en cada iteración, recorremos nuestro diccionario
y generamos uno nuevo con los decrementos de los contadores, los reseteos y los nuevos elementos.
```python3
for _ in range(80):
    new_data = defaultdict(int)
    for c, v in data.items():
        if c > 0:
            new_data[c-1] += v
        else:
            new_data[6] += v
            new_data[8] += v
    data = new_data
```

Por último sumamos la cantidad de valores del diccionario (la cantidad de peces) y los mostramos por pantalla.
```python3
print(sum(v for v in data.values()))
```

## [Parte 2](./Sol2.py)
La parte 2 es idéntica a la primera parte, por lo que no voy a explicar nada, lo único que cambia es
que el for hace 256 iteraciones en lugar de solo 80.
```python3
from collections import defaultdict

if __name__ == "__main__":
    data = [list(map(int, line.strip().split(","))) for line in open("input.txt", "r").readlines()][0]
    data = {c: data.count(c) for c in set(data)}
    
    for _ in range(256):
        new_data = defaultdict(int)
        for c, v in data.items():
            if c > 0:
                new_data[c-1] += v
            else:
                new_data[6] += v
                new_data[8] += v
        data = new_data
    
    print(sum(v for v in data.values()))
```
