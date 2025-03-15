import sys
import socket

hostname = sys.argv[1]

try:
    ip = socket.gethostbyname(hostname)
    print(ip)
except socket.herror:
    print("Nie znaleziono ip")