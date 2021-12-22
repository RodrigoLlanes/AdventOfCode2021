# [Día 19](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 19  | 10:40:32 | 4413 | 0     | 11:17:20 | 4375 | 0     |

## [Parte 1](./Sol1.py)
Segundo reto del año que no logro resolver solo y necesito consultar otras soluciones para entender como implementarlo.

Este reto tiene dos dificultades principales, el cálculo de las rotaciones (para el que he copiado la función de [Mustafa Quraish](https://github.com/mustafaquraish)),
y la eficiencia del código para que el coste temporal no se dispare, para lo que también me he fijado en [su implementación](https://github.com/mustafaquraish/aoc-2021/blob/master/python/19.py),
aunque haciéndolo a mi manera.

El objetivo de esta primera parte consiste en encontrar la manera de encajar los distintos resultados de cada escáner, de manera
que coincidan en al menos 12 balizas para cada uno, y de esta manera saber cuantas hay en realidad.
```python3
from copy import deepcopy
import re


def transform_set(beacons, orientation):
    return set(transform(pos, orientation) for pos in beacons)


def transform(pt, orientation):
    a, b, c = pt
    return (
        (+a, +b, +c), (+b, +c, +a), (+c, +a, +b), (+c, +b, -a), (+b, +a, -c), (+a, +c, -b),
        (+a, -b, -c), (+b, -c, -a), (+c, -a, -b), (+c, -b, +a), (+b, -a, +c), (+a, -c, +b),
        (-a, +b, -c), (-b, +c, -a), (-c, +a, -b), (-c, +b, +a), (-b, +a, +c), (-a, +c, +b),
        (-a, -b, +c), (-b, -c, +a), (-c, -a, +b), (-c, -b, -a), (-b, -a, -c), (-a, -c, -b)
    )[orientation]


def relative_set(beacons, piv=(0, 0, 0), dis=(0, 0, 0)):
    return set(relative(pos, piv, dis) for pos in beacons)


def relative(pos, piv=(0, 0, 0), dis=(0, 0, 0)):
    return tuple([a - p + d for (a, p, d) in zip(pos, piv, dis)])


def match(_beacons, curr):
    curr_relatives = {piv: relative_set(curr, piv) for piv in curr}
    for orientation in range(24):
        beacons = {piv: transform_set(beacons, orientation) for (piv, beacons) in _beacons.items()}
        for beacon, b_rel in beacons.items():
            for pivot, p_rel in curr_relatives.items():
                if len(set.intersection(b_rel, p_rel)) >= 12:
                    return relative_set(b_rel, dis=pivot)
    return None


def main():
    inp = [line.strip() for line in open("input.txt", "r").readlines()]

    data = []
    for line in inp:
        header = re.match(r"--- scanner ([0-9]+) ---", line)
        coord = re.findall(r"-?[0-9]+", line)
        if line == "":
            continue
        elif header:
            data.append(set())
        else:
            data[-1].add(tuple([int(d) for d in coord]))

    relatives = [{piv: relative_set(group, piv) for piv in group} for group in data]

    aligned = deepcopy(data[0])
    queue = deepcopy(relatives[1:])
    while len(queue) > 0:
        b = queue.pop(0)
        res = match(b, aligned)
        if res is not None:
            aligned = aligned.union(res)
        else:
            queue.append(b)

    print(len(aligned))


if __name__ == "__main__":
    main()
```

Primero vamos a fijarnos en las funciones transformm y relative. 

La función transform, como ya he comentado es de la solución
de [Mustafa Quraish](https://github.com/mustafaquraish), básicamente recibe un punto 3D en forma de tupla y un entero que 
indica la transformación a aplicar (orientación) y devuelve ese punto tras aplicarle esa transformación.

La función relative recibe un punto y otros dos puntos opcionales (pivote y desplazamiento), y devuelve el punto original,
desplazado para que el pivote sea el origen de coordenadas y vuelto a desplazar en función del parámetro desplazamiento.
```python3
def transform(pt, orientation):
    a, b, c = pt
    return (
        (+a, +b, +c), (+b, +c, +a), (+c, +a, +b), (+c, +b, -a), (+b, +a, -c), (+a, +c, -b),
        (+a, -b, -c), (+b, -c, -a), (+c, -a, -b), (+c, -b, +a), (+b, -a, +c), (+a, -c, +b),
        (-a, +b, -c), (-b, +c, -a), (-c, +a, -b), (-c, +b, +a), (-b, +a, +c), (-a, +c, +b),
        (-a, -b, +c), (-b, -c, +a), (-c, -a, +b), (-c, -b, -a), (-b, -a, -c), (-a, -c, -b)
    )[orientation]


def relative(pos, piv=(0, 0, 0), dis=(0, 0, 0)):
    return tuple([a - p + d for (a, p, d) in zip(pos, piv, dis)])
```

Después tenemos la función mtach, que realiza la mayor parte del cálculo, recibe un conjunto de sets relativos y un set de puntos ya orientados,
e intentará encajar el primero en el segundo, si lo logra devolverá el primer set reorientado de modo que coincida con el 
segundo, en caso contrario devolverá None.

Sobre la implementación, simplemente calcula las posiciones para cada elemento del segundo set, de todos los demás elementos 
con respecto al elemento actual (sets relativos), y para cada orientación, la aplica al primer parámetro y comprueba si algún set relativo, se intersecta correctamente
con algún set relativo del segundo parámetro, si es así vuelve a desplazar el set relativo, pero esta vez con respecto a la baliza que ha coincidido, 
para que deje de ser relativo y lo devuelve.
```python3
def match(_beacons, curr):
    curr_relatives = {piv: relative_set(curr, piv) for piv in curr}
    for orientation in range(24):
        beacons = {piv: transform_set(beacons, orientation) for (piv, beacons) in _beacons.items()}
        for beacon, b_rel in beacons.items():
            for pivot, p_rel in curr_relatives.items():
                if len(set.intersection(b_rel, p_rel)) >= 12:
                    return relative_set(b_rel, dis=pivot)
    return None
```

Para terminar, el programa principal, lee la entrada, creando un set para cada escaner, a continuación construye para cada
set un diccionario de sets relativos, se guarda en el primer set como set ya alineado y el resto los añade a una cola.

En cada iteración coge el primer elemento de la cola y trata de encontrar su orientación con el resto de balizas ya alineadas, 
si lo logra, se añade el resultado al set de balizas alineadas, en caso contrario lo añade de nuevo al final de la cola para que
vuelva a ser procesado más tarde.
```python3
def main():
    inp = [line.strip() for line in open("input.txt", "r").readlines()]

    data = []
    for line in inp:
        header = re.match(r"--- scanner ([0-9]+) ---", line)
        coord = re.findall(r"-?[0-9]+", line)
        if line == "":
            continue
        elif header:
            data.append(set())
        else:
            data[-1].add(tuple([int(d) for d in coord]))

    relatives = [{piv: relative_set(group, piv) for piv in group} for group in data]

    aligned = deepcopy(data[0])
    queue = deepcopy(relatives[1:])
    while len(queue) > 0:
        b = queue.pop(0)
        res = match(b, aligned)
        if res is not None:
            aligned = aligned.union(res)
        else:
            queue.append(b)

    print(len(aligned))
```


## [Parte 2](./Sol2.py)
Una vez completada la primera parte, solo debes guardarte también la posición de los escáneres y calcular cual es la mayor 
[distancia de manhattan](https://es.wikipedia.org/wiki/Geometr%C3%ADa_del_taxista) entre dos de ellos.
```python3
from copy import deepcopy
import re


def manhattan(p0, p1):
    return sum(abs(d0 - d1) for (d0, d1) in zip(p0, p1))


def transform_set(beacons, orientation):
    return set(transform(pos, orientation) for pos in beacons)


def transform(pt, orientation):
    a, b, c = pt
    return (
        (+a, +b, +c), (+b, +c, +a), (+c, +a, +b), (+c, +b, -a), (+b, +a, -c), (+a, +c, -b),
        (+a, -b, -c), (+b, -c, -a), (+c, -a, -b), (+c, -b, +a), (+b, -a, +c), (+a, -c, +b),
        (-a, +b, -c), (-b, +c, -a), (-c, +a, -b), (-c, +b, +a), (-b, +a, +c), (-a, +c, +b),
        (-a, -b, +c), (-b, -c, +a), (-c, -a, +b), (-c, -b, -a), (-b, -a, -c), (-a, -c, -b)
    )[orientation]


def relative_set(beacons, piv=(0, 0, 0), dis=(0, 0, 0)):
    return set(relative(pos, piv, dis) for pos in beacons)


def relative(pos, piv=(0, 0, 0), dis=(0, 0, 0)):
    return tuple([a - p + d for (a, p, d) in zip(pos, piv, dis)])


def match(_beacons, curr):
    curr_relatives = {piv: relative_set(curr, piv) for piv in curr}
    for orientation in range(24):
        beacons = {piv: transform_set(beacons, orientation) for (piv, beacons) in _beacons.items()}
        for beacon, b_rel in beacons.items():
            for pivot, p_rel in curr_relatives.items():
                if len(set.intersection(b_rel, p_rel)) >= 12:
                    scan = relative(transform(relative((0, 0, 0), piv=beacon), orientation), dis=pivot)
                    return relative_set(b_rel, dis=pivot), scan
    return None


def main():
    inp = [line.strip() for line in open("input.txt", "r").readlines()]

    data = []
    for line in inp:
        header = re.match(r"--- scanner ([0-9]+) ---", line)
        coord = re.findall(r"-?[0-9]+", line)
        if line == "":
            continue
        elif header:
            data.append(set())
        else:
            data[-1].add(tuple([int(d) for d in coord]))

    relatives = [{piv: relative_set(group, piv) for piv in group} for group in data]

    aligned = deepcopy(data[0])
    queue = deepcopy(relatives[1:])
    scanners = [(0, 0, 0)]
    while len(queue) > 0:
        b = queue.pop(0)
        res = match(b, aligned)
        if res is not None:
            al, scan = res
            aligned = aligned.union(al)
            scanners.append(scan)
        else:
            queue.append(b)

    m = manhattan(scanners[0], scanners[1])
    for a in scanners:
        for b in scanners:
            if a != b:
                m = max(m, manhattan(a, b))

    print(m)


if __name__ == "__main__":
    main()
```

Lo único de esta parte que puede tener un cierto interés es el cálculo de la posición del escaner, para ello, desplazamos
el origen de coordenadas (posición relativa del escaner con respecto a si mismo) con la baliza actual como pivote, para tenerlo en relación a ella,
posteriormente lo orientamos correctamente y para terminar lo volvemos a desplazar, pero esta vez con la posición ya alineada 
de la baliza, para que pase a “coordenadas globales”.
```python3
scan = relative(transform(relative((0, 0, 0), piv=beacon), orientation), dis=pivot)
```
