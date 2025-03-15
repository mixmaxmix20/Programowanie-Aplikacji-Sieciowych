#!/usr/bin/env python
import socket
if __name__ == '__main__':
    message = input("Podaj wiadomosc: ")
    sockIPv4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockIPv4.settimeout(1)
    try:
        while True:
            sockIPv4.sendto(message.encode('utf-8'), ('127.0.0.1', 2901))
            data, _ = sockIPv4.recvfrom(1024)
            print(data.decode())
    except socket.error as exc:
        print("Wyjatek socket.error : %s" % exc)
    sockIPv4.close()