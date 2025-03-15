import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 2906

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
local_ip = socket.gethostbyname(socket.gethostname())

try:
    client_socket.sendto(local_ip.encode(), (SERVER_IP, SERVER_PORT))
    print(f"Wysłano: {local_ip}")
    response, _ = client_socket.recvfrom(1024)
    print(f"Otrzymana nazwa hosta: {response.decode()}")

finally:
    client_socket.close()
