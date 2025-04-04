import socket

HOST = '127.0.0.1'
PORT = 2912


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("Połączono z serwerem. Rozpocznij zgadywanie!")

            while True:
                guess = input("Podaj liczbę: ")
                s.sendall(f"{guess}\n".encode())

                response = s.recv(1024).decode().strip()

                if not response:
                    print("Połączenie zamknięte przez serwer. Prawdopodobnie odgadnięto liczbę!")
                    break

                print("Odpowiedź serwera:", response)
                if "udało" in response.lower() or "gratulacje" in response.lower():
                    print("Udało się! Koniec gry.")
                    break

        except ConnectionResetError:
            print("Serwer zamknął połączenie. Odgadłeś liczbę!")
        except Exception as e:
            print("Wystąpił błąd:", e)


if __name__ == "__main__":
    main()