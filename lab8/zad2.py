import imaplib

imap_server = "212.182.24.27"
email = "pasinf2017@infumcs.edu"
password = "P4SInf2017"

try:
    mail = imaplib.IMAP4(imap_server)

    mail.login(email, password)

    mail.select("INBOX")

    status, messages = mail.search(None, "ALL")

    if status == "OK":
        message_ids = messages[0].split()
        print(f"Liczba wiadomości w skrzynce Inbox: {len(message_ids)}")
    else:
        print("Nie udało się pobrać wiadomości.")

    mail.logout()

except imaplib.IMAP4.error as e:
    print("Błąd IMAP:", e)
except Exception as e:
    print("Nieoczekiwany błąd:", e)
