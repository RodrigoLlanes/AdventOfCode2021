# [Día 2](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 2   | 00:03:15 | 1227 | 0     | 00:08:07 | 2928 | 0     |

Consejo del día, leed bien el enunciado, como podéis observar eso me ha penalizado mucho en el segundo apartado,
pues no he implementado la funcionalidad que pedían para cada instrucción correctamente, me ha dado resultado 
incorrecto y me ha tocado repetirlo.

## [Parte 1](./Sol1.py)
Seguimos en la ronda de calentamiento, otro problema sencillito para ir abriendo boca, en el reto de hoy,
simplemente deberemos ir iterando en la entrada e incrementar o decrementar unas variables en función de
la instrucción que leamos.
```python3
if __name__ == "__main__":
    data = [line.strip().split() for line in open("input.txt", "r").readlines()]
    data = [(order, int(x)) for order, x in data]

    depth = pos = 0
    for order, x in data:
        if order == "forward":
            pos += x
        elif order == "up":
            depth -= x
        elif order == "down":
            depth += x

    print(pos * depth)
```

La lectura de la entrada, la hago en dos líneas por legibilidad, primero leemos cada línea y la dividimos por
los espacios en blanco, para posteriormente convertir el segundo elemento de cada línea en int.
```python3
data = [line.strip().split() for line in open("input.txt", "r").readlines()]
data = [(order, int(x)) for order, x in data]
```

Iteramos en cada línea, y en función de la instrucción leída incrementamos o decrementamos las variables correspondientes.
```python3
depth = pos = 0
for order, x in data:
    if order == "forward":
        pos += x
    elif order == "up":
        depth -= x
    elif order == "down":
        depth += x
```

## [Parte 2](./Sol2.py)
Segunda parte, mismo procedimiento que en el apartado anterior, lo único distinto es, que se añade una nueva variable,
y se cambia lo que hace cada instrucción.
```python3
if __name__ == "__main__":
    data = [line.strip().split() for line in open("input.txt", "r").readlines()]
    data = [(order, int(x)) for order, x in data]

    depth = pos = aim = 0
    for order, x in data:
        if order == "forward":
            pos += x
            depth += aim * x
        elif order == "up":
            aim -= x
        elif order == "down":
            aim += x

    print(pos * depth)
```

La lectura de los datos es igual que en el apartado anterior, así que no nos vamos a molestar
en repetirlo, y vamos a pasar directamente al bucle, aunque tampoco es que cambie mucho.

El bucle funciona exactamente igual que antes, únicamente cambiando las operaciones 
correspondientes a cada función.
```python3
depth = pos = aim = 0
for order, x in data:
    if order == "forward":
        pos += x
        depth += aim * x
    elif order == "up":
        aim -= x
    elif order == "down":
        aim += x
```
