import socket

HOST = '127.0.0.1'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    while True:
        try:
            expression = input("Wpisz działanie (np. 5 + 3): ")
            client_socket.sendto(expression.encode(), (HOST, PORT))
            response, _ = client_socket.recvfrom(1024)
            print(response.decode())
        except KeyboardInterrupt:
            print("\nZamykanie klienta...")
            break