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
