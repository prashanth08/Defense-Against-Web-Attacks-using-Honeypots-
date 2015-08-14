import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('54.187.68.21', 80)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
try:
    
    # Send data
    message = 'GET /tutorials/other/top-20-mysql-best-practices/ HTTP/1.1 Host: net.tutsplus.com User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729) Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8 Accept-Language: en-us,en;q=0.5 Accept-Encoding: gzip,deflate Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7 Keep-Alive: 300 Connection: keep-alive Cookie: PHPSESSID=r2t5uvjq435r4q7ib3vtdjq120 Pragma: no-cache Cache-Control: no-cache'
    print >>sys.stderr, 'sending "%s"' % message
    myCRString = message+'\r'
    myCRLFString = myCRString+'\n'
    myCRLFString = myCRLFString+'\r'
    myCRLFString = myCRLFString+'\n'
    sock.sendall(myCRLFString)

    
    #receive reply
    msg = ''
    while len(msg) < 10000:
        chunk = sock.recv(100)
        if(chunk == ''):
            break
        msg = msg + chunk
     
    print >>sys.stderr, 'received "%s"' % msg


finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
