import socket
import os
import datetime
import email.utils

HOST = '127.0.0.1'
PORT = 8080

def format_http_date(timestamp):
    return email.utils.formatdate(timestamp, usegmt=True)

def parse_http_date(date_str):
    try:
        return datetime.datetime(*email.utils.parsedate(date_str)[:6])
    except Exception:
        return None

def handle_client(conn):
    request = conn.recv(4096).decode('utf-8')
    if not request:
        conn.close()
        return

    lines = request.split('\r\n')
    request_line = lines[0]
    headers = {}

    for line in lines[1:]:
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key.lower()] = value

    method, path, _ = request_line.split()

    if method != 'GET':
        conn.sendall(b"HTTP/1.1 405 Method Not Allowed\r\n\r\n")
        conn.close()
        return

    file_path = path.lstrip('/')
    if file_path == '':
        file_path = 'index.html'

    if not os.path.exists(file_path):
        response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\n404 File Not Found"
        conn.sendall(response.encode())
        conn.close()
        return

    last_modified_ts = os.path.getmtime(file_path)
    last_modified_str = format_http_date(last_modified_ts)

    if 'if-modified-since' in headers:
        client_time = parse_http_date(headers['if-modified-since'])
        server_time = datetime.datetime.utcfromtimestamp(last_modified_ts)
        if client_time and server_time <= client_time:
            response = "HTTP/1.1 304 Not Modified\r\n\r\n"
            conn.sendall(response.encode())
            conn.close()
            return

    with open(file_path, 'rb') as f:
        content = f.read()

    response_headers = [
        "HTTP/1.1 200 OK",
        f"Content-Length: {len(content)}",
        "Content-Type: application/octet-stream",
        f"Last-Modified: {last_modified_str}",
        "\r\n"
    ]
    response = "\r\n".join(response_headers).encode() + content
    conn.sendall(response)
    conn.close()

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Serwer HTTP działa na http://{HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            handle_client(conn)

if __name__ == "__main__":
    run_server()
