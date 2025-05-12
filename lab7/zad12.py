import socket
import threading

messages = [
    "From: test1@example.com\r\nSubject: Hello 1\r\n\r\nThis is the first test email.\r\n",
    "From: test2@example.com\r\nSubject: Hello 2\r\n\r\nThis is the second test email.\r\n",
    "From: test3@example.com\r\nSubject: Hello 3\r\n\r\nThis is the third test email.\r\n"
]

USERNAME = "user"
PASSWORD = "pass"

def handle_client(conn, addr):
    print(f"[+] Połączono z {addr}")
    conn.sendall(b"+OK POP3 server ready\r\n")

    authed = False
    while True:
        data = conn.recv(1024).decode().strip()
        if not data:
            break

        print(f"[{addr}] > {data}")
        cmd_parts = data.split()
        command = cmd_parts[0].upper()

        if command == "USER":
            if cmd_parts[1] == USERNAME:
                conn.sendall(b"+OK user accepted\r\n")
            else:
                conn.sendall(b"-ERR invalid user\r\n")

        elif command == "PASS":
            if cmd_parts[1] == PASSWORD:
                authed = True
                conn.sendall(b"+OK password accepted\r\n")
            else:
                conn.sendall(b"-ERR invalid password\r\n")

        elif not authed:
            conn.sendall(b"-ERR not authenticated\r\n")

        elif command == "STAT":
            count = len(messages)
            total_size = sum(len(m.encode()) for m in messages)
            conn.sendall(f"+OK {count} {total_size}\r\n".encode())

        elif command == "LIST":
            response = f"+OK {len(messages)} messages:\r\n"
            for i, msg in enumerate(messages, 1):
                response += f"{i} {len(msg.encode())}\r\n"
            response += ".\r\n"
            conn.sendall(response.encode())

        elif command == "RETR":
            try:
                index = int(cmd_parts[1]) - 1
                if 0 <= index < len(messages):
                    msg = messages[index]
                    response = f"+OK {len(msg.encode())} octets\r\n{msg}\r\n.\r\n"
                    conn.sendall(response.encode())
                else:
                    conn.sendall(b"-ERR no such message\r\n")
            except:
                conn.sendall(b"-ERR invalid message number\r\n")

        elif command == "QUIT":
            conn.sendall(b"+OK bye\r\n")
            break

        else:
            conn.sendall(b"-ERR command not implemented\r\n")

    conn.close()
    print(f"[-] Rozłączono z {addr}")

def start_server(host='127.0.0.1', port=11000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[START] Serwer POP3 działa na {host}:{port}")

    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    except KeyboardInterrupt:
        print("\n[STOP] Serwer zatrzymany")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
