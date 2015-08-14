#!/usr/bin/python

## A simple http server that can serve GET HTTP requests. Please help by putting in POST for the next project. 

import signal
import socket
import subprocess
import time

def graceful_shutdown(sig, dummy):  # Function that shutsdown a server instance
	s.shutdown()
	import sys
	sys.exit(1)

class Server:

	def __init__(self, port = 80):   #initializes server port as 80. Usually this will default to port 8080
		self.host = ''
		self.port = port
		self.www_dir = 'www'      #store files in www folder which is in same directory as server.py

	#function that activates server by binding socket to self.port and self.host
	def activate_server(self):
		
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			print ("Launching HTTP server on ", self.host, ":", self.port)
			self.socket.bind((self.host, self.port))

		except Exception as e:
			print ("Could not aquire port: ", self.port, "\n")
			
			user_port = self_port
			self_port = 8080

			try:
				print("Attempting to bind to new port: 8080")
				self.socket.bind((self.host, self.port))
			except Exception as e:
				print("Error: Failed to bind socket to ", user_port, " and port 8080.\n")
				print("Try running server as super user 'sudo' ")
				self.shutdown()
				import sys
				sys.exit(1)
		print ("Server successfully started on port: ", self.port)
		print("Press Ctrl C to shutdown the server and exit")
		self._wait_for_connections()

		#unbinds port essentially shutting down the server
	def shutdown(self):
		try:
			print ("Shutting down the server")
			s.socket.shutdown(socket.SHUT_RDWR)
		except Exception as e:
			print("Warning: could not shutdown the socket. ", e)


			#simple function which takes in a preset integer as a header code and returns the full HTTP header
	def _gen_headers(self, code):
		h = ''
		if (code==200):
			h = 'HTTP/1.1 200 OK\n'
		if (code == 404):
			h = 'HTTP/1.1 404 Not Found\n'

		current_date = time.strftime("%a, %d %b %y %H:%M:%S", time.localtime())
		h += 'Date: ' + current_date +'\n'
		h += 'Server: Basic-Python-HTTP-Server\n'
		h += 'Connection: close\n\n'  # signal that the conection wil be closed after complting the request

		return h

	#allow incoming connections from the world on the port
	def _wait_for_connections(self):
		while True:
			print("Awaiting new connection")
			self.socket.listen(5)

			conn, addr = self.socket.accept()  #conn is client socket, addr is client address

			print("new connection from", addr)

			data = conn.recv(4096)
			string = bytes.decode(data)
			request_method = string.split(' ')[0]   #split request string into seperate strings seperated by the spaces
			
			
			print("Method: ", request_method)
			print ("Request body: ", string)
			if (request_method == 'GET') | (request_method == 'HEAD'):
				file_requested = string.split(' ')
				file_requested = file_requested[1]
				file_requested = file_requested.split('?')[0]
				if (file_requested == '/'):
					file_requested = '/index.html'
        		file_requested = self.www_dir + file_requested

        		try:
        			file_handler = open(file_requested)
        			response_content = file_handler.read()
        			response_headers = self._gen_headers( 200)
        		except Exception as e:
        			print ("Warning, file not found. serving response code 404\n")
        			response_headers = self._gen_headers( 404)
        			if (request_method == 'GET'):
        				response_content = b"<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"
        		conn.send(response_content)
        		print ("Closing connection with client")
        		conn.close()
        	else:
        		print("Unknown HTTP request method:", request_method)
signal.signal(signal.SIGINT, graceful_shutdown)
print ("Starting web server")
s = Server(8080)
s.activate_server()



