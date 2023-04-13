import socket
import os
from cryptography.fernet import Fernet
import bcrypt

# Define the encryption key
key = b'_vIt8OKkWlDGid-hI9MG9MpkvJc8fWdhrCp4F3qkGv4='
f = Fernet(key)

# Define the buffer size
BUFFER_SIZE = 65536  # increased buffer size

# Define the host and port to send the file
host = "localhost"
port = 8000

# Create the socket object
s = socket.socket()

# Connect to the server
s.connect((host, port))

# Get the username and password from the user
username = input("Enter your username: ")
password = input("Enter your password: ").encode()

# Hash the entered username and password
hashed_entered_username = bcrypt.hashpw(username.encode(), bcrypt.gensalt())
hashed_entered_password = bcrypt.hashpw(password, bcrypt.gensalt())

# Send the hashed username to the server
s.send(hashed_entered_username)

# Send the hashed password to the server
s.send(hashed_entered_password)

# Receive the authentication result from the server
auth_result = s.recv(BUFFER_SIZE).decode()

# Check if the authentication was successful
if auth_result == "OK":
    print("Authentication successful.")

    # Get the file to send from the user
    file_path = input("Enter the path of the file to send: ")

    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"File '{file_path}' does not exist.")
        # Close the connection
        s.close()
        exit()

    # Get the size of the file
    filesize = os.path.getsize(file_path)

    # Send the file size to the server
    s.send(str(filesize).encode())

    # Send the file data in chunks
    with open(file_path, "rb") as file:
        print("Sending file...")
        while True:
            # Read a chunk of data from the file
            data = file.read(BUFFER_SIZE)

            # Check if the end of file has been reached
            if not data:
                break

            # Encrypt the data using the key
            encrypted_data = f.encrypt(data)

            # Send the encrypted data to the server
            s.send(encrypted_data)

    # Close the connection
    s.close()

    print("File sent successfully.")
else:
    print("Authentication failed.")

    # Close the connection
    s.close()
