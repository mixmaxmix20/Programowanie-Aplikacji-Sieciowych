import socket

HOST = '127.0.0.1'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
    udp_socket.bind((HOST, PORT))
    print(f"Serwer nasłuchuje na {HOST}:{PORT} (UDP)...")

    while True:
        data, client_addr = udp_socket.recvfrom(1024)
        ip_address = data.decode().strip()
        print(f"Odebrano zapytanie od {client_addr} dla IP: {ip_address}")

        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
            response = f"Nazwa hosta dla {ip_address}: {hostname}"
        except socket.herror:
            response = f"Nie znaleziono hostname dla {ip_address}"
        except Exception as e:
            response = f"Błąd: {str(e)}"

        udp_socket.sendto(response.encode(), client_addr)
        print(f"Wysłano odpowiedź do {client_addr}")