#!/usr/bin/env python3
import socket
import os
import sys
import subprocess


def SendData(filename):
    fileObj = open(filename, "rb")
    fileData = fileObj.read(65536)
    if fileData:
        # print(fileData)
    	# Get the size of the data read
		# and convert it to string
        dataSizeStr = str(len(fileData))
        # print(type(fileData))
		# Prepend 0's to the size string
		# until the size is 10 bytes
        while len(dataSizeStr) < 10:
            dataSizeStr = "0" + dataSizeStr
	
	
		# Prepend the size of the data to the
		# file data.

        # convert bytes to str
        fileData = dataSizeStr + str(fileData)	
		
		# The number of bytes sent
        numSent = 0
		#print("number of bytes", fileData[numSent:].encode()) #this is sending 0000000022This is a test string
		
		# Send the data!
        while len(fileData) > numSent:
            numSent += connSock.send(fileData[numSent:].encode()) #this is sending bytes-object
	
	# The file has been read. We are done
    fileObj.close()
    return numSent
        

# Command line checks 
if len(sys.argv) < 3:
    print("USAGE python " + sys.argv[0] + " <FILE NAME>")
    sys.exit()

# Server address
serverAddr = "localhost"

serverPort = int(sys.argv[2])

# Server port
#serverPort = 1234

# The name of the file
#fileName = sys.argv[1]

# Open the file
#fileObj = open(fileName, "rb")

# Create a TCP socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
connSock.connect((serverAddr, serverPort))

# The number of bytes sent
numSent = 0

# The file data
fileData = None

# Keep sending until all is sent
while True:
    console_command="ftp> "
    user_input = input(console_command)
    filename = user_input[4:]

    # Read 65536 bytes of data
    
    if "get" in user_input:
        print("get command")
        
    elif "put" in user_input:
        print("put command")
        numSent = SendData(filename)
        print("File name: ", filename)
        print("Number of bytes transferred: ", numSent)
    elif "ls" in user_input:
        print("ls")
        subprocess.call(['ls'], stderr=subprocess.DEVNULL)
    elif "quit" in user_input:
        break
    else:
        print("invalid command")
    

# Close the socket and the file
connSock.close()
