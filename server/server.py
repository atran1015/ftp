import socket
import os
import sys
from string import digits
from pathlib import Path

def send_file(conn, filename):
    # if file does exist
    if os.path.exists(filename):
        # do this
        try:
            filesize = os.path.getsize(filename)
            conn.send(str(filesize).encode())

            with open(filename, 'rb') as file:
                data = file.read(1024)
                while data:
                    sent = conn.send(data)
                    data = file.read(1024 - sent)
                print(f"File '{filename}' sent.")
            print("SUCCESS")
        # handle get error
        except Exception as e:
            print("Get Error: ", str(e))
            print("FAILURE")
    # if file doesn't exist, send error string
    else:
        conn.send(str("ERROR").encode())
        print("FAILURE")

def receive_file(conn, filename):
    """ For put method """
    try:
        #print("this is filename: ", filename)

        # get dynamic file path and get filesize from file that belongs to client folder
        root_folder = Path(__file__).parents[1]
        my_path = str(root_folder)+ "/client/" + filename
        filesize = os.path.getsize(my_path)
        
        with open(filename, 'wb') as file:
            received = 0
            while received < filesize:
                data = conn.recv(1024)
                received += len(data)
                file.write(data)
        
        print("SUCCESS")
    except Exception as e:
        # catch all errors to prevent crashing
        print("FAILURE")
        print("Error encountered: ", str(e))

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
                # get extension of filename
                extension = filename.split(".")[-1]
                #print("this is file extension: ", extension)

                logicBool = False
                # check if extension contains digit, meaning bytes is being attached to extension "txt42"
                for i in extension:
                    if i.isdigit():
                        logicBool = True

                # if extension does contain digit
                if logicBool:
                    #print("filename contains digit")
               
                    # remove the digits from the extension
                    remove_digits = str.maketrans('', '', digits)
                    res = extension.translate(remove_digits)
                    # rejoin the strings together without the digits
                    join_string = filename.split(".")[0] + "." + res                
                    try:
                        receive_file(conn, join_string)
                    except Exception as e:
                        conn.send(str(e).encode())
                else:
                    try:
                        receive_file(conn, filename)
                    except Exception as e:
                        conn.send(str(e).encode())

            elif command == 'ls':
                file_list = os.listdir('.')
                print("SUCCESS")
                conn.send('\n'.join(file_list).encode())
            elif command == 'quit':
                print("SUCCESS")
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
