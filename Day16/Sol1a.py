
def parse(hexadecimal):
    binary = bin(int(hexadecimal, 16))[2:].zfill(len(hexadecimal) * 4)
    packets = []
    while binary != len(binary) * '0':
        p_version = int(binary[:3], 2)
        p_type = int(binary[3:6], 2)
        i = 6
        if p_type == 4:
            while binary[i] == '1':
                i += 5
            i += 4
            p_data = binary[6:i+1]
            packets.append((p_version, p_type, p_data))
        else:
            p_len_id = int(binary[i], 2)
            i += 15 if p_len_id == 0 else 11
            p_len = binary[7:i+1]
            packets.append((p_version, p_type, p_len_id, p_len))
        d = 0
        binary = binary[i+1+d:]
    return packets


def main():
    packets = parse([line.strip() for line in open("input.txt", "r").readlines()][0])
    print(sum(packet[0] for packet in packets))


if __name__ == "__main__":
    main()
