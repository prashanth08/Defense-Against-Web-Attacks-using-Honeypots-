import sys
import os
import Queue
import re

EXIT_CODE = "/exit"
q_in = Queue.Queue()
q_out = Queue.Queue()

req  = """
POST /honeypot1 HTTP 1.1
Content-Type: message/http
Priority: 2
FlowTableKey: SIP_DIP_SPORT_DPORT_PROTOCOL
GroupID: 1
Content-Length: 72
GET /tutorials/other/top-20-mysql-best-practices/ HTTP/1.1
Host: net.tutsplus.com
User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Keep-Alive: 300
Connection: keep-alive
Cookie: PHPSESSID=r2t5uvjq435r4q7ib3vtdjq120
Pragma: no-cache
Cache-Control: no-cache

"""
request_headers = {}
#print req
#ast.literal_eval(req.replace('\r','\\r').replace('\n','\\n'))
try:
    req = req.split("\n")
    #print req
    '''for line in req:
        # If the line contains a colon, it's a header
        #
        if (line.find(':') != -1):
            #print line
            (key, value) = line.split(": ", 1)
            #request_headers[key] = value
            if(key=='Priority'):
                print value

        # Maybe it's a GET request...
        if (line.find("GET") != -1):
            print line
            location = re.findall(r'^GET / * /HTTP/.*', line)
            print location
            if len(location):
                request_headers['GET'] = location[0]
                print request_headers'''
        

    #return request_headers
    a3 = req[3].split(" ")
    pty = int(a3[1])
    print type(pty)
    print "Priority: " , pty
    a1 = req[4].split(" ")
    print "FlowTableKey: " , a1[1]
    a2 = req[5].split(" ")
    gid = int(a2[1])
    print "GroupID: " , gid
    get = "".join(req[7:])
    myCRString = get+'\r'
    get = get+'\n'
    get = get+'\r'
    get = get+'\n'
    print get
    for line in req:
        if(line.find("GET")!= -1):
            print line
            print req.index(line)
            location = re.findall(r'^GET / * /HTTP/.*', line)
            print location , len(location)
            



except IOError as exc:
    if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
        raise # Propagate other kinds of IOError.

    


