import socket
import threading
import re
import sys

import selectors
 # brief:   shuts connection and return error message
 # @param   $error_c:error message which will be send
 # @param   $con    :connection to shut-down
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


 # brief:   sends message and closes connection after succesful transfer
 # @param   $con    :current connection
 # @param   $msg    :return message
def ok(con,msg):
    message = str.encode('HTTP/1.1 200 OK\r\n\r\n' + msg)
    con.sendall(message)
    con.close()
    exit(0)


 # brief:   checks syntax of url
 # @param   $url    :url which will be checked
 # @param   $con    :current connection
def check_a(url, con):
    pattern = r"^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$"         
    match = re.match(pattern, url)
    if match is None:
        return True
    return False


 # brief:   checks syntax of ipv4 address
 # @param   $url    :address which will be checked
 # @param   $con    :current connection

def check_ptr(address, con):
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?= - -)"
    match = re.match(pattern, address)
    if match is None:
        return True
    return False


 # brief:   processes GET request from the client
 # @param   $row    :row with the request
 # @param   $con    :current connection

def get_req(row, con):
    match = re.search(r'^\/resolve\?name=', row[1])
    if match:
        url = row[1].split("/resolve?name=",1)[1] 
        url = url.split("&type=",1)[0] 
        url_type = row[1].split("&type=",1)[1] 

        if url_type == "A":
            if not check_ptr(url, con):
                error(400, con)
            try:
                url =url + ":A=" +socket.gethostbyname(url)
            except socket.gaierror:
                error(400, con)
            print(url)
            print(url_type)
            ok(con, url)

        elif url_type == "PTR":
            if not check_ptr(url, con):
                error(400, con)
            try:
                url =url + ":PTR=" +socket.gethostbyaddr(url)
            except socket.gaierror:
                error(400, con)
            print(url)
            print(url_type)
            ok(con, url)

    else:
        error(400, con)
    exit(0)

 # brief:   processes POST request from the client
 # @param   $row    :row with the request
 # @param   $con    :current connection
def post_req(row, con):
    match = re.search(r':', row)
    if match:
        row = row.split(':',1)
        url = row[0].strip()
        url_type = row[1].strip()

        if url_type == "A":
            if not check_ptr(url, con):
                return ""
            try:
                url =url + ":A=" +socket.gethostbyname(url)
            except socket.gaierror:
                return ""
            return url
        elif url_type == "PTR":
            if not check_ptr(url, con):
                return ""
            try:
                url =url + ":PTR=" + socket.gethostbyaddr(url)[0]
            except socket.gaierror:
                return ""
            return url
    return ""


 # brief:   checks and divides requests into categories
 # @param   $data   :request data
 # @param   $con    :current connection
def parse(data,con):
    match = re.search(r' HTTP/1.1', data)
    http_flag = True
    if match:
        data = data.split("HTTP/1.1",1)[0] + "HTTP/1.1\r\n\r\n"+ data.split("HTTP/1.1",1)[1]
        data = data.split('\r\n\r\n')
    else:
        http_flag = False

    row = data[0]
    row = row.split(' ')
    if len(row) != 3:
        if row[0] == "POST" or row[0] == "GET":
            error(400, con)
        else:
            error(405, con)
    elif not http_flag:
        error(400,con)
    else:
        if row[0] != "POST" and row[0] != "GET":
            error(405, con)
        elif row[2] != "HTTP/1.1":
            error(400,con)
        elif row[0] == "GET":
            get_req(row, con)               
        elif row[0] == "POST":
            url = ""
            for row in data: 
                row = row.split("\n")
                for request in row:
                    request = str(post_req(request, con))
                    if  request != "":
                        url = str(url) + request + "\r\n"
            ok(con, url)

 # brief:   handles recieving of data
 # @param   $con    :current connection

def handler(con,a):
    while True:
        data = con.recv(2048)
        if not data:
            con.close()
            break
        data = str(data, 'utf-8')   #data to string
        parse(data,con)
        con.close()
 # brief:   initialize server and divide simultanous connections into threads
 # @param   $con    :current connection
def start_server():
    sel = selectors.DefaultSelector()

    # AF_INET -> Internet address family for IPv4
    # SOCK_STREAM -> socket type for TCP
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # associate the socket with a specific network interface
    host = '127.0.0.1'

    # check correct number of arguments
    if len(sys.argv) != 2:
            print(sys.stderr, "Invalid number of arguments")
            exit(-1)
    # sssign argument to port
    port = int(sys.argv[1])
    # check if port is uint16
    if port > 65535 or port <= 0:
        print(sys.stderr, "Invalid PORT")
        exit(-2)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(1)
    sel.register(sock, selectors.EVENT_READ, data=None)
    try:
        #server loop
        while True:     
            con, a = sock.accept()
            con_thread = threading.Thread(target=handler, args=(con,a))
            con_thread.deamon = True
            con_thread.start()

    #accepting keyboard interupt ctrl+c
    except KeyboardInterrupt:
        print(sys.stderr, "Caught keyboard interrupt, exiting\n")
    finally:
        sel.close()

start_server()