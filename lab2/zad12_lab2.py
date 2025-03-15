import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 2908
MESSAGE = "Hello server this is a very long text that should be divided into chunks"


def format_message(msg, length=20):
    return msg[:length].ljust(length) if len(msg) > length else msg.ljust(length)


def receive_all(sock, length):
    data = bytearray()
    while len(data) < length:
        remaining = length - len(data)
        chunk = sock.recv(remaining)
        if not chunk:
            raise socket.error("Połączenie zamknięte przed odebraniem wszystkich danych")
        data.extend(chunk)
    return data


if __name__ == '__main__':
    sockIPv4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockIPv4.settimeout(3)

    try:
        sockIPv4.connect((SERVER_IP, SERVER_PORT))
        formatted_message = format_message(MESSAGE)
        print(f"Wysłana wiadomość: '{formatted_message}'")

        sockIPv4.sendall(formatted_message.encode('utf-8'))

        received_data = receive_all(sockIPv4, 20)
        response = received_data.decode('utf-8').strip()
        print(f"Otrzymana odpowiedź: '{response}'")

    except socket.error as exc:
        print(f"Błąd socket.error: {exc}")

    finally:
        sockIPv4.close()