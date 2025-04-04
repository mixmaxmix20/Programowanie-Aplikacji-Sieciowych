import socket
import threading

TCP_PORT = 12345
UDP_PORT = 12345
BUFFER_SIZE = 1024

def handle_tcp(client_socket):
    try:
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            client_socket.send(data)
    finally:
        client_socket.close()

def tcp_server():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', TCP_PORT))
            s.listen(5)
            print("Serwer TCP nasłuchuje...")
            while True:
                client, _ = s.accept()
                threading.Thread(target=handle_tcp, args=(client,)).start()
    except Exception as e:
        print(f"Błąd TCP: {e}")

def udp_server():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', UDP_PORT))
            print("Serwer UDP nasłuchuje...")
            while True:
                data, addr = s.recvfrom(BUFFER_SIZE)
                s.sendto(data, addr)
    except Exception as e:
        print(f"Błąd UDP: {e}")

if __name__ == "__main__":
    threading.Thread(target=tcp_server, daemon=True).start()
    threading.Thread(target=udp_server, daemon=True).start()
    input("Naciśnij Enter, aby zatrzymać serwer...\n")

# UDP będzie miał krótszy czas przesyłu, ponieważ:
# Nie nawiązuje połączenia
# Nie potwierdza odbioru
# Nie ma kontroli przeplywu

# TCP musi potwierdzać każdy pakiet i odtwarzać połączenie co generuje dodatkowy ruch sieciowy
# UDP wysyła pakiety bez gwarancji dostarczenia

# TCP
# Zalety:
# Gwarancja dostarczenia pakietow
# Zachowuje kolejnosc pakietow
# Wady:
# Wolniejszy

# UDP
# Zalety:
# Szybszy
# Nie blokuje przy utracie pakietow
# Wady:
# Brak kontorli przeplywu