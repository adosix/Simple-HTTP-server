import socket
import threading
# AF_INET -> Internet address family for IPv4
# SOCK_STREAM -> socket type for TCP
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# associate the socket with a specific network interface
host = '127.0.0.1'
port = 10000    # range of possible ports   1-65535
sock.bind((host, port))

sock.listen(1)

connections = []

def handler(c,a):
    global connections
    while True:
        data = c.recv(2048)
        for connection in connections:
            connection.send(bytes(data))
        if not data:
            connections.remove(c)
            c.close()
            break
while True:
    c, a = sock.accept()
    cThread = threading.Thread(target=handler, args=(c,a))
    cThread.deamon = True
    cThread.start()
    connections.append(c)
    print(connections)

