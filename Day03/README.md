# [Día 3](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 3   | 00:05:44 | 794  | 0     | 00:25:28 | 1742 | 0     |

## [Parte 1](./Sol1.py)
La primera parte no era complicada, simplemente consiste en irse quedando con el bit más y menos común en 
cada posición del string, convertirlos a decimal y calcular el producto.
```python3
from collections import Counter

if __name__ == "__main__":
    data = [list(line.strip()) for line in open("input.txt", "r").readlines()]
    data = [Counter(bit) for bit in zip(*data)]

    gamma = "".join([max(bit, key=bit.get) for bit in data])
    epsilon = "".join([min(bit, key=bit.get) for bit in data])

    print(int(gamma, 2) * int(epsilon, 2))
```

La lectura de la entrada, ya es un poco más compleja, primero convertimos cada línea de la entrada en una
lista, para posteriormente cambiar filas por columnas y realizar un conteo del número de bits en cada posición.

Como los retos aún son asequibles, entiendo que habrá gente no muy experta intentando completarlos, así que
permitidme detenerme un momento a explicar con más detalle la segunda línea. Lo que hace ```zip(*data)``` es
coger cada elemento de las sublistas que contiene data y agruparlos por posición, por ejemplo, si data fuera 
```[[1, 0, 1], [0, 1, 1]]```, el resultado del zip sería ```[[1, 0], [0, 1], [1, 1]]```. Y counter básicamente
cuenta cuantos elementos de cada hay en cada lista, en este caso cuantos unos y ceros hay en cada posición.
```python3
data = [list(line.strip()) for line in open("input.txt", "r").readlines()]
data = [Counter(bit) for bit in zip(*data)]
```

Una vez leído correctamente el input, terminar el reto es trivial, simplemente nos quedamos en gamma, con el 
máximo utilizando como clave el get del counter y para epsilon con el mínimo (posteriormente los unimos en un
único string con el join).

Para los jóvenes y no tan jóvenes programadores que no sepan que es esto de la key, cuando python calcule el 
máximo de cada bit, se encontrará con un objeto contador, que le va a devolver la lista de valores que ha contado,
en este caso ```["0", "1"]```, si no pusiéramos la key, python compararía los textos, pero lo que queremos es que
compare la cantidad de cada uno, esa cantidad se obtiene con el get.
```python3
gamma = "".join([max(bit, key=bit.get) for bit in data])
epsilon = "".join([min(bit, key=bit.get) for bit in data])
```

Por último convertimos a int cada valor, indicando que está en base 2 (binario).
```python3
print(int(gamma, 2) * int(epsilon, 2))
```

## [Parte 2](./Sol2.py)
Las cosas ya empiezan a complicarse, en este caso no porque el reto sea especialmente complicado, sino porque
la implementación se puede volver más engorrosa y propiciar la aparición de bugs. En este caso el reto consiste
en ir filtrando las listas en función de una regla dada en el enunciado (Cuidad, porque la regla de conteo, esta
vez se aplica para los resultados válidos que se están procesando en ese momento y no sobre la entrada).
```python3
from collections import Counter
from copy import copy

if __name__ == "__main__":
    data = [line.strip() for line in open("input.txt", "r").readlines()]

    oxygen = copy(data)
    for i in range(len(data[0])):
        if len(oxygen) == 1:
            break
        
        c = Counter([line[i] for line in oxygen])
        if c.get("0") > c.get("1"):
            oxygen = list(filter(lambda x: x[i] == "0", oxygen))
        else:
            oxygen = list(filter(lambda x: x[i] == "1", oxygen))

    co2 = copy(data)
    for i in range(len(data[0])):
        if len(co2) == 1:
            break
        
        c = Counter([line[i] for line in co2])
        if c.get("0") > c.get("1"):
            co2 = list(filter(lambda x: x[i] == "1", co2))
        else:
            co2 = list(filter(lambda x: x[i] == "0", co2))

    print(int("".join(co2), 2) * int("".join(oxygen), 2))
```

La lectura de los datos es igual que en el apartado anterior, solo que no se usa el counter, así que, como va
siendo costumbre nos la saltamos para empezar con el algoritmo, voy a analizar solo uno de los bucles, porque
ambos son equivalentes.

Guardamos en una variable, una copia de la entrada, para poder seguir usando la original más adelante y vamos
filtrando posición por posición hasta que solo queda un valor válido. En cada iteración, calculamos el conteo
de la posición actual y aplicamos el filtrado.
```python3
oxygen = copy(data)
for i in range(len(data[0])):
    if len(oxygen) == 1:
        break
    c = Counter([line[i] for line in oxygen])
    if c.get("0") > c.get("1"):
        oxygen = list(filter(lambda x: x[i] == "0", oxygen))
    else:
        oxygen = list(filter(lambda x: x[i] == "1", oxygen))
```

Por último, indicar que se podría compactar el if-else, de la siguiente forma, pero por claridad, 
prefiero no compactarlo tanto.
```python3
oxygen = list(filter(lambda x: x[i] == ("1" if c.get("0") > c.get("1") else "0"), oxygen))
```
