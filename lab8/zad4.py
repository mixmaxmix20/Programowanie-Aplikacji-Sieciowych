import imaplib
import email

imap_server = "212.182.24.27"
email_user = "pasinf2017@infumcs.edu"
password = "P4SInf2017"

try:
    mail = imaplib.IMAP4(imap_server)
    mail.login(email_user, password)

    mail.select("INBOX")

    status, messages = mail.search(None, 'UNSEEN')

    if status != "OK":
        print("Nie udało się pobrać wiadomości.")
        mail.logout()
        exit()

    message_ids = messages[0].split()

    if not message_ids:
        print("Brak nieprzeczytanych wiadomości.")
    else:
        print(f"Znaleziono {len(message_ids)} nieprzeczytanych wiadomości:\n")

        for msg_id in message_ids:
            status, msg_data = mail.fetch(msg_id, "(RFC822)")
            if status != "OK":
                print(f"Nie udało się pobrać wiadomości {msg_id.decode()}.")
                continue

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject = msg.get("Subject", "(brak tematu)")
            from_ = msg.get("From", "(brak nadawcy)")
            print(f"Od: {from_}\nTemat: {subject}")

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain" and not part.get("Content-Disposition"):
                        print("Treść:")
                        print(part.get_payload(decode=True).decode(part.get_content_charset("utf-8"), errors="replace"))
                        break
            else:
                print("Treść:")
                print(msg.get_payload(decode=True).decode(msg.get_content_charset("utf-8"), errors="replace"))

            print("-" * 60)

            mail.store(msg_id, '+FLAGS', '\\Seen')

    mail.logout()

except imaplib.IMAP4.error as e:
    print("Błąd IMAP:", e)
except Exception as e:
    print("Wystąpił błąd:", e)
