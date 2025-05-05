import socket
import os
import base64
import mimetypes


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


def przygotuj_wiadomosc(nadawca, odbiorcy, temat, tresc, nazwa_pliku, zawartosc_pliku, mime_type):
    granica = "=====Granica_MIME_123456789=="

    naglowki = [
        f"From: {nadawca}",
        f"To: {', '.join(odbiorcy)}",
        f"Subject: {temat}",
        "MIME-Version: 1.0",
        f"Content-Type: multipart/mixed; boundary=\"{granica}\"",
        "",
    ]

    czesc_tekstowa = [
        f"--{granica}",
        "Content-Type: text/plain; charset=utf-8",
        "Content-Transfer-Encoding: 8bit",
        "",
        tresc,
        ""
    ]

    zalacznik = [
        f"--{granica}",
        f"Content-Type: {mime_type}",
        "Content-Transfer-Encoding: base64",
        f"Content-Disposition: attachment; filename=\"{nazwa_pliku}\"",
        "",
        zawartosc_pliku,
        f"--{granica}--",
        ""
    ]

    linie = naglowki + czesc_tekstowa + zalacznik
    wiadomosc = "\r\n".join(linie)

    return "\r\n".join(
        ["." + linia if linia.startswith(".") else linia for linia in wiadomosc.split("\r\n")]) + "\r\n.\r\n"


def main():
    nadawca = input("Podaj adres nadawcy: ")
    odbiorcy = input("Podaj adres(y) odbiorców (oddzielone przecinkami): ").split(',')
    temat = input("Podaj temat wiadomości: ")
    tresc = input("Podaj treść wiadomości: ")
    sciezka_pliku = input("Podaj ścieżkę do pliku obrazu do załączenia: ")

    try:
        with open(sciezka_pliku, 'rb') as f:
            obraz_bytes = f.read()

        obraz_base64 = base64.b64encode(obraz_bytes).decode('utf-8')
        obraz_base64 = '\r\n'.join([obraz_base64[i:i + 76] for i in range(0, len(obraz_base64), 76)])

        nazwa_pliku = os.path.basename(sciezka_pliku)

        mime_type, _ = mimetypes.guess_type(sciezka_pliku)
        if not mime_type:
            mime_type = "application/octet-stream"

    except Exception as e:
        print(f"Błąd przy czytaniu pliku: {e}")
        return

    wiadomosc = przygotuj_wiadomosc(
        nadawca,
        [o.strip() for o in odbiorcy],
        temat,
        tresc,
        nazwa_pliku,
        obraz_base64,
        mime_type
    )

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 587))
        print("Odebrano:", odbierz_odpowiedz(s))

        s.sendall(b'EHLO localhost\r\n')
        print("EHLO:", odbierz_odpowiedz(s))

        s.sendall(f'MAIL FROM:<{nadawca}>\r\n'.encode())
        print("MAIL FROM:", odbierz_odpowiedz(s))

        for odbiorca in odbiorcy:
            s.sendall(f'RCPT TO:<{odbiorca.strip()}>\r\n'.encode())
            print(f"RCPT TO {odbiorca}:", odbierz_odpowiedz(s))

        s.sendall(b'DATA\r\n')
        print("DATA:", odbierz_odpowiedz(s))

        s.sendall(wiadomosc.encode('utf-8'))
        print("Wiadomość wysłana:", odbierz_odpowiedz(s))

        s.sendall(b'QUIT\r\n')
        print("QUIT:", odbierz_odpowiedz(s))


if __name__ == "__main__":
    main()