#!/usr/bin/env python3 

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 10007        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello,world')
    data = s.recv(2048)
    s.sendall(b'GET /resolve?name=apple.com&type=A HTTP/1.1')
    data = s.recv(2048)

print('Received: ', repr(data))