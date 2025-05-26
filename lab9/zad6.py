import socket
import os

host = "212.182.24.27"
port = 8080
path = "/image.jpg"
metadata_file = "last_modified.txt"

def get_headers(extra_headers=""):
    request = f"""HEAD {path} HTTP/1.1\r
Host: {host}\r
User-Agent: MyClient/1.0\r
{extra_headers}Connection: close\r
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
    return response.decode()

def get_range(start, end):
    with open(metadata_file) as f:
        last_modified = f.read().strip() if os.path.exists(metadata_file) else None

    headers = f"Range: bytes={start}-{end}\r\n"
    if os.path.exists(metadata_file):
        headers += f"If-Modified-Since: {last_modified}\r\n"

    request = f"""GET {path} HTTP/1.1\r
Host: {host}\r
User-Agent: MyClient/1.0\r
{headers}Connection: close\r
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

    header_part, body = response.split(b"\r\n\r\n", 1)
    header_text = header_part.decode()
    if "304 Not Modified" in header_text:
        return None
    return body

def get_content_length_and_last_modified():
    headers = get_headers()
    content_length = None
    last_modified = None
    for line in headers.split("\r\n"):
        if line.lower().startswith("content-length:"):
            content_length = int(line.split(":")[1].strip())
        elif line.lower().startswith("last-modified:"):
            last_modified = line.split(":", 1)[1].strip()
    return content_length, last_modified

extra = ""
if os.path.exists(metadata_file):
    with open(metadata_file) as f:
        last_modified = f.read().strip()
        extra = f"If-Modified-Since: {last_modified}\r\n"

head_response = get_headers(extra)
if "304 Not Modified" in head_response:
    print("Obrazek nie został zmodyfikowany – pobieranie pominięte.")
    exit()

content_length, last_modified = get_content_length_and_last_modified()
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
    part = get_range(start, end)
    if part is None:
        print("Część pliku nie została zmodyfikowana – pomijam.")
        exit()
    image_data += part

with open("obrazek.jpg", "wb") as f:
    f.write(image_data)

if last_modified:
    with open(metadata_file, "w") as f:
        f.write(last_modified)

print("Obrazek został zapisany jako 'obrazek.jpg'")
