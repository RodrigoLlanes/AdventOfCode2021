# [Día 14](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 14  | 00:14:50 | 1975 | 0     | 00:36:31 | 1341 | 0     |

## [Parte 1 y 2](./Sol2.py)
Volvemos con uno de estos problemas en los que la primera parte puede funcionar con una versión ineficiente, pero la
segunda no, en este caso durante la primera parte no se me ocurría como hacerlo eficiente así que implementé una versíon
ineficiente para ir ganando tiempo e implementé la versión correcta en la segunda parte, como el código de la segunda es 
mejor y vale para las dos, solo voy a explicar ese y si alguien, por algún motivo quiere ver mi versión de la primera [aquí
tenéis un enlace](Sol1.py).

Dicho todo esto, en ambas partes el objetivo es ir llevando la cuenta de las inserciones, pero nos da igual el orden,
así que lo que vamos a hacer es llevar por un lado la cuenta de los símbolos individuales y por otro de los pares de símbolos,
de modo que podamos saber que elementos se pueden insertar y cuantos de cada.
```python3
import re
from collections import defaultdict
from copy import deepcopy


def main():
    data = [line.strip() for line in open("input.txt", "r").readlines()]
    raw_pattern = data[0]

    values = defaultdict(int, {k: raw_pattern.count(k) for k in set(list(raw_pattern))})

    pattern = defaultdict(int)
    for i in range(len(raw_pattern)-1):
        pair = raw_pattern[i:i+2]
        pattern[pair] += 1

    insertions = [list(re.match(r"(\w+) -> (\w+)", line).groups()) for line in data[2:]]
    insertions = {k: v for (k, v) in insertions}

    for n in range(40):
        new_pattern = deepcopy(pattern)
        for (k, v) in pattern.items():
            if k in insertions:
                inserted = insertions[k]
                new_pattern[k] -= v
                new_pattern[k[0] + inserted] += v
                new_pattern[inserted + k[1]] += v
                values[inserted] += v
        pattern = new_pattern

    print(max(values.values()) - min(values.values()))


if __name__ == "__main__":
    main()
```

Como siempre, empezamos con la lectura de los datos, lo primero es leer las líneas y quedarnos con la primera que es el patrón,
y a continuación dividimos la limpieza de los datos en 3 fases.
1. Creamos un ```defaultdict``` y para cada símbolo del patrón insertamos el par ```(símbolo, número de ocurrencias)```.
2. Creamos otro ```defaultdict``` y para cada par de símbolos del patrón, insertamos el par ```(par de símbolos, número de ocurrencias)```.
3. Creamos un diccionario cuya clave es el par en el que se inserta y su valor el símbolo a insertar.
```python3
data = [line.strip() for line in open("input.txt", "r").readlines()]
raw_pattern = data[0]

values = defaultdict(int, {k: raw_pattern.count(k) for k in set(list(raw_pattern))})

pattern = defaultdict(int)
for i in range(len(raw_pattern)-1):
    pair = raw_pattern[i:i+2]
    pattern[pair] += 1

insertions = [list(re.match(r"(\w+) -> (\w+)", line).groups()) for line in data[2:]]
insertions = {k: v for (k, v) in insertions}
```

Con estos tres datos ya podemos aplicar nuestro algoritmo, en cada iteración copiamos el diccionario pattern, y para cada 
par ```(clave, valor)``` en el original, si la clave aparece en el diccionario de inserciones, eliminamos las ocurrencias
de la clave en el diccionario que hemos creado, incrementamos el número de ocurrencias del par ```(primer símbolo de la clave, símbolo insertado)```
en el número de ocurrencias de la clave y lo mismo para el par ```(símbolo insertado, segundo símbolo de la clave)``` y por último
incrementamos en la misma cantidad el valor del símbolo insertado.
```python3
for n in range(40):
    new_pattern = deepcopy(pattern)
    for (k, v) in pattern.items():
        if k in insertions:
            inserted = insertions[k]
            new_pattern[k] -= v
            new_pattern[k[0] + inserted] += v
            new_pattern[inserted + k[1]] += v
            values[inserted] += v
    pattern = new_pattern
```

Por último se muestra por pantalla el máximo número de ocurrencias menos el mínimos.
```python3
print(max(values.values()) - min(values.values()))
```
