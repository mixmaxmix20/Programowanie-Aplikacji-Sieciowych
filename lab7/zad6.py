import socket

HOST = 'interia.pl'
PORT = 110
USER = 'pas2017@interia.pl'
PASS = 'P4SInf2017'

def recv_all(sock):
    data = b''
    while True:
        part = sock.recv(1024)
        data += part
        if b'\r\n' in part or not part:
            break
    return data.decode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(recv_all(s))

    s.sendall(f'USER {USER}\r\n'.encode())
    print(recv_all(s))

    s.sendall(f'PASS {PASS}\r\n'.encode())
    print(recv_all(s))

    s.sendall(b'STAT\r\n')
    response = recv_all(s)
    print("Odpowiedź STAT:", response)

    if response.startswith('+OK'):
        parts = response.strip().split()
        if len(parts) >= 2:
            count = parts[1]
            print(f"Liczba wiadomości: {count}")
        else:
            print("Nie udało się odczytać liczby wiadomości.")
    else:
        print("Błąd podczas pobierania danych.")

    s.sendall(b'QUIT\r\n')
    print(recv_all(s))
