# [Día 18](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 18  | 03:24:45 | 2730 | 0     | 03:35:53 | 2701 | 0     |

## [Parte 1](./Sol1.py)
Esta primera parte no es complicada en realidad, la problemática viene de lo complejo del enunciado, que puede llevar a confusión
o a que te olvides de algún detalle (como fue mi caso).

La idea es que tienes que realizar todas las reducciones posibles después de cada suma, **siempre que sea posible la reducción de explode** y en caso contario,
la de split.

```python3
from copy import deepcopy
from math import ceil


class Node:
    def __init__(self, prev=None, right=None, left=None, value=None):
        self.prev = prev
        self.right = right
        self.left = left
        self.value = value

    def __add__(self, other):
        left = deepcopy(self)
        right = deepcopy(other)
        res = Node(left=left, right=right)
        left.prev = res
        right.prev = res

        while res.reduce():
            continue

        return res

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.right == other.right and self.left == other.left and self.value == other.value
        return False

    def is_leaf(self):
        return self.value is not None

    def level(self):
        level = 0
        node = self
        while node.prev is not None:
            level += 1
            node = node.prev
        return level

    def root(self):
        root = self
        while root.prev is not None:
            root = root.prev
        return root

    def reduce(self):
        if self.reduce_explode():
            return True
        return self.reduce_split()

    def reduce_explode(self):
        if self.is_leaf():
            return False
        if self.right.is_leaf() and self.left.is_leaf() and self.level() >= 4:
            self.explode()
            return True
        if self.left.reduce_explode():
            return True
        if self.right.reduce_explode():
            return True

    def reduce_split(self):
        if self.is_leaf():
            if self.value >= 10:
                self.split()
                return True
            return False

        if self.left.reduce_split():
            return True
        if self.right.reduce_split():
            return True

    def explode(self):
        self.add_near_left(self.left.value)
        self.add_near_right(self.right.value)

        self.right = None
        self.left = None
        self.value = 0

    def split(self):
        self.left = Node(prev=self, value=self.value//2)
        self.right = Node(prev=self, value=ceil(self.value/2))
        self.value = None

    def add_near_left(self, n):
        if self.prev is None:
            return

        if self.prev.left is self:
            return self.prev.add_near_left(n)

        node = self.prev.left
        while not node.is_leaf():
            node = node.right

        node.value += n

    def add_near_right(self, n):
        if self.prev is None:
            return

        if self.prev.right is self:
            return self.prev.add_near_right(n)

        node = self.prev.right
        while not node.is_leaf():
            node = node.left

        node.value += n

    def __str__(self):
        if self.is_leaf():
            return str(self.value)
        return "[" + str(self.left) + ", " + str(self.right) + "]"

    def __repr__(self):
        return str(self)

    def magnitud(self):
        if self.is_leaf():
            return self.value
        return self.left.magnitud() * 3 + self.right.magnitud() * 2


def cast(line):
    res = Node()
    for c in line[1:-1]:
        if c == '[':
            if res.left is None:
                res.left = Node(prev=res)
                res = res.left
            else:
                res.right = Node(prev=res)
                res = res.right
        elif c == ']':
            res = res.prev
        elif c.isalnum():
            if res.left is None:
                res.left = Node(prev=res, value=int(c))
            else:
                res.right = Node(prev=res, value=int(c))
    return res


def main():
    data = [cast(line.strip()) for line in open("input.txt", "r").readlines()]

    res = data[0]
    for d in data[1:]:
        res += d
    print(res.magnitud())


if __name__ == "__main__":
    main()
```

