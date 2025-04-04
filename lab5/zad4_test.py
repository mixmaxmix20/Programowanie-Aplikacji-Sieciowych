import socket
import time

SERVER_IP = '127.0.0.1'
PORT = 12345
BUFFER_SIZE = 1024
TEST_DATA = b'a' * 1024
REPEATS = 1000


def test_tcp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_IP, PORT))

        start = time.time()
        for _ in range(REPEATS):
            s.sendall(TEST_DATA)
            s.recv(BUFFER_SIZE)
        end = time.time()

        print(f"TCP Średni czas: {(end - start) * 1000 / REPEATS:.3f} ms")
    except Exception as e:
        print(f"Błąd TCP: {e}")
    finally:
        s.close()


def test_udp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        start = time.time()
        for _ in range(REPEATS):
            s.sendto(TEST_DATA, (SERVER_IP, PORT))
            s.recvfrom(BUFFER_SIZE)
        end = time.time()

        print(f"UDP Średni czas: {(end - start) * 1000 / REPEATS:.3f} ms")
    except Exception as e:
        print(f"Błąd UDP: {e}")
    finally:
        s.close()


if __name__ == "__main__":
    test_tcp()
    test_udp()