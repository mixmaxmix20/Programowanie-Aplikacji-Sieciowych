import socket

tcp_datagram = "0b 54 89 8b 1f 9a 18 ec bb b1 64 f2 80 18 00 e3 67 71 00 00 01 01 08 0a 02 c1 a4 ee 00 1a 4c ee 68 65 6c 6c 6f 20 3a 29"

tcp_datagram_splited = tcp_datagram.split()

source_port = int(tcp_datagram_splited[0] + tcp_datagram_splited[1], 16)
destination_port = int(tcp_datagram_splited[2] + tcp_datagram_splited[3], 16)

data_offset_byte = int(tcp_datagram_splited[12], 16)
header_length = (data_offset_byte >> 4) * 4

data_start = header_length
data_bytes = bytes.fromhex("".join(tcp_datagram_splited[data_start:]))
data = data_bytes.decode("utf-8", errors="replace")

message = f"zad13odp;src;{source_port};dst;{destination_port};data;{data}"

SERVER_IP = "127.0.0.1"
SERVER_PORT = 2909

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))
    print(f"Wysłano: {message}")
    response, _ = client_socket.recvfrom(1024)
    print(f"Odpowiedź: {response.decode()}")

finally:
    client_socket.close()