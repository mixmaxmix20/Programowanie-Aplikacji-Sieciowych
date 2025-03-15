#!/usr/bin/env python
import socket
if __name__ == '__main__':
    message = input("Podaj wiadomosc: ")
    sockIPv4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockIPv4.settimeout(5)
    try:
        sockIPv4.connect(('127.0.0.1', 2900))
        while True:
            sockIPv4.sendall(message.encode('utf-8'))
            data = sockIPv4.recv(1024).decode('utf-8')
            print(data)
    except socket.error as exc:
        print("Wyjatek socket.error : %s" % exc)
    sockIPv4.close()