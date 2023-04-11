import os
import socket
import argparse
import sys
from cryptography.fernet import Fernet

def encrypt_file(key, filepath):
    """
    Encrypts the file at the given file path using the provided key.

    Parameters:
    key (bytes): the encryption key
    filepath (str): the file path of the file to encrypt
    """
    with open(filepath, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)

    with open(filepath, 'wb') as f:
        f.write(encrypted_data)

def send_file(filepath, host, port, key):
    """
    Sends the file at the given file path to the specified host and port
    using a socket connection. The file is encrypted before being sent
    using the provided key.

    Parameters:
    filepath (str): the file path of the file to send
    host (str): the host to send the file to
    port (int): the port to use for the socket connection
    key (bytes): the encryption key to use for encrypting the file
    """
    # Encrypt the file before sending
    encrypt_file(key, filepath)

    # Create a socket connection and connect to the specified host and port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    # Send the filename and file contents over the socket
    filename = os.path.basename(filepath)
    sock.sendall(filename.encode())
    with open(filepath, 'rb') as f:
        sock.sendall(f.read())

    # Close the socket connection
    sock.close()

    print(f"File '{filename}' sent successfully to {host}:{port}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send a file over a socket connection.')
    parser.add_argument('file', metavar='file', type=str, help='the file to send')
    parser.add_argument('host', metavar='host', type=str, help='the host to send the file to')
    parser.add_argument('port', metavar='port', type=int, help='the port to use for the socket connection')
    args = parser.parse_args()

    # Define the encryption key
    key = b'_5FB9tA2P7VHv8mWk7VJ1wqop3NYRKb1adz0Z0oX9Dg='

    # Send the file to the specified host and port
    send_file(args.file, args.host, args.port, key)
