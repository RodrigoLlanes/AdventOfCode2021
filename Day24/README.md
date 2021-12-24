# [Día 24](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 24  | 03:28:15 | 1312 | 0     | 03:28:46 | 1219 | 0     |

## [Parte 1](./Sol1.py)
El reto de hoy es complicado, sobre todo si eres como yo y te pones manos a la obra sin pararte a leer el input (como se recomienda en el enunciado).

Tras unas cuantas horas de desesperación decidí aceptar mi derrota y me puse a buscar una buena solución para entender y poder
replicar a mi manera (como hago siempre que no soy capaz de resolver un reto). Encontré todo tipo de soluciones, desde [transpilar a c, 
compilar optimizando, decompilar y volver a transpilar a python](https://www.reddit.com/r/adventofcode/comments/rnejv5/comment/hps4c3n/?utm_source=share&utm_medium=web2x&context=3),
hasta [resolverlo a mano](https://www.reddit.com/r/adventofcode/comments/rnejv5/comment/hps7skz/?utm_source=share&utm_medium=web2x&context=3). 

Pero sin lugar a dudas, mi solución favorita es la de [Adib Surani](https://gist.github.com/AdibSurani/c047a0f0d3d9bc294337cb58da16173e), 
que analizando el código del problema y con un puñado de líneas de código, soluciona el problema en segundos. Y en esa solución es en la
que me basé para mi implementación, notar que al ser la original tan compacta, mi versión es muy similar.
```python3
from z3 import *


def main():
    data = [line.strip().split() for line in open("input.txt", "r").readlines()]
    params = [[int(data[i+j][-1]) for j in [4, 5, 15]] for i in range(0, len(data), 18)]
    inputs = [Int(f'inp_{i}') for i in range(14)]

    opt = Optimize()
    val = z = 0
    for inp, (a, b, c) in zip(inputs, params):
        val = val * 10 + inp
        opt.add(And(inp >= 1, inp <= 9))
        z = If(z % 26 + b != inp,
               z / a * 26 + inp + c,
               z / a)
    opt.add(z == 0)

    opt.maximize(val)
    assert opt.check() == sat
    print(opt.model().eval(val))


if __name__ == "__main__":
    main()
```

#### TODO

## [Parte 2](./Sol2.py)

Para pasar de la solución de la primera parte a la de la segunda, solamente hay que cambiar la función de optimización, de maximización
a minimización.
```python3
from z3 import *


def main():
    data = [line.strip().split() for line in open("input.txt", "r").readlines()]
    params = [[int(data[i+j][-1]) for j in [4, 5, 15]] for i in range(0, len(data), 18)]
    inputs = [Int(f'inp_{i}') for i in range(14)]

    opt = Optimize()
    val = z = 0
    for inp, (a, b, c) in zip(inputs, params):
        val = val * 10 + inp
        opt.add(And(inp >= 1, inp <= 9))
        z = If(z % 26 + b != inp,
               z / a * 26 + inp + c,
               z / a)
    opt.add(z == 0)

    opt.minimize(val)
    assert opt.check() == sat
    print(opt.model().eval(val))


if __name__ == "__main__":
    main()
```