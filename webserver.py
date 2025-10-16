import socket, os
#return MIME type based on file extension
def content_type(path: str):
    extension = os.path.splitext(path)[1].lower()
    if extension == ".txt":
        return "text/plain"
    if extension == ".html":
        return "text/html"
    return "application/octet-stream"  #anything else
    

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", 28333))
s.listen(5)

print("My server ears are listening on port 28333...")


#Keep running the server until all data is through-
while True:
    connection, address = s.accept()
    data = b""
    while b"\r\n\r\n" not in data:
        part = connection.recv(1)
        if not part:          #if client closed or nothing more to be read, quit
            break
        data += part


    #parse--take the first line of the request, split, only GET, close, and wait
    request_line = data.split(b"\r\n", 1)[0]    
    parts = request_line.split()
    if len(parts) < 2 or parts[0] != b"GET":
        connection.close()
        continue

    target = parts[1].split(b"?", 1)[0].decode("ascii", "ignore") 
    filename = "index.html" if target == "/" else target.lstrip("/") #strip first "/"


     #read in bytes and store   
    try:
        with open(filename, "rb") as fp:
            payload = fp.read()
        content_t = content_type(filename) #find content type
        headers = (                        #response headers
            "HTTP/1.1 200 OK\r\n"
            f"Content-Type: {content_t}\r\n"
            f"Content-Length: {len(payload)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode("ascii")
        connection.sendall(headers + payload)

     #throw error if neccesary
    except:
        message = b"404 Not Found"
        response = (
            b"HTTP/1.1 404 Not Found\r\n"
            b"Content-Type: text/plain\r\n"
            b"Content-Length: 13\r\n"
            b"Connection: close\r\n"
            b"\r\n"
        ) + message
        connection.sendall(response)

    connection.close()



#references
#https://realpython.com/python-sockets/#:~:text=Socket%20programming%20is%20essential%20for,and%20using%20exceptions%20like%20OSError%20.

#https://theswissbay.ch/pdf/Gentoomen%20Library/Programming/Python/Beginning%20Python.pdf 
    
