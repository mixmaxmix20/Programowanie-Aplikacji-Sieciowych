import socket
import sys
from time import gmtime, strftime


def check_msg_syntax(txt):
    s = len(txt.split(";"))
    if s != 7:
        return "BAD_SYNTAX"
    else:
        tmp = txt.split(";")
        if tmp[0] == "zad13odp" and tmp[1] == "src" and tmp[3] == "dst" and tmp[5] == "data":
            try:
                src_port = int(tmp[2])
                dst_port = int(tmp[4])
                data = tmp[6]
            except:
                return "BAD_SYNTAX"
            if src_port == 2900 and dst_port == 35211 and data == "hello :)":
                return "TAK"
            else:
                return "NIE"
        else:
            return "BAD_SYNTAX"


HOST = '127.0.0.1'
PORT = 2909

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    server_socket.bind((HOST, PORT))
except socket.error as msg:
    print(f'Bind failed. Error Code: {msg[0]} Message: {msg[1]}')
    sys.exit()

print(f"[{strftime('%Y-%m-%d %H:%M:%S', gmtime())}] UDP Server is waiting for messages...")

try:
    while True:
        data, client_address = server_socket.recvfrom(1024)

        decoded_data = data.decode()
        timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print(f"[{timestamp}] Received {len(data)} bytes from {client_address}: {decoded_data}")

        response = check_msg_syntax(decoded_data)
        server_socket.sendto(response.encode(), client_address)
        print(f"[{timestamp}] Sent response to {client_address}: {response}")

except KeyboardInterrupt:
    print("\nShutting down server...")
finally:
    server_socket.close()