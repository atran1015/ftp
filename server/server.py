import socket
import os
import sys

def send_file(conn, filename):
    filesize = os.path.getsize(filename)
    conn.send(str(filesize).encode())

    with open(filename, 'rb') as file:
        data = file.read(1024)
        while data:
            conn.send(data)
            data = file.read(1024)

def receive_file(conn, filename):
    filesize = int(conn.recv(1024).decode())

    # save
    with open(filename, 'wb') as file:
        received = 0
        while received < filesize:
            data = conn.recv(1024)
            received += len(data)
            file.write(data)

def main(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))

    server_socket.listen(1)

    # wait for connection
    
    print('Waiting for a client to connect...')
    conn, address = server_socket.accept()

    print(f'Connection established with {address}')

    while True:
        command = conn.recv(1024).decode()

        if command.startswith('get'):
            filename = command.split(' ')[1]
            send_file(conn, filename)

            print(f'Sent {filename} to client')
        elif command.startswith('put'):
            filename = command.split(' ')[1]
            receive_file(conn, filename)

            print(f'Received {filename} from client')
        elif command == 'ls':
            file_list = os.listdir('.')
            conn.send('\n'.join(file_list).encode())
        elif command == 'quit':
            break

    conn.close()
    server_socket.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python server.py <port_number>')
        sys.exit(1)
    
    port = int(sys.argv[1])
    main(port)
