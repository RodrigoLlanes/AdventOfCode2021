# [Día 22](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 22  | 00:14:13 | 1008 | 0     | 01:56:24 | 1104 | 0     |

## [Parte 1](./Sol1.py)

La primera parte de este reto es sencilla, simplemente tenemos que llevar la cuenta de los cubos que se van encendiendo
y apagando.
```python3
import re


def main():
    data = [re.match(r"(on|off) x=(-?[0-9]+)..(-?[0-9]+),y=(-?[0-9]+)..(-?[0-9]+),z=(-?[0-9]+)..(-?[0-9]+)", line.strip()).groups()
            for line in open("input.txt", "r").readlines()]
    data = [(act == "on", int(x0), int(x1), int(y0), int(y1), int(z0), int(z1)) for (act, x0, x1, y0, y1, z0, z1) in data]

    cubes = {}
    _min = -50
    _max = 50
    for act, x0, x1, y0, y1, z0, z1 in data:
        if x1 >= _min and x0 <= _max and y1 >= _min and y0 <= _max and z1 >= _min and z0 <= _max:
            for x in range(max(x0, _min), min(x1, _max)+1):
                for y in range(max(y0, _min), min(y1, _max)+1):
                    for z in range(max(z0, _min), min(z1, _max)+1):
                        cubes[x, y, z] = act

    print(sum(1 for v in cubes.values() if v))


if __name__ == "__main__":
    main()
```

