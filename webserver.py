import socket

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", 28333))
s.listen(5)

print("My server ears are listening on port 28333...")



while True:
    new_conn = s.accept()
    new_socket = new_conn[0]


    data = b""
    while b"\r\n\r\n" not in data:
        chunk = new_socket.recv(4096)
        if not chunk:
            break
        data += chunk

    body = b"<!doctype html><html><body><h1>I'm working..Yay!</h1></body></html>"
    response = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Type: text/html; charset=UTF-8\r\n"
        + f"Content-Length: {len(body)}\r\n".encode("ascii")
        + b"Connection: close\r\n"
        b"\r\n"
        + body
    )


     
    new_socket.sendall(response)
    new_socket.close()