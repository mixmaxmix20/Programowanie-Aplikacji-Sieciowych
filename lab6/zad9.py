import socket


def odbierz_odpowiedz(sock):
    dane = b''
    while True:
        czesc = sock.recv(1024)
        if not czesc:
            break
        dane += czesc
        if dane.endswith(b'\r\n'):
            break
    return dane.decode('utf-8', errors='ignore')


def przygotuj_wiadomosc_html(nadawca, odbiorcy, temat, tresc_html):
    headers = [
        f"From: {nadawca}",
        f"To: {', '.join(odbiorcy)}",
        f"Subject: {temat}",
        "MIME-Version: 1.0",
        "Content-Type: text/html; charset=UTF-8",
        "Content-Transfer-Encoding: 8bit",
        "",
    ]

    body = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        f"<title>{temat}</title>",
        "<meta charset='UTF-8'>",
        "</head>",
        "<body>",
        tresc_html,
        "</body>",
        "</html>"
    ]

    wiadomosc = "\r\n".join(headers + body)

    return "\r\n".join(
        ["." + linia if linia.startswith(".") else linia for linia in wiadomosc.split("\r\n")]) + "\r\n.\r\n"


def main():
    nadawca = input("Podaj adres nadawcy: ")
    odbiorcy = input("Podaj adres(y) odbiorców (oddzielone przecinkami): ").split(',')
    temat = input("Podaj temat wiadomości: ")

    print("Podaj treść HTML (zakończ pustą linią):")
    tresc_html = []
    while True:
        linia = input()
        if linia == "":
            break
        tresc_html.append(linia)

    tresc_html = "\n".join(tresc_html)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 587))
        print("Połączenie:", odbierz_odpowiedz(s))

        s.sendall(b'EHLO localhost\r\n')
        print("EHLO:", odbierz_odpowiedz(s))

        s.sendall(f'MAIL FROM:<{nadawca}>\r\n'.encode())
        print("MAIL FROM:", odbierz_odpowiedz(s))

        for odbiorca in odbiorcy:
            s.sendall(f'RCPT TO:<{odbiorca.strip()}>\r\n'.encode())
            print(f"RCPT TO {odbiorca}:", odbierz_odpowiedz(s))

        s.sendall(b'DATA\r\n')
        print("DATA:", odbierz_odpowiedz(s))

        wiadomosc = przygotuj_wiadomosc_html(
            nadawca,
            [o.strip() for o in odbiorcy],
            temat,
            tresc_html
        )
        s.sendall(wiadomosc.encode('utf-8'))
        print("Wiadomość wysłana:", odbierz_odpowiedz(s))

        s.sendall(b'QUIT\r\n')
        print("QUIT:", odbierz_odpowiedz(s))


if __name__ == "__main__":
    main()