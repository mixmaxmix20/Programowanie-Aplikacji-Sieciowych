import ipaddress

ip = input("Podaj adres ip: ")

try:
    ipaddress.ip_address(ip)
    print("Poprawny")
except ValueError:
    print("Niepoprawny")


