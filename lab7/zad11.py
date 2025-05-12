import poplib
import email
import os
from email import policy
from email.parser import BytesParser
from email.header import decode_header
import getpass


def save_attachments_with_filenames():
    server = 'interia.pl'
    username = 'pas2017@interia.pl'
    password = 'P4SInf2017'
    port = 110

    client = None
    try:
        client = poplib.POP3_SSL(server, port)
        print("Połączono z serwerem!")

        client.user(username)
        client.pass_(password)
        print("Zalogowano pomyślnie.")

        _, msg_count, _ = client.stat()
        print(f"Liczba wiadomości w skrzynce: {msg_count}")

        for msg_num in range(1, msg_count + 1):
            _, lines, _ = client.retr(msg_num)
            msg_bytes = b'\r\n'.join(lines)

            msg = BytesParser(policy=policy.default).parsebytes(msg_bytes)

            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue

                if part.get("Content-Disposition") is None:
                    continue

                filename = part.get_filename()
                if filename:
                    decoded_filename = decode_header(filename)[0][0]
                    if isinstance(decoded_filename, bytes):
                        filename = decoded_filename.decode('utf-8', errors='replace')
                    else:
                        filename = str(decoded_filename)

                    if part.get_content_type().startswith('image/'):
                        file_data = part.get_payload(decode=True)

                        with open(filename, 'wb') as f:
                            f.write(file_data)
                        print(f"Zapisano obraz: {filename}")
                        return

            print(f"Brak obrazów w wiadomości {msg_num}")

        print("Nie znaleziono żadnych obrazów w skrzynce.")

    except poplib.error_proto as e:
        print(f"Błąd protokołu: {e}")
    except Exception as e:
        print(f"Błąd: {e}")
    finally:
        if client:
            client.quit()


if __name__ == "__main__":
    save_attachments_with_filenames()