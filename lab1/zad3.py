def check_ip(ip_add):
    parts = ip_add.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False

        temp = int(part)

        if temp < 0 or temp > 255:
            return False
    return True

ip = input("Podaj adres ip: ")
if check_ip(ip):
    print("Poprawny")
else:
    print("Niepoprawny")


