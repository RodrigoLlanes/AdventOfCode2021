# [Día 10](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 10  | 00:08:28 | 1076 | 0     | 00:17:36 | 1340 | 0     |

## [Parte 1](./Sol1.py)
Esta primera parte es bastante asequible, la única cosa "compleja" es que hay que usar una pila, pero cualquier persona
con mínimos conocimientos de estructuras de datos, lo sacaría sin problemas. Simplemente tenemos que comprobar si
un símbolo de cierre no corresponde con el último símbolo de apertura, y en dicho caso sumar la puntuación correspondiente
a ese error.
```python3
opening = {")": "(", "]": "[", "}": "{", ">": "<"}
error_points = {")": 3, "]": 57, "}": 1197, ">": 25137}

if __name__ == "__main__":
    data = [list(line.strip()) for line in open("input.txt", "r").readlines()]

    score = 0
    for line in data:
        stack = []
        for c in line:
            if c in opening.values():
                stack.append(c)
            else:
                last = stack.pop()
                if last != opening[c]:
                    score += error_points[c]
                    break

    print(score)

```

Primero definimos dos diccionarios, en el primero relacionamos cada símbolo de cierre con su correspondiente símbolo de
apertura, y en el segundo los relacionamos con su puntuación. La lectura de la entrada es trivial, cada línea la convertimos a lista para poder manejar los símbolos por 
separado
con más facilidad.
```python3
opening = {")": "(", "]": "[", "}": "{", ">": "<"}
error_points = {")": 3, "]": 57, "}": 1197, ">": 25137}

if __name__ == "__main__":
    data = [list(line.strip()) for line in open("input.txt", "r").readlines()]
```

Tras esto para cada línea creamos una pila e iteramos en cada símbolo de la línea, si es de apertura lo apilamos, si por
el contrario es de cierre des apilamos el último símbolo de la pila, si este no coincide con el de apertura del símbolo
actual, incrementamos la puntuación y pasamos a la siguiente línea.
```python3
score = 0
for line in data:
    stack = []
    for c in line:
        if c in opening.values():
            stack.append(c)
        else:
            last = stack.pop()
            if last != opening[c]:
                score += error_points[c]
                break
```

## [Parte 2](./Sol2.py)
Esta segunda parte se complica ligeramente, tenemos que encontrar los símbolos que faltan a las líneas incompletas y guardarnos
la puntuación de ese completado, una vez tengamos todas las puntuaciones, calculamos la [mediana](https://es.wikipedia.org/wiki/Mediana_(estad%C3%ADstica)).
```python3
from statistics import median

opening = {")": "(", "]": "[", "}": "{", ">": "<"}
completion_points = {"(": 1, "[": 2, "{": 3, "<": 4}

if __name__ == "__main__":
    data = [list(line.strip()) for line in open("input.txt", "r").readlines()]

    scores = []
    for line in data:
        stack = []
        for c in line:
            if c in opening.values():
                stack.append(c)
            else:
                last = stack.pop()
                if last != opening[c]:
                    break
        else:
            score = 0
            while len(stack) > 0:
                score *= 5
                score += completion_points[stack.pop()]
            scores.append(score)

    print(median(scores))
```

La lectura del input es idéntica a la del apartado anterior, lo único que cambia es la puntuación de cada símbolo y que
ahora se relacionan con los símbolos de apertura y no de cierre.

Mantenemos el código del apartado anterior, solo que no llevamos la cuenta de la puntuación, y en el caso de que no
se haya llamado a break dentro del for, recorremos los elementos sobrantes de la pila, calculamos la puntuación y la
añadimos a una lista de puntuaciones.
```python3
scores = []
for line in data:
    stack = []
    for c in line:
        if c in opening.values():
            stack.append(c)
        else:
            last = stack.pop()
            if last != opening[c]:
                break
    else:
        score = 0
        while len(stack) > 0:
            score *= 5
            score += completion_points[stack.pop()]
        scores.append(score)
```

Para terminar, calculamos la mediana de las puntuaciones.
```python3
print(median(scores))
```
