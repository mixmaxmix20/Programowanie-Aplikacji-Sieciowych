import socket

HOST = '127.0.0.1'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Serwer nasłuchuje na {HOST}:{PORT}")

    while True:
        client_conn, client_addr = server_socket.accept()
        with client_conn:
            print(f"Połączono z {client_addr}")

            data = client_conn.recv(1024)
            if data:
                print(f"Odebrano: {data.decode()}")

                client_conn.sendall(data)
                print(f"Odesłano {data}")

        print("Połączenie zamknięte")