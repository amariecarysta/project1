import socket

s = socket.socket()
s.connect(("localhost", 28333))

request = (
    "GET / HTTP/1.1\r\n"
    "Host: localhost\r\n"
    "Connection: close\r\n"
    "\r\n"

)

s.sendall(request.encode())


while True:

    d = s.recv(4096)
    if not d:
        break
    print(d.decode(errors="ignore"))

s.close()

    