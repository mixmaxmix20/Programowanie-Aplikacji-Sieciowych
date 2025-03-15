import socket

# Adres IP i port serwera
SERVER_IP = "127.0.0.1"
SERVER_PORT = 2907

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hostname = socket.gethostname()

try:
    client_socket.sendto(hostname.encode(), (SERVER_IP, SERVER_PORT))
    print(f"Wysłano hostname: {hostname}")
    response, _ = client_socket.recvfrom(4096)
    print(f"Otrzymany adres IP: {response.decode()}")

finally:
    client_socket.close()
