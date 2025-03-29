import socket

HOST = '127.0.0.1'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    message = input("Wpisz wiadomość: ")
    client_socket.sendall(message.encode())
    response = client_socket.recv(1024).decode()
    print(f"Odebrano echo: {response}")