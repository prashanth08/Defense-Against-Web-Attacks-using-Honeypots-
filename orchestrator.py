import socket
import select
import sys
import Queue
import re
from datetime import timedelta, datetime
import time
try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser

result = []
file = open('/var/ossec/logs/alerts/alerts.log','r')
FMT = '%Y%b%d%H:%M:%S'

q = Queue.Queue()



class Server:
    def __init__(self):
        self.host    = ''
        self.port    = [5555,5556]
        self.server  = None
        self.inputs  = []
        self.running = True

    # Open the Main Server Socket
    def open_socket(self):
        try:
            for port in self.port:
                print port
                sock_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock_conn.bind((self.host, port))
                sock_conn.listen(5)
                sock_conn.setblocking(0)

                print "Listening on %s:%s" % (self.host, port)
                self.inputs.append(sock_conn)#connections

        except socket.error, (value, message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)


    # Process a command received on the local console
    def process_console_command(self, cmd):
        print "console: %s" % cmd

        if (cmd == "quit"):
            self.shutdown()

    def process_new_conn(self,sockfd):
        data = ''
        sockfd.settimeout(2)
        
        while True:
            try:
                data2 = sockfd.recv(1024)
                print data2
                if not data2:
                    break
                data = data + data2

            except socket.timeout as e:
                break
             
        

        p = HttpParser()
        #data = str.replace(data, '\n', '\r\n')
        recved = len(data)
        nparsed = p.execute(data, recved)
        #assert nparsed == recved
        #import pdb
        #pdb.set_trace()
        assert nparsed == recved
        #get_head = p.get_headers()
        get_path = p.get_path()
        #print get_path
        if(get_path == '/status'):
            print "---------------Receiving data from DDOS Detector for a response------------------"
            self.process_status_req(sockfd)
            print "--------------------------------------------------------------"
        else:
            print "---------------Receiving data from DDOS Detector to replay it in a honeypot------------------"
            self.process_replay_req(sockfd,p)
            print "--------------------------------------------------------------"

    # Process a message from a connected client
    def process_replay_req(self, client, parse_obj):
        # Message from a client
        
        #rint data
        client.send("HTTP/1.1 200 OK")
        #r = requests.get('http://10.156.1.113') 
        #print 'Response from VM1 is',r.status_code
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        a = datetime.now()

