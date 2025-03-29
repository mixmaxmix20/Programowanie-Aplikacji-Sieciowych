import socket

HOST = '127.0.0.1'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
    udp_socket.bind((HOST, PORT))
    print(f"Serwer nasłuchuje na {HOST}:{PORT} (UDP)...")

    while True:
        data, client_addr = udp_socket.recvfrom(1024)
        hostname = data.decode().strip()
        print(f"Odebrano zapytanie od {client_addr} dla hosta: '{hostname}'")

        try:
            ip_address = socket.gethostbyname(hostname)
            response = f"Adres IP dla '{hostname}': {ip_address}"
        except socket.gaierror:
            response = f"Nie znaleziono adresu IP dla '{hostname}'"
        except Exception as e:
            response = f"Błąd: {str(e)}"

        udp_socket.sendto(response.encode(), client_addr)
        print(f"Wysłano odpowiedź do {client_addr}\n")