# [Día 17](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 17  | 00:36:51 | 2499 | 0     | 01:52:27 | 4895 | 0     |

## [Parte 1](./Sol1.py)
El reto de hoy era terriblemente sencillo, la primera parte consistía en calcular la altura máxima a la que podemos lanzar
una sonda para que caiga en una fosa oceánica sin pasarse.
```python3
import re


def main():
    left, right, bottom, top = \
        [list(map(int, list(re.findall("-?[0-9]+", line)))) for line in open("input.txt", "r").readlines()][0]

    vy = abs(bottom) - 1

    print(vy*(vy+1)/2)


if __name__ == "__main__":
    main()
```

La resolución es tan sencilla que la voy a comentar en un único bloque, primero con regex, obtenemos las coordenadas de los
lados de la fosa, una vez obtenidos esos datos y sabiendo que en un tiro parabólico, el objeto lanzado, vuelve a la altura desde
la que se lanzó, con la misma velocidad, pero en sentido contrario, sabemos que la velocidad más alta que podemos alcanzar ```Vmax```, es la
que hará que saliendo de y=0 con velocidad ```-(Vmax + 1)``` llegue al borde inferior de la fosa.

Por último, para obtener la altura máxima alcanzada, calculamos el número triangular correspondiente a Vmax.
```python3
    left, right, bottom, top = \
        [list(map(int, list(re.findall("-?[0-9]+", line)))) for line in open("input.txt", "r").readlines()][0]

    vy = abs(bottom) - 1

    print(vy*(vy+1)/2)
```

## [Parte 2](./Sol2.py)
Esta segunda parte tampoco es especialmente complicada, el objetivo es encontrar todas las formas posibles de lanzar la 
sonda y que entre en la fosa.

Moraleja del día de hoy: En ocasiones la solución más sencilla es la mejor (aunque sea fuerza bruta).
```python3
from math import sqrt
import re


def main():
    left, right, bottom, top = \
        [list(map(int, list(re.findall("-?[0-9]+", line)))) for line in open("input.txt", "r").readlines()][0]

    max_vy = abs(bottom) - 1
    min_vy = bottom

    min_vx = int(sqrt(left * 2 + 1 / 4) - 1 / 2)
    max_vx = right

    sols = 0
    for vy in range(min_vy, max_vy + 1):
        for vx in range(min_vx, max_vx + 1):
            x, y = 0, 0
            dvx, dvy = 0, 0
            while x <= right and y >= bottom:
                if left <= x <= right and top >= y >= bottom:
                    sols += 1
                    break
                x += vx - dvx
                y += vy + dvy
                dvy -= 1
                dvx = min(vx, dvx+1)

    print(sols)


if __name__ == "__main__":
    main()
```

Lo primero que hacemos es calcular las velocidades mínimas y máximas en cada uno de los ejes. La máxima de y ya la hemos calculado
en la parte anterior, y su mínima es simplemente una velocidad hacia abajo tal que, en un paso llega al borde inferior de la fosa.
La mínima de la x corresponde a la inversa del número triangular del borde izquierdo y su máxima, una velocidad tal, que en un
único paso llega al borde derecho.
```python3
max_vy = abs(bottom) - 1
min_vy = bottom

min_vx = int(sqrt(left * 2 + 1 / 4) - 1 / 2)
max_vx = right
```

Una vez con el rango de velocidades acotado, solo tenemos que probar todas las combinaciones posibles, desplazando un punto
según las velocidades y comprobando si entra o se pasa.
```python3
sols = 0
for vy in range(min_vy, max_vy + 1):
    for vx in range(min_vx, max_vx + 1):
        x, y = 0, 0
        dvx, dvy = 0, 0
        while x <= right and y >= bottom:
            if left <= x <= right and top >= y >= bottom:
                sols += 1
                break
            x += vx - dvx
            y += vy + dvy
            dvy -= 1
            dvx = min(vx, dvx+1)
```
