import socket
import threading
from datetime import datetime


def log_email(sender, recipients, message):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"email_{timestamp}.eml"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"From: {sender}\n")
        f.write(f"To: {', '.join(recipients)}\n")
        f.write(message)

    print(f"\n--- Nowa wiadomość ({timestamp}) ---")
    print(f"Od: {sender}")
    print(f"Do: {recipients}")
    print("Treść:")
    print(message)
    print(f"Zapisano jako: {filename}\n")


def handle_client(conn, addr):
    try:
        buffer = b""
        state = "EHLO"
        sender = ""
        recipients = []

        conn.send(b"220 localhost ESMTP Test Server\r\n")

        while True:
            data = conn.recv(1024)
            if not data:
                break
            buffer += data

            while b"\r\n" in buffer:
                request, buffer = buffer.split(b"\r\n", 1)
                request = request.decode("utf-8").strip()

                if state == "EHLO":
                    if request.upper().startswith("EHLO"):
                        conn.send(b"250-localhost\r\n250-8BITMIME\r\n250-SIZE 10485760\r\n250 OK\r\n")
                        state = "MAIL"
                    else:
                        conn.send(b"500 Syntax error\r\n")
                        return

                elif state == "MAIL":
                    if request.upper().startswith("MAIL FROM:"):
                        sender = request[10:].strip("<> ")
                        conn.send(b"250 OK\r\n")
                        state = "RCPT"
                    else:
                        conn.send(b"503 Bad sequence\r\n")
                        return

                elif state == "RCPT":
                    if request.upper().startswith("RCPT TO:"):
                        recipient = request[8:].strip("<> ")
                        recipients.append(recipient)
                        conn.send(b"250 OK\r\n")
                    elif request.upper() == "DATA":
                        conn.send(b"354 End data with <CR><LF>.<CR><LF>\r\n")
                        state = "DATA"
                    else:
                        conn.send(b"503 Bad sequence\r\n")
                        return

                elif state == "DATA":
                    message = []
                    while True:
                        if b"\r\n.\r\n" in buffer:
                            msg_part, buffer = buffer.split(b"\r\n.\r\n", 1)
                            message.append(msg_part.decode("utf-8"))
                            break
                        else:
                            message.append(buffer.decode("utf-8"))
                            buffer = b""
                            data = conn.recv(1024)
                            if not data:
                                break
                            buffer += data

                    full_message = "\n".join(message).replace("\n..", "\n.")
                    log_email(sender, recipients, full_message)
                    conn.send(b"250 Message accepted\r\n")
                    state = "QUIT"

                elif state == "QUIT":
                    if request.upper() == "QUIT":
                        conn.send(b"221 Bye\r\n")
                        return
                    else:
                        conn.send(b"503 Bad sequence\r\n")
                        return

    except Exception as e:
        print(f"Błąd połączenia: {e}")
    finally:
        conn.close()


def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", 587))
        s.listen(5)
        print("Serwer testowy ESMTP nasłuchuje na porcie 587...")

        while True:
            conn, addr = s.accept()
            print(f"\nNowe połączenie od: {addr[0]}:{addr[1]}")
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()


if __name__ == "__main__":
    run_server()