# [Día 8](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 8   | 00:09:56 | 1866 | 0     | 01:28:56 | 4089 | 0     |

## [Parte 1](./Sol1.py)
Esta primera parte es peligrosamente fácil, simplemente tenemos que contar la cantidad de “palabras” con 2, 4, 3 o 7
letras.
```python3
if __name__ == "__main__":
    data = [line.strip().split("|") for line in open("input.txt", "r").readlines()]
    inputs = [inp.split() for inp, _ in data]
    outputs = [out.split() for _, out in data]

    res = 0
    for line in outputs:
        res += sum((len(out) == 7 or len(out) == 2 or len(out) == 3 or len(out) == 4) for out in line)

    print(res)
```

Para leer la entrada, primero dividimos cada línea por la barra vertical, y cada una de las dos sublistas la dividimos
por los espacios en blanco.
```python3
data = [line.strip().split("|") for line in open("input.txt", "r").readlines()]
inputs = [inp.split() for inp, _ in data]
outputs = [out.split() for _, out in data]
```

Hecho esto, vamos contando cuantos elementos de la parte derecha de la barra tienen la longitud que nos piden.
```python3
res = 0
for line in outputs:
    res += sum((len(out) == 7 or len(out) == 2 or len(out) == 3 or len(out) == 4) for out in line)
```

## [Parte 2](./Sol2.py)
Esta segunda parte consiste en, a partir de los segmentos que se iluminan para cada número, decodificar el valor 
de cada uno. Y ha sido el primer reto del año que, tras una hora sin conseguir nada, he tenido que pararme los
pies, y decirme a mi mismo “Para, no te hagas más daño y busca ayuda”. Y es algo maravilloso en realidad, porque
en estos retos que no sabes resolver, es en los que más aprendes, buscando las soluciones de la gente y entendiéndolas,
así que eso he hecho, me he metido en el foro oficial de [AOC en reddit](https://www.reddit.com/r/adventofcode/), me he 
ido a la sección del [reto de hoy](https://www.reddit.com/r/adventofcode/comments/rbj87a/2021_day_8_solutions/) y he 
buscado entre los comentarios hasta encontrar una [solución](https://www.reddit.com/r/adventofcode/comments/rbj87a/comment/hnor7je/?utm_source=share&utm_medium=web2x&context=3) 
elegante y compacta, le he echado un vistazo, he entendido su razonamiento, la he cerrado y me he puesto a 
implementarla a mi manera.
```python3
if __name__ == "__main__":
    data = [line.strip().split("|") for line in open("input.txt", "r").readlines()]
    inputs = [[set(list(digit)) for digit in inp.split()] for inp, _ in data]
    outputs = [[set(list(digit)) for digit in out.split()] for _, out in data]

    res = 0
    for inp, out in zip(inputs, outputs):
        code = [set()] * 10
        code[1] = [digit for digit in inp if len(digit) == 2][0]
        code[4] = [digit for digit in inp if len(digit) == 4][0]
        code[7] = [digit for digit in inp if len(digit) == 3][0]
        code[8] = [digit for digit in inp if len(digit) == 7][0]

        code[9] = [digit for digit in inp if len(digit) == 6 and len(digit - set.union(code[4], code[7])) == 1][0]
        code[6] = [digit for digit in inp if len(digit) == 6 and len(set.intersection(digit, code[1])) == 1][0]
        code[0] = [digit for digit in inp if len(digit) == 6 and digit != code[6] and digit != code[9]][0]

        code[5] = [digit for digit in inp if len(digit) == 5 and len(code[6] - digit) == 1][0]
        code[3] = [digit for digit in inp if len(digit) == 5 and digit != code[5] and len(code[9] - digit) == 1][0]
        code[2] = [digit for digit in inp if len(digit) == 5 and digit != code[3] and digit != code[5]][0]

        value = 0
        for digit in out:
            value *= 10
            value += code.index(set(list(digit)))
        res += value
    print(res)
```

Para empezar, como siempre, el input. En este caso empezamos igual que en el apartado anterior, solo que para cada
“palabra”, la convertimos en una lista de caracteres y esa lista a un set (Para que ignore el orden).
```python3
data = [line.strip().split("|") for line in open("input.txt", "r").readlines()]
inputs = [[set(list(digit)) for digit in inp.split()] for inp, _ in data]
outputs = [[set(list(digit)) for digit in out.split()] for _, out in data]
```

Y ahora viene lo interesante, vamos a intentar averiguar que set representa a cada número, para ello, primero
cogemos los sets correspondientes al 1, 4, 7 y 8 (que tienen una cantidad de segmentos activos distinta a todos
los demás), y a partir de estos dígitos, vamos realizando operaciones con sets para descubrir los demás, por ejemplo:

Sabemos que la unión entre el 4 y el 7, equivale al 9 sin el segmento de abajo (Como se muestra en la figura de abajo),
por lo tanto, si encontramos un dígito, con seis segmentos activos, al que quitandole la unión entre el 4 y el 7, le
queda solo un segmento activo, ese será a la fuerza el 9.
```
 ....       ####       #### 
#    #     .    #     #    #
#    #     .    #     #    #
 ####   +   ....   =   #### 
.    #     .    #     .    #
.    #     .    #     .    #
 ....       ....       .... 
 ```

Pues un razonamiento muy similar se sigue para el resto de números, os animo a intentar sacarlo por vosotros mismos,
si os fijáis en el código de [hugh_tc](https://www.reddit.com/user/hugh_tc/) que he citado antes, su razonamiento difiere
bastante del mío, porque no hay una única manera de relacionar los distintos dígitos, así que os recomiendo intentarlo.
```python3
res = 0
for inp, out in zip(inputs, outputs):
    code = [set()] * 10
    code[1] = [digit for digit in inp if len(digit) == 2][0]
    code[4] = [digit for digit in inp if len(digit) == 4][0]
    code[7] = [digit for digit in inp if len(digit) == 3][0]
    code[8] = [digit for digit in inp if len(digit) == 7][0]

    code[9] = [digit for digit in inp if len(digit) == 6 and len(digit - set.union(code[4], code[7])) == 1][0]
    code[6] = [digit for digit in inp if len(digit) == 6 and len(set.intersection(digit, code[1])) == 1][0]
    code[0] = [digit for digit in inp if len(digit) == 6 and digit != code[6] and digit != code[9]][0]

    code[5] = [digit for digit in inp if len(digit) == 5 and len(code[6] - digit) == 1][0]
    code[3] = [digit for digit in inp if len(digit) == 5 and digit != code[5] and len(code[9] - digit) == 1][0]
    code[2] = [digit for digit in inp if len(digit) == 5 and digit != code[3] and digit != code[5]][0]
```

Una vez obtenida la representación de los dígitos, en cada línea calculamos el valor del output y lo vamos sumando.
```python3
value = 0
for digit in out:
    value *= 10
    value += code.index(set(list(digit)))
res += value
```
