import socket
import os
import sys

# get server host and port from command line arguments
if len(sys.argv) != 3:
    print(f"Usage: python {sys.argv[0]} <server_host> <server_port>")
    sys.exit()
server_host = sys.argv[1]
server_port = int(sys.argv[2])

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
    print("Error creating socket:", e)
    sys.exit()

# connect server
try:
    client_socket.connect((server_host, server_port))
except socket.error as e:
    print("Error connecting to server:", e)
    client_socket.close()
    sys.exit()

while True:

    try:
        command = input("ftp> ")
    except KeyboardInterrupt:
        print("Interrupted.")
        client_socket.close()
        sys.exit()

    command_list = command.split()
    cmd = command_list[0]

    if cmd == 'quit':
        try:
            client_socket.sendall('quit'.encode())
        except socket.error as e:
            print("Error sending command:", e)
            client_socket.close()
            sys.exit()
        break

    elif cmd == 'get':
        try:
            filename = command_list[1]
            client_socket.sendall(f'get {filename}'.encode())
        except (IndexError, socket.error) as e:
            print("Error sending command:", e)
            continue

        try:
            filesize = int(client_socket.recv(1024).decode())
        except (ValueError, socket.error) as e:
            print("Error receiving filesize:", e)
            continue

        try:
            with open(f'received_{filename}', 'wb') as file:
                received = 0
                while received < filesize:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    received += len(data)
                    file.write(data)

            print(f'Download complete. {filesize} bytes received.')
        except (OSError, socket.error) as e:
            print("Error saving file:", e)
            continue

    elif cmd == 'put':
        try:
            filename = command_list[1]
            client_socket.sendall(f'put {filename}'.encode())
        except (IndexError, socket.error) as e:
            print("Error sending command:", e)
            continue

        if not os.path.exists(filename):
            print(f"File '{filename}' does not exist.")
            continue

        try:
            filesize = os.path.getsize(filename)
            client_socket.send(str(filesize).encode())
        except (OSError, socket.error) as e:
            print("Error getting filesize:", e)
            continue

        try:
            with open(filename, 'rb') as file:
                data = file.read(1024)
                while data:
                    client_socket.send(data)
                    data = file.read(1024)

            print(f'Upload complete. {filesize} bytes sent.')
        except (OSError, socket.error) as e:
            print("Error reading file:", e)
            continue

    elif cmd == 'ls':
        try:
            client_socket.sendall('ls'.encode())
        except socket.error as e:
            print("Error sending command:", e)
            continue

        try:
            data = client_socket.recv(1024).decode()
            print(data)
        except socket.error as e:
            print("Error receiving data:", e)
            continue

    else:
        print(f"Invalid command: {cmd}")

client_socket.close()
