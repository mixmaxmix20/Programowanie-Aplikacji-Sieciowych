import socket
import time

HOST = '127.0.0.1'
UDP_BASE_PORT = 666
TCP_PORT = 2913
TIMEOUT = 0.5
PING_MESSAGE = b"PING"


def find_valid_udp_ports():
    valid_ports = []

    for port in range(UDP_BASE_PORT, 65536, 1000):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(TIMEOUT)
            try:
                s.sendto(PING_MESSAGE, (HOST, port))
                data, _ = s.recvfrom(1024)
                if data.strip() == b"PONG":
                    valid_ports.append(port)
                    print(f"Znaleziono port: {port}")
            except (socket.timeout, ConnectionResetError):
                continue
            except Exception as e:
                print(f"Błąd przy porcie {port}: {str(e)}")

    return sorted(valid_ports)


def perform_port_knocking(ports):
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            try:
                s.sendto(PING_MESSAGE, (HOST, port))
                print(f"Wysłano PING na port {port}")
            except Exception as e:
                print(f"Błąd przy port knocking {port}: {str(e)}")
        time.sleep(0.1)


def get_tcp_message():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, TCP_PORT))
            return s.recv(1024).decode()
        except Exception as e:
            return f"Błąd połączenia TCP: {str(e)}"


def main():
    print("Rozpoczynanie skanowania portów UDP...")
    valid_ports = find_valid_udp_ports()

    if not valid_ports:
        print("Nie znaleziono żadnych portów w sekwencji")
        return

    print(f"\nZnalezione porty: {valid_ports}")
    print("\nRozpoczynanie port knocking...")
    perform_port_knocking(valid_ports)

    print("\nPróba połączenia TCP...")
    print(get_tcp_message())


if __name__ == "__main__":
    main()