import socket
import threading
# AF_INET -> Internet address family for IPv4
# SOCK_STREAM -> socket type for TCP
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# associate the socket with a specific network interface
host = '127.0.0.1'
port = 10007    # range of possible ports   1-65535
sock.bind((host, port))

sock.listen(1)

connections = []

def parse(data):
    data = data.split(" ")
    if len(data) == 1:
        if data == "POST" or data == "GET":
            exit(0);
        
    print(len(data))
    print(data[0])
    print(data[1])

def handler(con,a):
    while True:
        data = con.recv(2048)
        if not data:
            con.close()
            break
        data = str(data, 'utf-8')   #data to string

        parse(data);

        data = str.encode(data)     #data to bytes
        con.send(data)

while True:
    con, a = sock.accept()
    con_thread = threading.Thread(target=handler, args=(con,a))
    con_thread.deamon = True
    con_thread.start()

