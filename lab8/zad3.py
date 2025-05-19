import imaplib

imap_server = "212.182.24.27"
email = "pasinf2017@infumcs.edu"
password = "P4SInf2017"

try:
    mail = imaplib.IMAP4(imap_server)

    mail.login(email, password)

    status, folders = mail.list()
    if status != "OK":
        print("Nie udało się pobrać listy folderów.")
        mail.logout()
        exit()

    total_messages = 0

    for folder in folders:
        parts = folder.decode().split(' "/" ')
        if len(parts) != 2:
            continue
        folder_name = parts[1].strip('"')

        status, _ = mail.select(f'"{folder_name}"', readonly=True)
        if status != "OK":
            print(f"Nie można uzyskać dostępu do folderu: {folder_name}")
            continue

        status, message_numbers = mail.search(None, "ALL")
        if status == "OK":
            message_ids = message_numbers[0].split()
            count = len(message_ids)
            total_messages += count
            print(f"{folder_name}: {count} wiadomości")
        else:
            print(f"Błąd przy odczycie wiadomości w folderze: {folder_name}")

    print(f"\nŁączna liczba wiadomości we wszystkich folderach: {total_messages}")

    mail.logout()

except imaplib.IMAP4.error as e:
    print("Błąd IMAP:", e)
except Exception as e:
    print("Wystąpił błąd:", e)
