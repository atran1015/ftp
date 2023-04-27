import socket
import os
import sys

def send_file(conn, filename):
    filesize = os.path.getsize(filename)
    conn.send(str(filesize).encode())

    with open(filename, 'rb') as file:
        data = file.read(1024)
        while data:
            sent = conn.send(data)
            data = file.read(1024 - sent)
        print(f"File '{filename}' sent.")

def receive_file(conn, filename):
    filesize = int(conn.recv(1024).decode())

    # save
    with open(filename, 'wb') as file:
        received = 0
        while received < filesize:
            data = conn.recv(1024)
            received += len(data)
            file.write(data)
        print(f"File '{filename}' received.")

def main(port):
    try:
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
                try:
                    send_file(conn, filename)
                except FileNotFoundError:
                    conn.send(b'File not found.')
                except Exception as e:
                    conn.send(str(e).encode())
            elif command.startswith('put'):
                filename = command.split(' ')[1]
                try:
                    receive_file(conn, filename)
                except Exception as e:
                    conn.send(str(e).encode())
            elif command == 'ls':
                file_list = os.listdir('.')
                conn.send('\n'.join(file_list).encode())
            elif command == 'quit':
                break

        conn.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server_socket.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python server.py <port_number>')
        sys.exit(1)
    
    port = int(sys.argv[1])
    main(port)
