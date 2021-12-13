# [Día 13](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 13  | 00:12:22 | 646  | 0     | 00:18:32 | 733  | 0     |

## [Parte 1](./Sol1.py)
Vale, el problema de hoy es algo ligero, en la primera parte, simplemente hay que “reflejar” los puntos a la derecha o debajo
del primer eje que te dan como input y contar cuantos puntos quedan, teniendo en cuenta que los superpuestos cuentan como solo uno.
```python3
import re


def main():
    dots_re = re.compile(r"([0-9]+),([0-9]+)")
    dots = [list(dots_re.match(line).groups()) for line in open("input.txt", "r").readlines() if dots_re.match(line)]
    dots = set([(int(dot[0]), int(dot[1])) for dot in dots])

    fold_re = re.compile(r"fold along ([xy])=([0-9]+)")
    folds = [list(fold_re.match(line).groups()) for line in open("input.txt", "r").readlines() if fold_re.match(line)]
    folds = [(fold[0], int(fold[1])) for fold in folds]

    for ax, line in folds[0:1]:
        if ax == "x":
            new_dots = set([(x, y) for (x, y) in dots if x < line])
            new_dots.update([(2 * line - x, y) for (x, y) in dots if x > line])
            dots = new_dots
        else:
            new_dots = set([(x, y) for (x, y) in dots if y < line])
            new_dots.update([(x, 2 * line - y) for (x, y) in dots if y > line])
            dots = new_dots

    print(len(dots))


if __name__ == "__main__":
    main()
```

Primero leemos la entrada, utilizamos [regex](https://es.wikipedia.org/wiki/Expresi%C3%B3n_regular) para detectar los dos
tipos de líneas del input, para después castear a int los elementos necesarios.
```python3
dots_re = re.compile(r"([0-9]+),([0-9]+)")
dots = [list(dots_re.match(line).groups()) for line in open("input.txt", "r").readlines() if dots_re.match(line)]
dots = set([(int(dot[0]), int(dot[1])) for dot in dots])

fold_re = re.compile(r"fold along ([xy])=([0-9]+)")
folds = [list(fold_re.match(line).groups()) for line in open("input.txt", "r").readlines() if fold_re.match(line)]
folds = [(fold[0], int(fold[1])) for fold in folds]
```

El código para calcular la posición de los puntos tras el doblado es sencillo, trabajamos con sets, para que los elementos
repetidos se traten como un único elemento, primero dejamos en el resultado todos los puntos anteriores al eje de doblado
para posteriormente incluir los puntos reflejados en ese eje con la sencilla fórmula ```2 * line - x```. 

Notad que lo he implementado como un for pese a que en el enunciado nos advertían de que solo usáramos la primera instrucción, 
esto es porque estaba claro que en la segunda parte las tendríamos que usar todas y de este modo ya lo tenía todo preparado.
```python3
for ax, line in folds[0:1]:
    if ax == "x":
        new_dots = set([(x, y) for (x, y) in dots if x < line])
        new_dots.update([(2 * line - x, y) for (x, y) in dots if x > line])
        dots = new_dots
    else:
        new_dots = set([(x, y) for (x, y) in dots if y < line])
        new_dots.update([(x, 2 * line - y) for (x, y) in dots if y > line])
        dots = new_dots
```

Por último se muestra por pantalla la longitud del set de puntos.
```python3
print(len(dots))
```

## [Parte 2](./Sol2.py)
Esta segunda parte, como preveíamos en la anterior, hay que realizar todos los pliegues, y después mostrar por pantalla la 
imagen que dibujan los puntos restantes.
```python3
import re


def main():
    dots_re = re.compile(r"([0-9]+),([0-9]+)")
    dots = [list(dots_re.match(line).groups()) for line in open("input.txt", "r").readlines() if dots_re.match(line)]
    dots = set([(int(dot[0]), int(dot[1])) for dot in dots])

    fold_re = re.compile(r"fold along ([xy])=([0-9]+)")
    folds = [list(fold_re.match(line).groups()) for line in open("input.txt", "r").readlines() if fold_re.match(line)]
    folds = [(fold[0], int(fold[1])) for fold in folds]

    for ax, line in folds:
        if ax == "x":
            new_dots = set([(x, y) for (x, y) in dots if x < line])
            new_dots.update([(2 * line - x, y) for (x, y) in dots if x > line])
            dots = new_dots
        else:
            new_dots = set([(x, y) for (x, y) in dots if y < line])
            new_dots.update([(x, 2 * line - y) for (x, y) in dots if y > line])
            dots = new_dots

    for y in range(0, max(dy for (_, dy) in dots)+1):
        for x in range(0, max(dx for (dx, _) in dots)+1):
            print("#" if (x, y) in dots else " ", end="")
        print("")


if __name__ == "__main__":
    main()
```

Con respecto al apartado anterior solo cambia el bucle for, que ahora sí que recorre todos los elementos, y el print,
que ahora dibuja para todo x en el rango de valores desde 0 hasta el punto más a la derecha y para todo y desde 0
hasta el punto más bajo, un # si hay un punto en esa posición o un espacio en blanco en caso contrario.
```python3
for y in range(0, max(dy for (_, dy) in dots)+1):
    for x in range(0, max(dx for (dx, _) in dots)+1):
        print("#" if (x, y) in dots else " ", end="")
    print("")
```

El resultado de la ejecución sería algo como esto:
```python3
###  #    #  #   ## ###  ###   ##   ## 
#  # #    # #     # #  # #  # #  # #  #
###  #    ##      # #  # ###  #  # #   
#  # #    # #     # ###  #  # #### # ##
#  # #    # #  #  # # #  #  # #  # #  #
###  #### #  #  ##  #  # ###  #  #  ###
```