# Connect the socket to the port where the server is listening

        server_address = ('192.168.0.24', 80)
        print >>sys.stderr, 'connecting to %s port %s' % server_address
        sock.connect(server_address)
        server_address2 = ('10.0.3.152', 80)
        print >>sys.stderr, 'connecting to %s port %s' % server_address2
        sock2.connect(server_address2)

        res2 = None;
        t1 = None;
        try:
    
            # Send data
            #message = 'GET /tutorials/other/top-20-mysql-best-practices/ HTTP/1.1 Host: net.tutsplus.com User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729) Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8 Accept-Language: en-us,en;q=0.5 Accept-Encoding: gzip,deflate Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7 Keep-Alive: 300 Connection: keep-alive Cookie: PHPSESSID=r2t5uvjq435r4q7ib3vtdjq120 Pragma: no-cache Cache-Control: no-cache'
            
            try:
                #print recved
                get_head = parse_obj.get_headers()
                gid = int(get_head['Group-Id'])
                ftk = str(get_head['Flow-Table-Key'])
                cl = int(get_head['Content-Length'])
                get_body = parse_obj.recv_body()
                get_body = get_body+'\r'
                get_body = get_body+'\n'
                get_body = get_body+'\r'
                get_body = get_body+'\n'
                #import pdb
                #pdb.set_trace()
                print "---------------Sending Data to Apache Web Server and Wordpress Server------------------"
                print >>sys.stderr, 'sending "%s"' % get_body

                sock.sendall(get_body)
                sock2.sendall(get_body)
                print "--------------------------------------------------------------"
                #print get_head
                #print type(get_body)
                #print get_body

            
            except IOError as exc:
                if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
                    raise # Propagate other kinds of IOError.


    
            #receive reply
            msg = ''
            print "---------------Receiving Response from Apache Web Server------------------"
            while len(msg) < 10000:
                chunk = sock.recv(100)
                if(chunk == ''):
                    break
                msg = msg + chunk
     
            print >>sys.stderr, 'received "%s"' % repr(msg)
            print "--------------------------------------------------------------"
            msg = ''
            print "---------------Receiving Response from Wordpress Server------------------"
            while len(msg) < 10000:
                chunk = sock2.recv(100)
                if(chunk == ''):
                    break
                msg = msg + chunk
     
            print >>sys.stderr, 'received "%s"' % repr(msg)
            print "--------------------------------------------------------------"

            b = datetime.now()
            time.sleep(20)
            b = b + timedelta(seconds=20)

            event_list = []
            print "-------------------------Parsing OSSEC log---------------------------"
            try:
                #with open(files) as f: # No need to specify 'r': this is the default.
                data = [line for line in file.readlines()]
                for line in data:
                    if line.startswith("**"):

                        index = data.index(line)
                        res1 = data[index+1].split(" ")
                        #print res1
                        timestamp1 = res1[0] , res1[1] , res1[2] , res1[3]
                        timestamp1 = ''.join(timestamp1) 
                        #print "Timestamp: " , timestamp1
                        #print "Location: " + res1[4]
                        res2 = data[index+2].split("->")
                        rule = res2[0].find("Rule: ")
                        #print "Rule Number: ",res2[0][6] + res2[0][7] #+ res2[0][8] + res2[0][9] 
                        level = res2[0].find("level")
                        #print "Level: ",res2[0][16]
                        #print "Event = " + res2[1]
                        res3 = data[index+3]
                        #print "Detailed Description: " + res3
                        #print res3
                        t1 = datetime.strptime(timestamp1, FMT)
                        #print event_list
                        
                        if ( a < t1 and t1 < b):  

                            event_list.append(res2[1])
                        

            except IOError as exc:
                if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
                    raise # Propagate other kinds of IOError.'''
        finally:
            #print >>sys.stderr, 'closing socket'
            print "--------------------------------------------------------------"
            sock.close()
        Is_Suspicious = 0
        print "-----------------------Building orchestrator Response------------------------------"
        if(res2 and res2[1]!=''):
            Is_Suspicious = 1            
        resp_head = "HTTP/1.1 200 OK" + '\r\n'
        resp_head = resp_head +"Flow-Table-Key: " + ftk  + '\r\n'
        resp_head = resp_head + "Group-Id: " + str(gid) + '\r\n'
        resp_head = resp_head + "Is_Suspicious: " + str(Is_Suspicious) + '\r\n'
        resp_head = resp_head + "Content-Length: "  + str(cl)  + "\r\n\r\n"
        resp_head = resp_head + get_body
        #import pdb
        #pdb.set_trace()
        resp_head = str(resp_head)

        #print "Initial Timestamp: ",a ,"\n","Alert Timestamp: " , t1 ,"\n","Final Timestamp: ", b , "\n"

                #print t1
                    #print "delta2",delta2.total_seconds()
                    #print "delta3",delta3.total_seconds()
                #print "--------------------------------------------------------------------------------"

                # Close the connection with this client
        print event_list
        s = ','.join(event_list)
        resp_head = resp_head + s + "\r\n"
        q.put(resp_head)   

           

            
        #client.socket.close()
        #self.inputs.remove(client)
        #print "client disconnecting"

    def process_status_req(self,sockfd):


                #print >>sys.stderr, 'connection from', (reply_host, reply_port)

                # Receive the data in small chunks and retransmit it
            #while True:
                    #data = clientsock.recv(1024)
                    #print >>sys.stderr, 'received "%s"' % data

        print >>sys.stderr, 'sending data back to the client'
            #clientsock.send("FlowTableKey: " + a1[1] + '\n')
            #clientsock.send("GroupID: " + a2[1] + '\n')
            #clientsock.send("Content Length: " + a4[1] + '\n')
            #clientsock.send(get + '\n')
            #clientsock.send(res2[1])
            #print q.get()
        print q.qsize()
        if q.qsize() > 0:
            get = q.get()
            print get
            g = sockfd.send(get)
            print g
        else:
            print "The queue is empty"
            #get = "The queue is empty"
            #sockfd.sendall("The queue is empty")
            return
        
        print q.qsize()
                            


    # Send a message to all connected clients
    def sendall(self, data):
        #for c in self.inputs:
                # Only send a message if the user has "logged in" (we have a username)
        c.send(data)

    # Shutdown the server
    def shutdown(self):
        # Close all the connected clients
        for c in self.inputs:
            self.inputs.remove(c)
            #c.send("Server Shutting Down!\n")
            c.socket.close()
        self.running = False


    # Main Server Loop
    def run(self):
        # Input Sources

        self.running = True
        while self.running:

            # Check if any of our input sources have data ready for us
            inputready, outputready, exceptready = select.select(self.inputs, [], [])

            for s in inputready:
                if s == self.inputs[0] or s == self.inputs[1]:
                    sockfd, addr = s.accept()
                    #sockfd.send("HTTP/1.1 200 OK\n")
                    self.inputs.append(sockfd)#clients
                    #sockfd.setblocking(0)
                    print "Client (%s, %s) connected" % addr
                    self.process_new_conn(sockfd)
                #else:
                    #self.process_new_conn(s)



        # Shutdown the Server
        self.shutdown()


# Class to keep track of a connected client
class Client:
    def __init__(self, (socket, address)):
        self.socket     = socket
        self.address    = address
        self.size       = 1024

        self.socket.setblocking(0)

    # Pass along the server's fileno() refernce.
    # This lets the Client class pretend to be a socket
    def fileno(self):
        return self.socket.fileno()

     # Send message to Client
    def send(self, data):
        self.socket.send(data)




if __name__ == "__main__":
    # Create our server instance
    print "---------------Starting orchestrator------------------"
    s = Server()
    # Start Listening for incomming connections
    s.open_socket()
    # Main loop of our server
    s.run()
