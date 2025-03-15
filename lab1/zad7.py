import socket
import sys
import ipaddress

def check_ip(ip_add):
    try:
        ipaddress.ip_address(ip_add)
        return True
    except ValueError:
        return False

def skanuj_port(host, port, timeout=0.1):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        wynik = s.connect_ex((host, port))
        return wynik == 0


host = sys.argv[1]
if not check_ip(host):
    try:
        host = socket.gethostbyname(host)
    except socket.gaierror:
        print("Błąd: Niepoprawny adres lub nazwa hosta")
        sys.exit(1)

print(f"Skanuje {host}...", flush=True)
print("Otwarte porty:", flush=True)
for port in range(1, 1025):
    if skanuj_port(host, port):
        print(port, flush=True)