import sys
import socket

host = sys.argv[1]
port = int(sys.argv[2])

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("Połaczenie nawiazane pomyslnie!")

except OverflowError:
    print("Blad: Port poza zakresem")

except socket.gaierror:
    print("Blad: Bledny adres ip")