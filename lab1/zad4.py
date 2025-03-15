import ipaddress
import sys
import socket

def check_ip(ip_add):
    try:
        ipaddress.ip_address(ip_add)
        return True
    except ValueError:
        return False

ip = sys.argv[1]

if not check_ip(ip):
    print("Niepoprawny adres ip")
    sys.exit(1)
try:
    hostname, _, _ = socket.gethostbyaddr(ip)
    print(hostname)
except socket.herror:
    print("Nie znaleziono hostname")