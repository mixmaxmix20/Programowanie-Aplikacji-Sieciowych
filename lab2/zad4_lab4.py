#!/usr/bin/env python
import socket
if __name__ == '__main__':
    sockIPv4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockIPv4.settimeout(1)
    try:
        sockIPv4.sendto('hello'.encode('utf-8'), ('127.0.0.1', 2901))
        data, _ = sockIPv4.recvfrom(1024)
        print(data.decode())
    except socket.error as exc:
        print("Wyjatek socket.error : %s" % exc)
    sockIPv4.close()