import socket

HOST = '127.0.0.1'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    message = input("Wpisz wiadomość: ")
    client_socket.sendto(message.encode(), (HOST, PORT))
    response, _ = client_socket.recvfrom(1024)
    print(f"Odebrano echo: {response.decode()}")