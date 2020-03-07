# HTTP-server
author: Andrej Ježík
## Domain name resolver
### Implementation details
As a language for implementation I have chosen Python version 3.8 because of its huge number of libraries for this purpose. <br>
Server runs on the local host (127.0.0.1) and the port is specified as an argument when the server is started.<br>
Server accepts 2 requests
##### POST
form: POST /dns-query HTTP/1.1 <br>
where: <br> 
dns-query contains list of requests.
##### GET
form: GET /resolve?name=some-name&type=some-type HTTP/1.1 <br>
where:  <br>
some-name =  ipv4 adress or url (www.google.com or 8.8.8.8) <br>
some-type =  "A" for url or "PRT" for ipv4 adress

#### Functions 

##### start_server()
Function accepts argument of the program, starts server, assign thread to each connection.
##### handler(con,a)
Handles recieved data and send them to the parser.
##### parse(data,con)
Parses requests, checks their general syntax and divide them into two types GET/POST and according it calls functions post_req or get_req.
##### post_req(row, con) and get_req(row, con)
Calls functions to check syntax of adresses or urls. Proccess actual requests and send them to client.
##### check_ptr(address, con) and check_a(url, con):
Check syntax of urls and ip adresses.
##### error(error_c, con) and ok(con,msg)
Shutdown or closes server and add header to the HTTP message


#### USED modules 

##### socket
I have used module socket which provides low-level networking interface which was perfect for creating simple HTTP server like this one

##### threading
I have used multithreading to allow  multiple connections to be established and the same time, one thread = one connection. To achieve this I have used module called threading.

##### re
For pasing and checking requests, especialy URLs I have used regexes among other methods. For this purpose I have imported module re. 

##### sys
Accepting PORT as an argument was required so I have use module sys to be able to check arguments and also use them for specifying on which PORT the server will be listening.

