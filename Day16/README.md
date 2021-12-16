# [Día 16](./)
| Day | Time     | Rank | Score | Time     | Rank | Score |
|-----|----------|------|-------|----------|------|-------|
| 16  | 00:41:30 | 889  | 0     | 01:31:53 | 2202 | 0     |

## [Parte 1](./Sol1b.py)
El reto de hoy no era en absoluto complicado, pero si largo y delicado de implementar, la primera parte la implementé primero
de otra forma menos elegante y luego la modifiqué para poder completar el segundo reto, de modo que voy a centrarme en esta 
segunda implementación, por si a alguien le interesa, aquí os dejo un enlace a mi [primera versión](./Sol1a.py) de la primera parte.
```python3
def parse_data(data):
    bin_code = ""
    for i in range(0, len(data)-1, 5):
        bin_code += data[i+1:i+5]
    return int(bin_code, 2)


def parse(hexadecimal):
    binary = bin(int(hexadecimal, 16))[2:].zfill(len(hexadecimal) * 4)

    def get_next_packet():
        nonlocal binary
        p_version, binary = int(binary[:3], 2), binary[3:]
        p_type, binary = int(binary[:3], 2), binary[3:]
        if p_type == 4:
            i = 0
            while binary[i] == '1':
                i += 5
            p_data, binary = parse_data(binary[:i+5]), binary[i+5:]
            return [p_version, p_type, p_data]
        else:
            p_len_id, binary = int(binary[:1], 2), binary[1:]
            if p_len_id == 0:
                p_len, binary = int(binary[:15], 2), binary[15:]
                package = [p_version, p_type, []]
                s_len = len(binary)
                while s_len - len(binary) < p_len:
                    package[2].append(get_next_packet())
                return package
            else:
                p_len, binary = int(binary[:11], 2), binary[11:]
                return [p_version, p_type, [get_next_packet() for _ in range(p_len)]]
    return get_next_packet()


def main():
    packet = parse([line.strip() for line in open("input.txt", "r").readlines()][0])

    def id_sum(pack):
        if pack[1] == 4:
            return pack[0]
        else:
            return pack[0] + sum(id_sum(sub) for sub in pack[2])

    print(id_sum(packet))


if __name__ == "__main__":
    main()
```

Básicamente el grueso del problema, es la lectura de los datos, primero tenemos la función ```parse_data```, que de acuerdo 
a la definición del problema, elimina el primer bit de cada grupo de 5, para después hacer la conversión a int.
```python3
def parse_data(data):
    bin_code = ""
    for i in range(0, len(data)-1, 5):
        bin_code += data[i+1:i+5]
    return int(bin_code, 2)
```

Y después tenemos la función ```parse```, lo primero que hace es convertir de hexadecimal a binario para posteriormente llamar
a ```get_next_packet``` que va a devolver el siguiente paquete, con sus sub-paquetes.

Lo primero que hace ```get_next_packet``` es calcular la versión y el tipo del paquete, si os fijais, cada vez que accedo
a la variable binary, hago algo como esto: 
```p_version, binary = int(binary[:3], 2), binary[3:] ```
De este modo, lo que conseguimos es ir eliminando las partes ya procesadas para poder trabajar siempre con la cabeza del
texto.

Una vez obtenido el tipo del paquete:
- Si es 4, iteramos de 5 en 5 bits hasta encontrar un grupo que empieza por 0, lo parseamos
y devolvemos el paquete.
  
- Si es distinto de 4, calculamos el id de la longitud:

    - Si es 0, calculamos el número de bits que ocupan los sub-paquetes y vamos obteniendo paquetes hasta cumplir con el tamaño,
      una vez tenemos todos los paquetes necesarios, devolvemos el paquete principal con todos los sub-paquetes en su interior.
    - Si es 1, calculamos el número de sub-paquetes del paquete actual, los obtenemos y devolvemos el paquete con todos sus sub-paquetes.

