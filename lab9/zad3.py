import socket

host = "212.182.24.27"
port = 8080
path = "/image.jpg"

def get_range(start, end):
    request = f"""GET {path} HTTP/1.1\r
Host: {host}\r
User-Agent: MyClient/1.0\r
Range: bytes={start}-{end}\r
Connection: close\r
\r
"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request.encode())
        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk
    headers, body = response.split(b"\r\n\r\n", 1)
    return body

def get_content_length():
    request = f"""HEAD {path} HTTP/1.1\r
Host: {host}\r
User-Agent: MyClient/1.0\r
Connection: close\r
\r
"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request.encode())
        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk
    headers = response.decode()
    for line in headers.split("\r\n"):
        if line.lower().startswith("content-length:"):
            return int(line.split(":")[1].strip())
    return None

content_length = get_content_length()
if content_length is None:
    print("Nie udało się pobrać rozmiaru pliku.")
    exit()

part_size = content_length // 3
ranges = [
    (0, part_size - 1),
    (part_size, 2 * part_size - 1),
    (2 * part_size, content_length - 1)
]

image_data = b""
for start, end in ranges:
    print(f"Pobieranie bajtów {start}-{end}")
    image_data += get_range(start, end)

with open("obrazek.jpg", "wb") as f:
    f.write(image_data)

print("Obrazek został zapisany jako 'obrazek.jpg'")
