import socket

HOST = '127.0.0.1'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    while True:
        try:
            hostname = input("Podaj nazwę hosta: ")
            client_socket.sendto(hostname.encode(), (HOST, PORT))
            response, _ = client_socket.recvfrom(1024)
            print(response.decode())
        except KeyboardInterrupt:
            print("\nZamykanie klienta...")
            break