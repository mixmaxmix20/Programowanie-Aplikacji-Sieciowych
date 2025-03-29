import socket
import select
from time import gmtime, strftime

HOST = '127.0.0.1'
PORT = 2900
MAX_MSG_LENGTH = 30

connected_clients_sockets = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

connected_clients_sockets.append(server_socket)

print("[%s] TCP ECHO Server is waiting for incoming connections on port %s ..." % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), PORT))

def reliable_send(sock, data):
    total_sent = 0
    while total_sent < len(data):
        sent = sock.send(data[total_sent:])
        if sent == 0:
            raise RuntimeError("Socket connection broken during send")
        total_sent += sent

def reliable_recv(sock, length):
    chunks = []
    total_received = 0
    while total_received < length:
        chunk = sock.recv(min(length - total_received, 4096))
        if chunk == b'':
            raise RuntimeError("Socket connection broken during recv")
        chunks.append(chunk)
        total_received += len(chunk)
    return b''.join(chunks)

while True:
    read_sockets, _, _ = select.select(connected_clients_sockets, [], [])

    for sock in read_sockets:
        if sock == server_socket:
            sockfd, client_address = server_socket.accept()
            connected_clients_sockets.append(sockfd)
            print("[%s] Client %s connected ..." % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), client_address))
        else:
            try:
                data = reliable_recv(sock, MAX_MSG_LENGTH)
                if data:
                    reliable_send(sock, data)
                    print("[%s] Sent to %s: [%s]" % (
                        strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                        sock.getpeername(),
                        data
                    ))
            except Exception as e:
                print("[%s] Client %s disconnected: %s" % (
                    strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                    sock.getpeername(),
                    str(e)
                ))
                sock.close()
                connected_clients_sockets.remove(sock)

server_socket.close()
