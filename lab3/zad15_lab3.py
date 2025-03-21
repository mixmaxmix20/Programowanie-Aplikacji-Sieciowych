import socket

hex_packet = """
45 00 00 4e f7 fa 40 00 38 06 9d 33 d4 b6 18 1b
c0 a8 00 02 0b 54 b9 a6 fb f9 3c 57 c1 0a 06 c1
80 18 00 e3 ce 9c 00 00 01 01 08 0a 03 a6 eb 01
00 0b f8 e5 6e 65 74 77 6f 72 6b 20 70 72 6f 67
72 61 6d 6d 69 6e 67 20 69 73 20 66 75 6e
"""

bytes_list = hex_packet.strip().split()

version = int(bytes_list[0], 16) >> 4
src_ip = ".".join(str(int(b, 16)) for b in bytes_list[12:16])
dst_ip = ".".join(str(int(b, 16)) for b in bytes_list[16:20])
protocol = int(bytes_list[9], 16)

if protocol == 6:
    tcp_start = 20
    src_port = int(bytes_list[tcp_start] + bytes_list[tcp_start + 1], 16)
    dst_port = int(bytes_list[tcp_start + 2] + bytes_list[tcp_start + 3], 16)

    data_offset_byte = int(bytes_list[tcp_start + 12], 16)
    header_length = (data_offset_byte >> 4) * 4

    data_start = tcp_start + header_length
    data_bytes = bytes.fromhex("".join(bytes_list[data_start:]))
    data = data_bytes.decode("utf-8", errors="replace")

msg_a = f"zad15odpA;ver;{version};srcip;{src_ip};dstip;{dst_ip};type;{protocol}"
msg_b = f"zad15odpB;srcport;{src_port};dstport;{dst_port};data;{data}"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server = ("127.0.0.1", 2911)

try:
    sock.sendto(msg_a.encode(), server)
    print(f"Wysłano A: {msg_a}")
    resp = sock.recvfrom(1024)[0].decode()
    print(f"Odpowiedź A: {resp}")

    if resp == "TAK":
        sock.sendto(msg_b.encode(), server)
        print(f"Wysłano B: {msg_b}")
        resp = sock.recvfrom(1024)[0].decode()
        print(f"Odpowiedź B: {resp}")

finally:
    sock.close()