Para la lectura de la entrada usamos [regex](https://es.wikipedia.org/wiki/Expresi%C3%B3n_regular) para obtener las coordenadas
y acción ejecutada en cada línea, para luego castear cada elemento a su tipo correspondiente.
```python3
data = [re.match(r"(on|off) x=(-?[0-9]+)..(-?[0-9]+),y=(-?[0-9]+)..(-?[0-9]+),z=(-?[0-9]+)..(-?[0-9]+)", line.strip()).groups()
        for line in open("input.txt", "r").readlines()]
data = [(act == "on", int(x0), int(x1), int(y0), int(y1), int(z0), int(z1)) for (act, x0, x1, y0, y1, z0, z1) in data]
```

Y para acabar, en cada acción recorremos la lista de pasos y vamos poniendo a True o False los contadores correspondientes (dentro del margen de -50 a 50).
```python3
cubes = {}
_min = -50
_max = 50
for act, x0, x1, y0, y1, z0, z1 in data:
    if x1 >= _min and x0 <= _max and y1 >= _min and y0 <= _max and z1 >= _min and z0 <= _max:
        for x in range(max(x0, _min), min(x1, _max)+1):
            for y in range(max(y0, _min), min(y1, _max)+1):
                for z in range(max(z0, _min), min(z1, _max)+1):
                    cubes[x, y, z] = act

print(sum(1 for v in cubes.values() if v))
```

## [Parte 2](./Sol2.py)

La segunda parte ha sido larga, pero muy divertida de implementar, mi solución no es la más óptima, y se podría mejorar con relativa
facilidad, pero aun así le cuesta pocos segundos, o como mucho un minuto ejecutarse así que no veo necesario optimizarla de momento.

Al ampliarse a varios miles de unidades el rango de las acciones, se hace imposible trabajar con cada cubo individual. Por lo que
trabajaremos con los [ortoedros](https://es.wikipedia.org/wiki/Ortoedro) (cuboides para los amigos) de los pasos de reinicio.
```python3
def overlap(x00, x01, y00, y01, z00, z01, x10, x11, y10, y11, z10, z11):
    if x01 < x10 or x11 < x00 or y01 < y10 or y11 < y00 or z01 < z10 or z11 < z00:
        return [], [(x00, x01, y00, y01, z00, z01)]
    x_min = max(x00, x10)
    y_min = max(y00, y10)
    z_min = max(z00, z10)
    x_max = min(x01, x11)
    y_max = min(y01, y11)
    z_max = min(z01, z11)

    x_slices = [(x00, x01)]
    if x00 < x_min:
        x_slices = [(x00, x_min - 1), (x_min, x01)]
    if x01 > x_max:
        x_slices = x_slices[:-1] + [(x_slices[-1][0], x_max), (x_max + 1, x01)]

    y_slices = [(y00, y01)]
    if y00 < y_min:
        y_slices = [(y00, y_min - 1), (y_min, y01)]
    if y01 > y_max:
        y_slices = y_slices[:-1] + [(y_slices[-1][0], y_max), (y_max + 1, y01)]

    z_slices = [(z00, z01)]
    if z00 < z_min:
        z_slices = [(z00, z_min - 1), (z_min, z01)]
    if z01 > z_max:
        z_slices = z_slices[:-1] + [(z_slices[-1][0], z_max), (z_max + 1, z01)]

    intersect, rest = [], []
    for (x_min, x_max) in x_slices:
        for (y_min, y_max) in y_slices:
            for (z_min, z_max) in z_slices:
                if x_max < x10 or x11 < x_min or y_max < y10 or y11 < y_min or z_max < z10 or z11 < z_min:
                    rest.append((x_min, x_max, y_min, y_max, z_min, z_max))
                else:
                    intersect.append((x_min, x_max, y_min, y_max, z_min, z_max))
    return intersect, rest


class Figure:
    def __init__(self, cubes=[]):
        self.cubes = cubes

    def intersect(self, other):
        res = []
        for self_cube in self.cubes:
            for other_cube in other.cubes:
                res.extend(overlap(*self_cube, *other_cube)[0])
        return Figure(res)

    def __sub__(self, other):
        res = []
        for self_cube in self.cubes:
            rest = Figure([self_cube])
            for other_cube in other.cubes:
                rest = rest.intersect(Figure(overlap(*self_cube, *other_cube)[1]))
            res.extend(rest.cubes)
        return Figure(res)

    def union(self, other):
        res = (deepcopy(self) - (self.intersect(other))).cubes
        res.extend(other.cubes)
        return Figure(res)

    def volume(self):
        res = 0
        for x0, x1, y0, y1, z0, z1 in self.cubes:
            res += (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1)
        return res


def main():
    data = [re.match(r"(on|off) x=(-?[0-9]+)..(-?[0-9]+),y=(-?[0-9]+)..(-?[0-9]+),z=(-?[0-9]+)..(-?[0-9]+)", line.strip()).groups()
            for line in open("input.txt", "r").readlines()]
    data = [(act == "on", Figure([(int(x0), int(x1), int(y0), int(y1), int(z0), int(z1))])) for (act, x0, x1, y0, y1, z0, z1) in data]

    res = Figure()
    for act, fig in data:
        if act:
            res = res.union(fig)
        else:
            res = res - fig
    print(res.volume())


if __name__ == "__main__":
    main()
```

La función overlap, recibe como parámetros las coordenadas de dos cuboides y devuelve dos listas, la primera contendrá
los sub-cubos del primer cuboide que intersectan con el segundo y en la segunda lista, los que no.

Para ello, se divide al cubo original de uno a nueve sub-cubos en función de la complejidad de la intersección y después
se calcula cuál de ellos está dentro y cuál fuera.
```python3
def overlap(x00, x01, y00, y01, z00, z01, x10, x11, y10, y11, z10, z11):
    if x01 < x10 or x11 < x00 or y01 < y10 or y11 < y00 or z01 < z10 or z11 < z00:
        return [], [(x00, x01, y00, y01, z00, z01)]
    x_min = max(x00, x10)
    y_min = max(y00, y10)
    z_min = max(z00, z10)
    x_max = min(x01, x11)
    y_max = min(y01, y11)
    z_max = min(z01, z11)

    x_slices = [(x00, x01)]
    if x00 < x_min:
        x_slices = [(x00, x_min - 1), (x_min, x01)]
    if x01 > x_max:
        x_slices = x_slices[:-1] + [(x_slices[-1][0], x_max), (x_max + 1, x01)]

    y_slices = [(y00, y01)]
    if y00 < y_min:
        y_slices = [(y00, y_min - 1), (y_min, y01)]
    if y01 > y_max:
        y_slices = y_slices[:-1] + [(y_slices[-1][0], y_max), (y_max + 1, y01)]

    z_slices = [(z00, z01)]
    if z00 < z_min:
        z_slices = [(z00, z_min - 1), (z_min, z01)]
    if z01 > z_max:
        z_slices = z_slices[:-1] + [(z_slices[-1][0], z_max), (z_max + 1, z01)]

    intersect, rest = [], []
    for (x_min, x_max) in x_slices:
        for (y_min, y_max) in y_slices:
            for (z_min, z_max) in z_slices:
                if x_max < x10 or x11 < x_min or y_max < y10 or y11 < y_min or z_max < z10 or z11 < z_min:
                    rest.append((x_min, x_max, y_min, y_max, z_min, z_max))
                else:
                    intersect.append((x_min, x_max, y_min, y_max, z_min, z_max))
    return intersect, rest
```

Posteriormente definimos la clase figura, que está formada por sub-cubos y consta de los siguientes métodos:

- ```intersect```: Devuelve la intersección de dos figuras, empleando la función anterior, y uniendo las intersecciones de los
sub-cubos de cada figura.

- ```__sub__```: Calcula la resta de dos figuras, como si de una [diferencia de conjuntos](https://es.wikipedia.org/wiki/Diferencia_de_conjuntos) se tratara
y empleando también el segundo valor de retorno de la función ```overlap```.
  
- ```union```: Devuelve la unión de dos figuras, empleando la intersección y la resta, como en la [unión de conjuntos](https://es.wikipedia.org/wiki/Uni%C3%B3n_de_conjuntos).
  
- ```volume```: Por último la función volumen, que simplemente calcula el volumen de la figura calculando el volumen de cada uno de los
  sub-cubos y sumándolos.
  
```python3
class Figure:
    def __init__(self, cubes=[]):
        self.cubes = cubes

    def intersect(self, other):
        res = []
        for self_cube in self.cubes:
            for other_cube in other.cubes:
                res.extend(overlap(*self_cube, *other_cube)[0])
        return Figure(res)

    def __sub__(self, other):
        res = []
        for self_cube in self.cubes:
            rest = Figure([self_cube])
            for other_cube in other.cubes:
                rest = rest.intersect(Figure(overlap(*self_cube, *other_cube)[1]))
            res.extend(rest.cubes)
        return Figure(res)

    def union(self, other):
        res = (deepcopy(self) - (self.intersect(other))).cubes
        res.extend(other.cubes)
        return Figure(res)

    def volume(self):
        res = 0
        for x0, x1, y0, y1, z0, z1 in self.cubes:
            res += (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1)
        return res
```

Por último, al leer la entrada, generamos las figuras y hacemos uso de las funciones definidas anteiormente para quedarnos solo
con el volumen de los cubos encendidos.
```python3
data = [re.match(r"(on|off) x=(-?[0-9]+)..(-?[0-9]+),y=(-?[0-9]+)..(-?[0-9]+),z=(-?[0-9]+)..(-?[0-9]+)", line.strip()).groups()
        for line in open("input.txt", "r").readlines()]
data = [(act == "on", Figure([(int(x0), int(x1), int(y0), int(y1), int(z0), int(z1))])) for (act, x0, x1, y0, y1, z0, z1) in data]

res = Figure()
for act, fig in data:
    if act:
        res = res.union(fig)
    else:
        res = res - fig
print(res.volume())
```