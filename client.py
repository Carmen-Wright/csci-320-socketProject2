import socket
import os.path as path
import sys

IP = '127.0.0.1'  # change to the IP address of the server
PORT = 12000  # change to a desired port number
BUFFER_SIZE = 1024  # change to a desired buffer size


def get_file_size(file_name: str) -> int:
    size = 0
    try:
        size = path.getsize(file_name)
    except FileNotFoundError as fnfe:
        print(fnfe)
        sys.exit(1)
    return size


def send_file(filename: str, address: (str, int)):
    file_size = get_file_size(filename)
    size = (file_size).to_bytes(8, byteorder='big')
    name = filename.encode()


    # create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((IP, PORT))
        message = size + name
        client_socket.sendto(message, (IP, PORT))
        reply = client_socket.recv(BUFFER_SIZE)
        if reply != b'go ahead':
            raise Exception('Bad server response - was not go ahead!')

        with open(file_name, 'rb') as file:
            is_done = False
            while not is_done:
                chunk = file.read(BUFFER_SIZE)
                if len(chunk) > 0:
                    client_socket.send(chunk)
                elif len(chunk) == 0:
                    is_done = True


    except OSError as e:
        print(f'An error occurred while sending the file:\n\t{e}')
    finally:
        client_socket.close()


if __name__ == "__main__":
    # get filename from cmd line
    if len(sys.argv) < 2:
        print(f'SYNOPSIS: {sys.argv[0]} <filename> [IP address]')
        sys.exit(1)
    file_name = sys.argv[1]  # filename from cmdline argument
    # if an IP address is provided on cmdline, then use it
    if len(sys.argv) == 3:
        IP = sys.argv[2]
        print(IP)

    send_file(file_name, (IP, PORT))



