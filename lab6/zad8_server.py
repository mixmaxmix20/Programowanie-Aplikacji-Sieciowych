import socket
import threading
from datetime import datetime
import base64
import email
import email.policy
import os


def log_email(sender, recipients, message):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    eml_filename = f"email_{timestamp}.eml"
    attachments_dir = f"attachments_{timestamp}"

    msg = email.message_from_string(message, policy=email.policy.default)

    os.makedirs(attachments_dir, exist_ok=True)

    with open(eml_filename, "w", encoding="utf-8") as f:
        f.write(message)

    print(f"\n--- Nowa wiadomość ({timestamp}) ---")
    print(f"Od: {sender}")
    print(f"Do: {', '.join(recipients)}")

    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue

        filename = part.get_filename()
        content_type = part.get_content_type()

        if filename:
            payload = part.get_payload(decode=True)
            attachment_path = os.path.join(attachments_dir, filename)

            try:
                with open(attachment_path, "wb") as f:
                    f.write(payload)
                print(f"Zapisano załącznik: {filename} ({content_type}, {len(payload)} bajtów)")
            except Exception as e:
                print(f"Błąd przy zapisie załącznika: {e}")


def handle_client(conn, addr):
    try:
        buffer = b""
        state = "EHLO"
        sender = ""
        recipients = []
        message = []

        conn.send(b"220 localhost ESMTP Test Server\r\n")

        while True:
            data = conn.recv(1024)
            if not data:
                break
            buffer += data

            while b"\r\n" in buffer:
                request, buffer = buffer.split(b"\r\n", 1)
                request_str = request.decode("utf-8", errors="ignore").strip()

                if state == "EHLO":
                    if request_str.upper().startswith("EHLO"):
                        conn.send(b"250-localhost\r\n250-8BITMIME\r\n250-SIZE 10485760\r\n250 OK\r\n")
                        state = "MAIL"
                    else:
                        conn.send(b"500 Syntax error\r\n")
                        return

                elif state == "MAIL":
                    if request_str.upper().startswith("MAIL FROM:"):
                        sender = request_str[10:].strip("<> ")
                        conn.send(b"250 OK\r\n")
                        state = "RCPT"
                    else:
                        conn.send(b"503 Bad sequence\r\n")
                        return

                elif state == "RCPT":
                    if request_str.upper().startswith("RCPT TO:"):
                        recipient = request_str[8:].strip("<> ")
                        recipients.append(recipient)
                        conn.send(b"250 OK\r\n")
                    elif request_str.upper() == "DATA":
                        conn.send(b"354 End data with <CR><LF>.<CR><LF>\r\n")
                        state = "DATA"
                    else:
                        conn.send(b"503 Bad sequence\r\n")
                        return

                elif state == "DATA":
                    while True:
                        if b"\r\n.\r\n" in buffer:
                            msg_part, buffer = buffer.split(b"\r\n.\r\n", 1)
                            message.append(msg_part)
                            break
                        else:
                            message.append(buffer)
                            buffer = b""
                            data = conn.recv(1024)
                            if not data:
                                break
                            buffer += data

                    full_message = b"".join(message).decode("utf-8", errors="ignore")
                    full_message = full_message.replace("\n..", "\n.")  # Usuwanie nadmiarowych kropek

                    log_email(sender, recipients, full_message)
                    conn.send(b"250 Message accepted\r\n")
                    state = "QUIT"

                elif state == "QUIT":
                    if request_str.upper() == "QUIT":
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