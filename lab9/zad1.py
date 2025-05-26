import socket

host = "httpbin.org"
port = 80
request_path = "/html"

http_request = f"""GET {request_path} HTTP/1.1\r
Host: {host}\r
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A\r
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

header_data, html_data = response.split(b"\r\n\r\n", 1)

with open("strona.html", "wb") as file:
    file.write(html_data)

print("Strona została zapisana jako 'strona.html'")
