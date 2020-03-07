#!/usr/bin/env python3 

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 10016        # The port used by the server

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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
     s.connect((HOST, PORT))
     s.sendall(b'GET /resolve?name=www.facebook.com&type=A HTTP/1.1')
     data = s.recv(2048)
     print(repr(data))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
     s.connect((HOST, PORT))
     s.sendall(b'GET /resolve?name=apple.c om&type=A HTTP/1.1')
     data = s.recv(2048)
     print(repr(data))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
     s.connect((HOST, PORT))
     s.sendall(b'GET /resolve?name=apple.cofm&type=A HTTP/1.1')
     data = s.recv(2048)
     print(repr(data))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
     s.connect((HOST, PORT))
     s.sendall(b'GET /resolve?name=appdle.com&type=A HTTP/1.1')
     data = s.recv(2048)
     print(repr(data))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
     s.connect((HOST, PORT))
     s.sendall(b'GET /resolve?name=w.apple.com&type=A HTTP/1.1')
     data = s.recv(2048)
     print(repr(data))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
     s.connect((HOST, PORT))
     s.sendall(b'GET /resolve?name=f.apple.com&type=A HTTP/1.1')
     data = s.recv(2048)
     print(repr(data))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
     s.connect((HOST, PORT))
     s.sendall(b'GET /resolve?name=aa-apple.com&type=A HTTP/1.1')
     data = s.recv(2048)
     print(repr(data))