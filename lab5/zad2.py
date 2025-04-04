import socket
import random
from threading import Thread

HOST = '127.0.0.1'
PORT = 2912

def handle_client(conn, addr):
    print(f"Nowe połączenie: {addr}")
    target_number = random.randint(1, 100)
    print(f"Wylosowana liczba dla {addr}: {target_number}")

    try:
        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            print(f"{addr} zgaduje: {data}")

            try:
                guess = int(data)
            except ValueError:
                conn.sendall("To nie jest liczba!\n".encode())
                continue

            if guess < target_number:
                conn.sendall("Za mało!\n".encode())
            elif guess > target_number:
                conn.sendall("Za dużo!\n".encode())
            else:
                conn.sendall("Gratulacje! Udało się!\n".encode())
                break

    finally:
        conn.close()
        print(f"Połączenie z {addr} zamknięte")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Serwer nasłuchuje na {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            thread = Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    start_server()