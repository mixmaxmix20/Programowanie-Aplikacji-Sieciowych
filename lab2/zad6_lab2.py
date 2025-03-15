#!/usr/bin/env python
import socket
if __name__ == '__main__':
    number1 = input("Podaj 1 liczbe: ")
    operator = input("Podaj operator: ")
    number2 = input("Podaj 2 liczbe: ")
    sockIPv4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockIPv4.settimeout(1)
    try:
        sockIPv4.sendto(number1.encode(), ('127.0.0.1', 2902))
        sockIPv4.sendto(operator.encode(), ('127.0.0.1', 2902))
        sockIPv4.sendto(number2.encode(), ('127.0.0.1', 2902))
        data, _ = sockIPv4.recvfrom(4096)
        print(data.decode())
    except socket.error as exc:
        print("Wyjatek socket.error : %s" % exc)
    sockIPv4.close()