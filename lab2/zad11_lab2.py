import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 2908
MESSAGE = "Hello server"


def format_message(msg, length=20):
    if len(msg) > length:
        return msg[:length]
    return msg.ljust(length)


if __name__ == '__main__':
    sockIPv4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockIPv4.settimeout(1)

    try:
        sockIPv4.connect((SERVER_IP, SERVER_PORT))
        formatted_message = format_message(MESSAGE)
        print(f"Wysłana wiadomość: '{formatted_message}'")

        sockIPv4.sendall(formatted_message.encode('utf-8'))

        data = sockIPv4.recv(20).decode('utf-8').strip()
        print(f"Otrzymana odpowiedź: '{data}'")

    except socket.error as exc:
        print(f"Błąd socket.error: {exc}")

    finally:
        sockIPv4.close()
