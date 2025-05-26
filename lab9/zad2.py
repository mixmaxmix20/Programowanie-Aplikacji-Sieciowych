import socket

host = "httpbin.org"
port = 80
path = "/image/png"

http_request = f"""GET {path} HTTP/1.1\r
Host: {host}\r
User-Agent: MyClient/1.0\r
Connection: close\r
\r
"""

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(http_request.encode())

    response = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        response += chunk

header_data, image_data = response.split(b"\r\n\r\n", 1)

with open("obrazek.png", "wb") as f:
    f.write(image_data)

print("Obrazek zapisany jako 'obrazek.png'")