La lectura de la entrada creará, para cada línea, un [árbol binario](https://es.wikipedia.org/wiki/%C3%81rbol_binario), 
e iteramos símbolo a símbolo ignorando el primer y último (porque esos corresponden al nodo raíz), realizando el siguiente procedimiento:

1. Si el símbolo es el corchete abierto, insertamos un nodo hijo en el primer hueco libre del nodo actual y lo seleccionamos como nodo actual.
2. Si es un corchete de cierre, seleccionamos al padre del nodo actual como nodo actual.
3. Si es un número, insertamos en el primer hueco libre del nodo actual un nodo hijo con el valor de ese número.
```python3
def cast(line):
    res = Node()
    for c in line[1:-1]:
        if c == '[':
            if res.left is None:
                res.left = Node(prev=res)
                res = res.left
            else:
                res.right = Node(prev=res)
                res = res.right
        elif c == ']':
            res = res.prev
        elif c.isalnum():
            if res.left is None:
                res.left = Node(prev=res, value=int(c))
            else:
                res.right = Node(prev=res, value=int(c))
    return res


def main():
    data = [cast(line.strip()) for line in open("input.txt", "r").readlines()]
```

La clase ```Node``` implementa funcionalidades típicas de un árbol binario que no me voy a parar a explicar, por el contrario,
también implementa los métodos para resolver el reto, que no son típicos, en los que me voy a centrar.

La suma de dos árboles binarios, es un nuevo árbol binario con los árboles a sumar como hijos, una vez realizada la suma, 
se reduce el árbol hasta que las reducciones ya no tengan efecto.

```python3
def __add__(self, other):
    left = deepcopy(self)
    right = deepcopy(other)
    res = Node(left=left, right=right)
    left.prev = res
    right.prev = res

    while res.reduce():
        continue

    return res
```

La reducción trata primero de reducir mediante explode, si esto no tiene ningún efecto, lo intenta mediante split.

La reducción por explode solo se puede aplicar si el nodo a reducir tiene dos hijos de tipo hoja y si su nivel es superior
o igual a 4, en caso contrario, trata de reducir a sus nodos hijos (si los tiene).

Por otra parte la reducción por split solo puede reducir un nodo hoja si su valor es superior a 10, en caso contrario, 
también trata de reducir a sus nodos hijos (si los tiene).
```python3
    def reduce(self):
        if self.reduce_explode():
            return True
        return self.reduce_split()

    def reduce_explode(self):
        if self.is_leaf():
            return False
        if self.right.is_leaf() and self.left.is_leaf() and self.level() >= 4:
            self.explode()
            return True
        if self.left.reduce_explode():
            return True
        if self.right.reduce_explode():
            return True

    def reduce_split(self):
        if self.is_leaf():
            if self.value >= 10:
                self.split()
                return True
            return False

        if self.left.reduce_split():
            return True
        if self.right.reduce_split():
            return True
```

La función explode suma el valor de su nodo izquierdo al nodo más cercano por la izquierda y el valor de su nodo derecho
al valor más cercano por su derecha. La función split, por el contrario, genera un nodo izquiero y otro derecho cada uno con el valor del
nodo original dividido entre dos, redondeado hacia abajo y hacia arriba respectivamente.
```python3
    def explode(self):
        self.add_near_left(self.left.value)
        self.add_near_right(self.right.value)

        self.right = None
        self.left = None
        self.value = 0

    def split(self):
        self.left = Node(prev=self, value=self.value//2)
        self.right = Node(prev=self, value=ceil(self.value/2))
        self.value = None

    def add_near_left(self, n):
        if self.prev is None:
            return

        if self.prev.left is self:
            return self.prev.add_near_left(n)

        node = self.prev.left
        while not node.is_leaf():
            node = node.right

        node.value += n

    def add_near_right(self, n):
        ...
```

Por último, la función magnitud, devuelve la magnitud del árbol según la ecuación dada en el enunciado.
```python3
    def magnitud(self):
        if self.is_leaf():
            return self.value
        return self.left.magnitud() * 3 + self.right.magnitud() * 2
```

## [Parte 2](./Sol2.py)
La solución a esta parte es idéntica a la del apartado anterior, únicamente cambia el hecho de calcular todas las posibles sumas, 
y obtener el máximo, en lugar de la suma total como en el apartado anterior.
```python3
from copy import deepcopy
from math import ceil


class Node:
    def __init__(self, prev=None, right=None, left=None, value=None):
        self.prev = prev
        self.right = right
        self.left = left
        self.value = value

    def __add__(self, other):
        left = deepcopy(self)
        right = deepcopy(other)
        res = Node(left=left, right=right)
        left.prev = res
        right.prev = res

        while res.reduce():
            continue

        return res

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.right == other.right and self.left == other.left and self.value == other.value
        return False

    def is_leaf(self):
        return self.value is not None

    def level(self):
        level = 0
        node = self
        while node.prev is not None:
            level += 1
            node = node.prev
        return level

    def root(self):
        root = self
        while root.prev is not None:
            root = root.prev
        return root

    def reduce(self):
        if self.reduce_explode():
            return True
        return self.reduce_split()

    def reduce_explode(self):
        if self.is_leaf():
            return False
        if self.right.is_leaf() and self.left.is_leaf() and self.level() >= 4:
            self.explode()
            return True
        if self.left.reduce_explode():
            return True
        if self.right.reduce_explode():
            return True

    def reduce_split(self):
        if self.is_leaf():
            if self.value >= 10:
                self.split()
                return True
            return False

        if self.left.reduce_split():
            return True
        if self.right.reduce_split():
            return True

    def explode(self):
        self.add_near_left(self.left.value)
        self.add_near_right(self.right.value)

        self.right = None
        self.left = None
        self.value = 0

    def split(self):
        self.left = Node(prev=self, value=self.value//2)
        self.right = Node(prev=self, value=ceil(self.value/2))
        self.value = None

    def add_near_left(self, n):
        if self.prev is None:
            return

        if self.prev.left is self:
            return self.prev.add_near_left(n)

        node = self.prev.left
        while not node.is_leaf():
            node = node.right

        node.value += n

    def add_near_right(self, n):
        if self.prev is None:
            return

        if self.prev.right is self:
            return self.prev.add_near_right(n)

        node = self.prev.right
        while not node.is_leaf():
            node = node.left

        node.value += n

    def __str__(self):
        if self.is_leaf():
            return str(self.value)
        return "[" + str(self.left) + ", " + str(self.right) + "]"

    def __repr__(self):
        return str(self)

    def magnitud(self):
        if self.is_leaf():
            return self.value
        return self.left.magnitud() * 3 + self.right.magnitud() * 2


def cast(line):
    res = Node()
    for c in line[1:-1]:
        if c == '[':
            if res.left is None:
                res.left = Node(prev=res)
                res = res.left
            else:
                res.right = Node(prev=res)
                res = res.right
        elif c == ']':
            res = res.prev
        elif c.isalnum():
            if res.left is None:
                res.left = Node(prev=res, value=int(c))
            else:
                res.right = Node(prev=res, value=int(c))
    return res


def main():
    data = [cast(line.strip()) for line in open("input.txt", "r").readlines()]

    res = 0
    for i, a in enumerate(data):
        for j, b in enumerate(data):
            if a != b:
                res = max(res, (a+b).magnitud(), (b+a).magnitud())
    print(res)


if __name__ == "__main__":
    main()
```
