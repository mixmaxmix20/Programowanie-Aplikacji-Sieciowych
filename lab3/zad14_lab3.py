import socket

upd_datagram = "ed 74 0b 55 00 24 ef fd 70 72 6f 67 72 61 6d 6d 69 6e 67 20 69 6e 20 70 79 74 68 6f 6e 20 69 73 20 66 75 6e"

upd_datagram_splited = upd_datagram.split()

source_port = int("".join(upd_datagram_splited[0:2]), 16)
destination_port = int("".join(upd_datagram_splited[2:4]), 16)
data = bytes.fromhex("".join(upd_datagram_splited[8:])).decode("utf-8")
message = f"zad14odp;src;{source_port};dst;{destination_port};data;{data}"

SERVER_IP = "127.0.0.1"
SERVER_PORT = 2910

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))
    print(f"Wysłano: {message}")
    response, _ = client_socket.recvfrom(1024)
    print(f"Odpowiedz: {response.decode()}")

finally:
    client_socket.close()