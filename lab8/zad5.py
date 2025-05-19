import imaplib
import email

imap_server = "212.182.24.27"
email_user = "pasinf2017@infumcs.edu"
password = "P4SInf2017"

try:
    mail = imaplib.IMAP4(imap_server)
    mail.login(email_user, password)

    mail.select("INBOX")

    status, data = mail.search(None, "ALL")
    if status != "OK":
        print("Nie udało się pobrać wiadomości.")
        mail.logout()
        exit()

    message_ids = data[0].split()

    if not message_ids:
        print("Skrzynka jest pusta.")
        mail.logout()
        exit()

    print(f"\nZnaleziono {len(message_ids)} wiadomości:")
    for i, msg_id in enumerate(message_ids, 1):
        status, msg_data = mail.fetch(msg_id, "(BODY.PEEK[HEADER.FIELDS (Subject From)])")
        if status != "OK":
            continue
        msg = email.message_from_bytes(msg_data[0][1])
        subject = msg.get("Subject", "(brak tematu)")
        sender = msg.get("From", "(brak nadawcy)")
        print(f"{i}: Od: {sender}, Temat: {subject}")

    num_to_delete = int(input("\nPodaj numer wiadomości do usunięcia: "))
    if num_to_delete < 1 or num_to_delete > len(message_ids):
        print("Nieprawidłowy numer wiadomości.")
        mail.logout()
        exit()

    msg_id_to_delete = message_ids[num_to_delete - 1]

    mail.store(msg_id_to_delete, '+FLAGS', '\\Deleted')

    mail.expunge()

    print("Wiadomość została trwale usunięta.")

    mail.logout()

except imaplib.IMAP4.error as e:
    print("Błąd IMAP:", e)
except Exception as e:
    print("Wystąpił błąd:", e)
