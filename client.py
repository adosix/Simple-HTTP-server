#!/usr/bin/env python3 

import socket

HOST = socket.gethostname()  # The server's hostname or IP address
PORT = 10015        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello,world')
    data = s.recv(2048)
    print(repr(data))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'GET /resolve?name=apple.com&type=A HTTP/1.1')
    data = s.recv(2048)
    print(repr(data))