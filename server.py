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
host = '127.0.0.1'
port = 10016    # range of possible ports   1-65535

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen(1)
sel.register(sock, selectors.EVENT_READ, data=None)

def error(error_c, con):
    codes = {
        400: "Bad Request",
        405: "Method Not Allowed"
    }
    error_msg = codes.get(error_c, "error")
    print("ERROR: " + error_msg)

    message = str.encode('HTTP/1.1 '+ str(error_c) + ' '+ error_msg + '\r\n\r\n')
    con.sendall(message)
    con.shutdown(1)
    exit(error_c)
def ok(con,msg):
    message = str.encode('HTTP/1.1 200 OK\r\n\r\n' + msg)
    con.sendall(message)
    con.close()
    exit(0)

def get_req(row, con):
    match = re.search(r'^\/resolve\?name=', row[1])
    if match:
        url = row[1].split("/resolve?name=",1)[1] 
        url = url.split("&type=",1)[0] 
        
        url_type = row[1].split("&type=",1)[1] 
        if url_type == "A":
            pattern = r"^(?:(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])(\.(?!$)|$)){4}$"
            match = re.match(pattern, url)
            if match is None:
                error(400, con)
                
            url = socket.gethostbyname(url)
            print(url)
            print(url_type)
            ok(con, url)

        elif url_type == "PTR":
            pattern = r"^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$"
            match = re.match(pattern, url)
            if match is None:
                error(400, con)
            print(url)
            print(url_type)
            ok(con, url)

    else:
        error(400, con)
    exit(0)

def parse(data,con):
    data = data.split("HTTP/1.1",1)[0] + "HTTP/1.1"
    data = data.split('\n\r')
    for row in data: 
        row = row.split(' ')
        print(row)
        if len(row) != 3:
            if row[0] == "POST" or row[0] == "GET":
                print(len(row))
                print(row)
                error(400, con)
            else:
                error(405, con)
        else:
            if row[0] == "POST" or row[0] == "GET":
                if row[2] != "HTTP/1.1" or len(data) != 1 and row[0] == "GET":
                    error(400,con)
                elif row[0] == "GET":
                    get_req(row, con)
            else:
                error(405, con)


def handler(con,a):
    while True:
        data = con.recv(2048)
        if not data:
            con.close()
            break
        data = str(data, 'utf-8')   #data to string
        parse(data,con)
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