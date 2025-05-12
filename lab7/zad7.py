import poplib


def get_total_mailbox_size(server, port, use_ssl, username, password):
    client = None
    try:
        if use_ssl:
            client = poplib.POP3_SSL(server, port)
        else:
            client = poplib.POP3(server, port)

        client.user(username)
        client.pass_(password)

        _, msg_list, _ = client.list()

        total_size = 0
        for msg in msg_list:
            parts = msg.decode().split()
            if len(parts) >= 2:
                total_size += int(parts[1])

        return total_size

    except Exception as e:
        print(f"Błąd: {e}")
        return None

    finally:
        if client:
            client.quit()


SERVER = "interia.pl"
PORT = 110
USE_SSL = True
USERNAME = "pas2017@interia.pl"
PASSWORD = "P4SInf2017"

total_bytes = get_total_mailbox_size(SERVER, PORT, USE_SSL, USERNAME, PASSWORD)
if total_bytes is not None:
    print(f"Łączny rozmiar wiadomości: {total_bytes} bajtów")