```python3
def parse(hexadecimal):
    binary = bin(int(hexadecimal, 16))[2:].zfill(len(hexadecimal) * 4)

    def get_next_packet():
        nonlocal binary
        p_version, binary = int(binary[:3], 2), binary[3:]
        p_type, binary = int(binary[:3], 2), binary[3:]
        if p_type == 4:
            i = 0
            while binary[i] == '1':
                i += 5
            p_data, binary = parse_data(binary[:i+5]), binary[i+5:]
            return [p_version, p_type, p_data]
        else:
            p_len_id, binary = int(binary[:1], 2), binary[1:]
            if p_len_id == 0:
                p_len, binary = int(binary[:15], 2), binary[15:]
                package = [p_version, p_type, []]
                s_len = len(binary)
                while s_len - len(binary) < p_len:
                    package[2].append(get_next_packet())
                return package
            else:
                p_len, binary = int(binary[:11], 2), binary[11:]
                return [p_version, p_type, [get_next_packet() for _ in range(p_len)]]
    return get_next_packet()
```

Una vez obtenido el paquete principal que contiene al resto, iteramos en cada sub-paquete y vamos sumando sus ids.
```python3
packet = parse([line.strip() for line in open("input.txt", "r").readlines()][0])

def id_sum(pack):
    if pack[1] == 4:
        return pack[0]
    else:
        return pack[0] + sum(id_sum(sub) for sub in pack[2])

print(id_sum(packet))
```



## [Parte 2](./Sol2.py)
Como siempre, esta parte supone una pequeña modificación del apartado anterior, en este caso, una vez tenemos nuestros paquetes,
asociamos una operación a cada tipo y calculamos el resultado de aplicar las operaciones del paquete principal.

```python3
from functools import reduce


def parse_data(data):
    bin_code = ""
    for i in range(0, len(data)-1, 5):
        bin_code += data[i+1:i+5]
    return int(bin_code, 2)


def parse(hexadecimal):
    binary = bin(int(hexadecimal, 16))[2:].zfill(len(hexadecimal) * 4)

    def get_next_packet():
        nonlocal binary
        p_version, binary = int(binary[:3], 2), binary[3:]
        p_type, binary = int(binary[:3], 2), binary[3:]
        if p_type == 4:
            i = 0
            while binary[i] == '1':
                i += 5
            p_data, binary = parse_data(binary[:i+5]), binary[i+5:]
            return [p_version, p_type, p_data]
        else:
            p_len_id, binary = int(binary[:1], 2), binary[1:]
            if p_len_id == 0:
                p_len, binary = int(binary[:15], 2), binary[15:]
                package = [p_version, p_type, []]
                s_len = len(binary)
                while s_len - len(binary) < p_len:
                    package[2].append(get_next_packet())
                return package
            else:
                p_len, binary = int(binary[:11], 2), binary[11:]
                return [p_version, p_type, [get_next_packet() for _ in range(p_len)]]
    return get_next_packet()


def execute(packet):
    p_type = packet[1]
    sub_packets = [execute(p) for p in packet[2]] if p_type != 4 else []
    if p_type == 0:
        return sum(sub_packets)
    elif p_type == 1:
        return reduce(lambda a, b: a * b, sub_packets)
    elif p_type == 2:
        return min(sub_packets)
    elif p_type == 3:
        return max(sub_packets)
    elif p_type == 4:
        return packet[2]
    elif p_type == 5:
        return 1 if sub_packets[0] > sub_packets[1] else 0
    elif p_type == 6:
        return 1 if sub_packets[0] < sub_packets[1] else 0
    elif p_type == 7:
        return 1 if sub_packets[0] == sub_packets[1] else 0


def main():
    packet = parse([line.strip() for line in open("input.txt", "r").readlines()][0])

    print(execute(packet))


if __name__ == "__main__":
    main()
```

Lo único que ha cambiado con respecto al paquete anterior, es la función execute, que recibe un paquete y calcula su resultado.

Primero obtenemos el tipo del paquete y si es distinto de 4 ejecutamos todos sus sub-paquetes, una vez hecho esto, en función
de su tipo, devuelve el resultado de realizar su operación asociada a la lista de resultados de los sub-paquetes.
```python3
def execute(packet):
    p_type = packet[1]
    sub_packets = [execute(p) for p in packet[2]] if p_type != 4 else []
    if p_type == 0:
        return sum(sub_packets)
    elif p_type == 1:
        return reduce(lambda a, b: a * b, sub_packets)
    elif p_type == 2:
        return min(sub_packets)
    elif p_type == 3:
        return max(sub_packets)
    elif p_type == 4:
        return packet[2]
    elif p_type == 5:
        return 1 if sub_packets[0] > sub_packets[1] else 0
    elif p_type == 6:
        return 1 if sub_packets[0] < sub_packets[1] else 0
    elif p_type == 7:
        return 1 if sub_packets[0] == sub_packets[1] else 0
```
