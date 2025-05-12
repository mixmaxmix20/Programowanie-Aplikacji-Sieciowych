import poplib
import getpass


def get_largest_message_content():
    server = 'interia.pl'
    username = 'pas2017@interia.pl'
    password = 'P4SInf2017'
    port = 110

    client = None
    try:
        client = poplib.POP3_SSL(server, port)

        client.user(username)
        client.pass_(password)
        print("Połączono pomyślnie!")

        _, msg_list, _ = client.list()

        if not msg_list:
            print("Skrzynka jest pusta.")
            return

        max_size = 0
        max_msg_num = 0

        for msg in msg_list:
            parts = msg.decode().split()
            if len(parts) >= 2:
                msg_num = int(parts[0])
                size = int(parts[1])

                if size > max_size:
                    max_size = size
                    max_msg_num = msg_num

        if max_msg_num > 0:
            print(f"\nPobieranie wiadomości nr {max_msg_num} ({max_size} bajtów)...")
            _, lines, _ = client.retr(max_msg_num)

            content = b'\n'.join(lines).decode(errors='replace')
            print("\n" + "=" * 50)
            print(f"Treść wiadomości:")
            print(content)
            print("=" * 50)

        else:
            print("Nie znaleziono wiadomości.")

    except poplib.error_proto as e:
        print(f"Błąd protokołu: {e}")
    except Exception as e:
        print(f"Błąd: {e}")
    finally:
        if client:
            client.quit()


if __name__ == "__main__":
    get_largest_message_content()