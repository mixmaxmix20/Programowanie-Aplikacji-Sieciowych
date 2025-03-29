import socket

HOST = '127.0.0.1'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
    udp_socket.bind((HOST, PORT))
    print(f"Serwer nasłuchuje na {HOST}:{PORT} (UDP)...")

    while True:
        data, client_addr = udp_socket.recvfrom(1024)

        try:
            message = data.decode().strip()
            parts = message.split()

            if len(parts) != 3:
                raise ValueError("Nieprawidłowy format. Wymagane: liczba operator liczba")

            num1 = float(parts[0])
            operator = parts[1]
            num2 = float(parts[2])

            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    raise ZeroDivisionError("Dzielenie przez zero")
                result = num1 / num2
            else:
                raise ValueError(f"Nieznany operator: {operator}")

            response = f"Wynik: {result:.2f}"

        except Exception as e:
            response = f"Błąd: {str(e)}"

        udp_socket.sendto(response.encode(), client_addr)
        print(f"Obsłużono klienta {client_addr}: {message} → {response}")