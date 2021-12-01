# [Día 1](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 1   | 00:02:45 | 1224 | 0     | 00:04:35 | 503  | 0     |

## [Parte 1](./Sol1.py)
Primer día, problema facilito, como siempre, para ir calentando motores, en este reto 
simplemente hay que ir incrementando un contador cada vez que el valor de una línea es 
mayor al de la línea anterior.
```python3
if __name__ == "__main__":
    data = [int(line.strip()) for line in open("input.txt", "r").readlines()]

    inc = 0
    for i in range(1, len(data)):
        if data[i-1] < data[i]:
            inc += 1
    
    print(inc)
```

Primero leemos el fichero de entrada convirtiendo cada línea a int.
```python3
data = [int(line.strip()) for line in open("input.txt", "r").readlines()]
```

Y para cada línea a partir de la segunda, incrementamos el contador ```inc``` si la 
línea actual es mayor que la anterior.
```python3
inc = 0
for i in range(1, len(data)):
    if data[i-1] < data[i]:
        inc += 1
```

Esta segunda parte sería equivalente a:
```python3
inc = sum([data[i-1] < data[i] for i in range(1, len(data))])
```

Pero por claridad, he dejado la primera.

## [Parte 2](./Sol2.py)
Segunda parte, mismo procedimiento que en el apartado anterior, pero en lugar de comparar
una línea con la anterior hay que comparar la suma de la línea actual y las dos siguientes
con la suma de la anterior, la actual y la inmediatamente siguiente.
```python3
if __name__ == "__main__":
    data = [int(line.strip()) for line in open("input.txt", "r").readlines()]

    inc = 0
    for i in range(1, len(data) - 2):
        prev = data[i - 1] + data[i] + data[i + 1]
        deep = data[i] + data[i + 1] + data[i + 2]
        if prev < deep:
            inc += 1

    print(inc)
```

La lectura de los datos es igual que en el apartado anterior, así que no nos vamos a molestar
en repetirlo, y vamos a pasar directamente al conteo.

Es lo mismo que el apartado anterior, lo único que cambia es que al tener que "mirar", dos
líneas hacia delante, en el rango, le restamos dos a la longitud de data, y calculamos prev 
y curr, en realidad se podría hacer dentro del if, pero dejándolos fuera se hace más legible.
```python3
inc = 0
for i in range(1, len(data) - 2):
    prev = data[i - 1] + data[i] + data[i + 1]
    curr = data[i] + data[i + 1] + data[i + 2]
    if prev < curr:
        inc += 1
```

El cálculo de prev y curr, se podría acortar de la siguiente manera:
```python3
prev = sum(data[i - 1:i + 2])
curr = sum(data[i:i + 3])
```

E incluso se podría ir enviando el curr anterior a través de una variable externa al for,
pero tampoco es necesario a estas alturas optimizar tanto el programa y así se hace más 
intuitivo.