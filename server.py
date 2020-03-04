import socket
import threading
import re
from urllib.parse import urlparse

import selectors
sel = selectors.DefaultSelector()

# AF_INET -> Internet address family for IPv4
# SOCK_STREAM -> socket type for TCP
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# associate the socket with a specific network interface
host = socket.gethostname()
port = 10015    # range of possible ports   1-65535

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen(1)
sel.register(sock, selectors.EVENT_READ, data=None)

def error(error_c):
    codes = {
        400: "Bad Request",
        405: "Method Not Allowed"
    }
    error_msg = codes.get(error_c, "error")
    print("ERROR: " + error_msg)
    exit(error_c)

def get_req(row):
    #pattern = re.compile(r"\b" + "\/resolve?name=" + r"\b")
    #print(row[1])
    match = re.search(r'^\/resolve\?name=', row[1])
    if match:
        url = row[1].split("/resolve?name=",1)[1] 
        url = url.split("&type=",1)[0] 
        url_type = row[1].split("&type=",1)[1] 
        print(socket.getaddrinfo(url, '80'))
        # from ip to dn GetnameInfo()
        #row = str.encode(','.join(row))     #data to bytes
        url = str.encode(url_type)
        con.send(url)
    else:
        error(400)
    exit(0)

def parse(data,con):
    data = data.split('\n\r')
    for row in data: 
        row = row.split(' ')
        if len(row) != 3:
            if row[0] == "POST" or row[0] == "GET":
                print(len(data))
                error(400)
            else:
                con.close()
                error(405)
        else:
            if row[0] == "POST" or row[0] == "GET":
                if row[2] != "HTTP/1.1" or len(data) != 1 and row[0] == "GET":
                    error(400)
                elif row[0] == "GET":
                    get_req(row);
            else:
                error(405)


def handler(con,a):
    while True:
        data = con.recv(2048)
        if not data:
            con.close()
            break
        data = str(data, 'utf-8')   #data to string

        parse(data,con);
        con.close()

try:
    while True:
        con, a = sock.accept()
        con_thread = threading.Thread(target=handler, args=(con,a))
        con_thread.deamon = True
        con_thread.start()

except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()