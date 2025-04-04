import socket
import threading
from time import time

UDP_SEQUENCE = [1666, 2666, 3666]
TCP_PORT = 2913
ALLOWED_TIMEOUT = 10
PING_MESSAGE = b"PING"
PONG_MESSAGE = b"PONG"

client_steps = {}
allowed_ips = {}
lock = threading.Lock()


def handle_udp_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", port))
        print(f"[UDP] Nasłuchiwanie na porcie {port}")

        while True:
            try:
                data, addr = s.recvfrom(1024)
                ip = addr[0]

                if data.strip() == PING_MESSAGE:
                    with lock:
                        current_step = client_steps.get(ip, 0)

                        if port == UDP_SEQUENCE[current_step]:
                            current_step += 1
                            try:
                                s.sendto(PONG_MESSAGE, addr)
                            except Exception as send_error:
                                print(f"Błąd wysyłania PONG do {ip}: {send_error}")
                                continue

                            print(f"[UDP] {ip}: poprawny krok {current_step}/{len(UDP_SEQUENCE)}")

                            if current_step == len(UDP_SEQUENCE):
                                allowed_ips[ip] = time() + ALLOWED_TIMEOUT
                                print(f"[!] {ip} odblokował port TCP!")
                                current_step = 0

                            client_steps[ip] = current_step
                        else:
                            if ip in client_steps:
                                del client_steps[ip]
                            try:
                                s.sendto(PONG_MESSAGE, addr)
                            except Exception as send_error:
                                print(f"Błąd wysyłania PONG (zła sekwencja) do {ip}: {send_error}")

            except ConnectionResetError as cre:
                print(f"Błąd połączenia z {addr[0]}: {cre}")
                continue
            except OSError as ose:
                print(f"Błąd systemowy na porcie {port}: {ose}")
                continue
            except Exception as e:
                print(f"Niespodziewany błąd: {e}")
                continue

def cleanup_expired_ips():
    while True:
        with lock:
            now = time()
            expired = [ip for ip, expiry in allowed_ips.items() if expiry < now]
            for ip in expired:
                del allowed_ips[ip]
        threading.Event().wait(1)


def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", TCP_PORT))
        s.listen()
        print(f"[TCP] Serwer nasłuchuje na porcie {TCP_PORT}")

        while True:
            conn, addr = s.accept()
            ip = addr[0]
            with lock:
                if ip in allowed_ips:
                    conn.sendall(b"Congratulations! You found the hidden.\n")
                    del allowed_ips[ip]
                    print(f"[TCP] {ip} odebrał nagrodę")
                else:
                    conn.sendall(b"Access denied. Complete port knocking first.\n")
            conn.close()


if __name__ == "__main__":
    for port in UDP_SEQUENCE:
        threading.Thread(target=handle_udp_port, args=(port,), daemon=True).start()

    threading.Thread(target=cleanup_expired_ips, daemon=True).start()

    tcp_server()