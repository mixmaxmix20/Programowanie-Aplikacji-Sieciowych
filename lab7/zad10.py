import socket

HOST = 'interia.pl'
PORT = 110
USER = 'pas2017@interia.pl'
PASS = 'P4SInf2017'

def recv_until_dot(sock):
    data = b''
    while True:
        chunk = sock.recv(1024)
        data += chunk
        if b'\r\n.\r\n' in data:
            break
    return data.decode()

def send_cmd(sock, cmd):
    sock.sendall(f"{cmd}\r\n".encode())
    return recv_until_dot(sock)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(recv_until_dot(s))

    print(send_cmd(s, f"USER {USER}"))
    print(send_cmd(s, f"PASS {PASS}"))

    stat = send_cmd(s, "STAT")
    print("STAT:", stat.strip())

    try:
        count = int(stat.strip().split()[1])
    except:
        print("Nie udało się odczytać liczby wiadomości.")
        count = 0

    for i in range(1, count + 1):
        print(f"\n===== WIADOMOŚĆ {i} =====")
        message = send_cmd(s, f"RETR {i}")
        print(message)

    print(send_cmd(s, "QUIT"))
