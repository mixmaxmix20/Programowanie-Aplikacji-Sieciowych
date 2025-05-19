import socket
import threading

HOST = '127.0.0.1'
PORT = 8143

MESSAGES = {
    "1": {
        "flags": [],
        "body": "From: pasinf2017@infumcs.edu\r\nSubject: Test 1\r\n\r\nThis is a test message 1."
    },
    "2": {
        "flags": ["\\Seen"],
        "body": "From: pasinf2017@infumcs.edu\r\nSubject: Test 2\r\n\r\nThis is a test message 2."
    }
}

def handle_client(conn, addr):
    conn.send(b'* OK IMAP4rev1 Service Ready\r\n')

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            print(f"Odebrano od klienta: {data.strip()}")

            parts = data.strip().split()
            if not parts:
                continue

            tag = parts[0]
            cmd = parts[1].upper() if len(parts) > 1 else ""

            if cmd == "LOGIN":
                conn.send(f'{tag} OK LOGIN completed\r\n'.encode())

            elif cmd == "SELECT":
                conn.send(f'* {len(MESSAGES)} EXISTS\r\n'.encode())
                conn.send(f'{tag} OK [READ-WRITE] SELECT completed\r\n'.encode())

            elif cmd == "SEARCH":
                msg_ids = " ".join(MESSAGES.keys())
                conn.send(f'* SEARCH {msg_ids}\r\n'.encode())
                conn.send(f'{tag} OK SEARCH completed\r\n'.encode())

            elif cmd == "FETCH":
                if len(parts) >= 4 and parts[3] == "(RFC822)":
                    msg_id = parts[2]
                    if msg_id in MESSAGES:
                        body = MESSAGES[msg_id]["body"]
                        response = f'* {msg_id} FETCH (RFC822 {{{len(body)}}}\r\n{body})\r\n'
                        conn.send(response.encode())
                        conn.send(f'{tag} OK FETCH completed\r\n'.encode())
                    else:
                        conn.send(f'{tag} NO Message not found\r\n'.encode())
                else:
                    conn.send(f'{tag} BAD FETCH format not supported\r\n'.encode())

            elif cmd == "STORE":
                if len(parts) >= 5:
                    msg_id = parts[2]
                    flags = parts[4].strip('()')
                    if msg_id in MESSAGES:
                        MESSAGES[msg_id]["flags"] = flags.split()
                        conn.send(f'* {msg_id} FETCH (FLAGS ({" ".join(MESSAGES[msg_id]["flags"])}))\r\n'.encode())
                        conn.send(f'{tag} OK STORE completed\r\n'.encode())
                    else:
                        conn.send(f'{tag} NO Message not found\r\n'.encode())
                else:
                    conn.send(f'{tag} BAD STORE format error\r\n'.encode())

            elif cmd == "EXPUNGE":
                to_delete = [k for k, v in MESSAGES.items() if "\\Deleted" in v["flags"]]
                for msg_id in to_delete:
                    conn.send(f'* {msg_id} EXPUNGE\r\n'.encode())
                    del MESSAGES[msg_id]
                conn.send(f'{tag} OK EXPUNGE completed\r\n'.encode())

            elif cmd == "LOGOUT":
                conn.send(b'* BYE IMAP4rev1 Server logging out\r\n')
                conn.send(f'{tag} OK LOGOUT completed\r\n'.encode())
                break

            else:
                conn.send(f'{tag} BAD Command "{cmd}" not implemented\r\n'.encode())

    finally:
        conn.close()
        print(f"Połączenie z {addr} zakończone.")

def start_server():
    print(f"Serwer IMAP nasłuchuje na {HOST}:{PORT}")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\nSerwer został zatrzymany.")

if __name__ == "__main__":
    start_server()
