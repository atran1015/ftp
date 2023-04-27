import socket
import os
import sys

# get server host and port from command line arguments
if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} <server_host> <server_port>")
    sys.exit()
server_host = sys.argv[1]
server_port = int(sys.argv[2])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect server
client_socket.connect((server_host, server_port))

while True:


    command = input("ftp> ")
    
    command_list = command.split()
    cmd = command_list[0]
    
    if cmd == 'quit':
        client_socket.sendall('quit'.encode())
        break
    
    elif cmd == 'get':
        filename = command_list[1]
        client_socket.sendall(f'get {filename}'.encode())
        
        filesize = int(client_socket.recv(1024).decode())
        
        with open(f'received_{filename}', 'wb') as file:
            received = 0
            while received < filesize:
                data = client_socket.recv(1024)
                received += len(data)
                file.write(data)
                
            print(f'Download complete. {filesize} bytes received.')
        
    elif cmd == 'put':
        filename = command_list[1]
        
        
        # check if file exists
        if os.path.exists(filename):
            client_socket.sendall(f'put {filename}'.encode())
            filesize = os.path.getsize(filename)
        
            client_socket.send(str(filesize).encode())
            with open(filename, 'rb') as file:
                data = file.read(1024)
                while data:
                    client_socket.send(data)
                    data = file.read(1024)
            print(f'Upload complete. {filesize} bytes sent.')
        # if file doesn't exist
        else:
            print(f"File '{filename}' does not exist.")
            #continue
            
    elif cmd == 'ls':
        client_socket.sendall('ls'.encode())

        data = client_socket.recv(1024).decode()
        print(data)
    
    else:
        print(f"Invalid command: {cmd}")
        
client_socket.close()
