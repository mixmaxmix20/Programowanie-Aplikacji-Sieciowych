import socket
import urllib.parse

name = input("Podaj swoje imię: ")
email = input("Podaj swój adres e-mail: ")

form_data = urllib.parse.urlencode({
    "name": name,
    "email": email
})

form_data_bytes = form_data.encode()

request = f"""POST /post HTTP/1.1\r
Host: httpbin.org\r
User-Agent: MyClient/1.0\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: {len(form_data_bytes)}\r
Connection: close\r
\r
""".encode() + form_data_bytes

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("httpbin.org", 80))
    s.sendall(request)

    response = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        response += chunk

print("Odpowiedź serwera:")
print(response.decode(errors="replace"))
