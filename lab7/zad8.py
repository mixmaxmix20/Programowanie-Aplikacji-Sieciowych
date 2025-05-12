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
        if b'\r\n.\r\n' in data or not part:
            break
    return data.decode()


def send_cmd(sock, cmd):
    sock.sendall(f"{cmd}\r\n".encode())
    return recv_all(sock)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(recv_all(s))

    print(send_cmd(s, f"USER {USER}"))
    print(send_cmd(s, f"PASS {PASS}"))

    response = send_cmd(s, "LIST")
    print("Rozmiary wiadomości (LIST):")

    lines = response.strip().split("\r\n")
    if lines[0].startswith("+OK"):
        for line in lines[1:]:
            if line == '.':
                break
            num, size = line.split()
            print(f"Wiadomość {num} zajmuje {size} bajtów")
    else:
        print("Błąd pobierania listy wiadomości")

    print(send_cmd(s, "QUIT"))
