import socket

HOST = '127.0.0.1'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
    udp_socket.bind((HOST, PORT))
    print(f"Serwer nasłuchuje na {HOST}:{PORT} (UDP)")

    while True:
        data, client_addr = udp_socket.recvfrom(1024)
        print(f"Odebrano od {client_addr}: {data.decode()}")

        udp_socket.sendto(data, client_addr)
        print(f"Odesłano {len(data)} bajtów do {client_addr}")