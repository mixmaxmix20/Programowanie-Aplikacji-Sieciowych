import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 587))
print(s.recv(1024).decode())  # Powinno wyświetlić "220 ... ESMTP"
s.close()