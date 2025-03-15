# Nawiązanie połączenia z serwerem
# • Język Python
#!/usr/bin/env python
import socket
if __name__ == '__main__':
    sockIPv4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockIPv4.settimeout(1)
    try:
        sockIPv4.sendto(b'', ('ntp.task.gda.pl', 13))
        data, addr = sockIPv4.recvfrom(1024)
        print("Data i czas:", data.decode('utf-8').strip())
    except socket.error as exc:
        print("Wyjatek socket.error : %s" % exc)
    sockIPv4.close()