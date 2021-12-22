# [Día 20](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 20  | 01:00:05 | 2122 | 0     | 01:01:08 | 1871 | 0     |

## [Parte 1](./Sol1.py)
En el reto de hoy simplemente tienes que ir recorriendo los símbolos de la matriz de entrada y mirar sus vecinos para aplicar la
regla correspondiente, básicamente es implementar [el juego de la vida](https://es.wikipedia.org/wiki/Juego_de_la_vida), lo que no es complicado, 
salvo por un pequeño detalle que te puede dejar un buen rato debugueando el código sin entender que está pasando, si una celda apagada está rodeada
de celdas apagadas, se enciende y si una celda encendida está rodeada de celdas encendidas, se apaga.
```python3
from copy import deepcopy


def parse(x, y, data, default):
    res = [data.get((x + dx, y + dy), default) for dy in range(-1, 2) for dx in range(-1, 2)]
    res = ''.join(['1' if sym == '#' else '0' for sym in res])
    return int(res, 2)


def main():
    inp = [line.strip() for line in open("input.txt", "r").readlines()]

    alg = inp[0]
    min_y, max_y = 0, len(inp) - 2
    min_x, max_x = 0, len(inp[2])
    data = {}
    for y, line in enumerate(inp[2:]):
        for x, sym in enumerate(line):
            data[x, y] = sym

    for step in range(2):
        min_y, max_y = min_y-1, max_y+1
        min_x, max_x = min_x-1, max_x+1
        background = "." if step % 2 == 0 else "#"
        new_data = deepcopy(data)
        for x in range(min_x-1, max_x+2):
            for y in range(min_y - 1, max_y + 2):
                new_data[x, y] = alg[parse(x, y, data, background)]
        data = new_data

    print(sum(1 for sym in data.values() if sym == "#"))


if __name__ == "__main__":
    main()
```

Definimos la función parse, que recibe las coordenadas de una celda, los datos y un valor por defecto, que tomarán las celdas sin valor asignado,
coge los valores de los vecinos y de la propia casilla, convierte los “#” en unos y los ”.” en ceros, y por último lo convierte de binario a entero.
```python3
def parse(x, y, data, default):
    res = [data.get((x + dx, y + dy), default) for dy in range(-1, 2) for dx in range(-1, 2)]
    res = ''.join(['1' if sym == '#' else '0' for sym in res])
    return int(res, 2)
```

Después tenemos la función principal, que primero lee el input, guarda los valores mínimos y máximos de x e y, y guarda en un diccionario, 
los valores asociados a cada celda.

Y a continuación, en cada step, incrementa y decrementa los valores mínimos y máximos respectivamente, calcula el símbolo de fondo (el valor de los símbolos exteriores sin procesar),
y para cada elemento genera su nuevo valor y lo almacena en un nuevo diccionario.

Por último muestra por pantalla la cantidad de elementos cuyo valor es “#”.
```python3
def main():
    inp = [line.strip() for line in open("input.txt", "r").readlines()]

    alg = inp[0]
    min_y, max_y = 0, len(inp) - 2
    min_x, max_x = 0, len(inp[2])
    data = {}
    for y, line in enumerate(inp[2:]):
        for x, sym in enumerate(line):
            data[x, y] = sym

    for step in range(2):
        min_y, max_y = min_y-1, max_y+1
        min_x, max_x = min_x-1, max_x+1
        background = "." if step % 2 == 0 else "#"
        new_data = deepcopy(data)
        for x in range(min_x-1, max_x+2):
            for y in range(min_y - 1, max_y + 2):
                new_data[x, y] = alg[parse(x, y, data, background)]
        data = new_data

    print(sum(1 for sym in data.values() if sym == "#"))
```

## [Parte 2](./Sol2.py)
La segunda parte es idéntica a la primera, únicamente realizando 50 iteraciones en lugar de solo 2.
```python3
from copy import deepcopy


def parse(x, y, data, default):
    res = [data.get((x + dx, y + dy), default) for dy in range(-1, 2) for dx in range(-1, 2)]
    res = ''.join(['1' if sym == '#' else '0' for sym in res])
    return int(res, 2)


def main():
    inp = [line.strip() for line in open("input.txt", "r").readlines()]

    alg = inp[0]
    min_y, max_y = 0, len(inp) - 2
    min_x, max_x = 0, len(inp[2])
    data = {}
    for y, line in enumerate(inp[2:]):
        for x, sym in enumerate(line):
            data[x, y] = sym

    for step in range(50):
        min_y, max_y = min_y-1, max_y+1
        min_x, max_x = min_x-1, max_x+1
        background = "." if step % 2 == 0 else "#"
        new_data = deepcopy(data)
        for x in range(min_x-1, max_x+2):
            for y in range(min_y - 1, max_y + 2):
                new_data[x, y] = alg[parse(x, y, data, background)]
        data = new_data

    print(sum(1 for sym in data.values() if sym == "#"))


if __name__ == "__main__":
    main()
```

