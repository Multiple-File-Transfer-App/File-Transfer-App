import socket
import os
from cryptography.fernet import Fernet

# Define the encryption key
key = b'_vIt8OKkWlDGid-hI9MG9MpkvJc8fWdhrCp4F3qkGv4='
f = Fernet(key)

# Define the file to send
filename = "test.txt"

# Get the size of the file in bytes and encode it to bytes
filesize = os.path.getsize(filename)
filesize_bytes = str(filesize).encode()

# Define the buffer size
BUFFER_SIZE = 4096

# Define the host and port to send the file
host = "localhost"
port = 8000

# Create the socket object
s = socket.socket()

# Connect to the server
print(f"Connecting to {host}:{port}")
s.connect((host, port))

# Send the file size to the server
print(f"Sending file size: {filesize_bytes}")
s.send(filesize_bytes)

# Open the file and read the data in chunks
with open(filename, "rb") as file:
    print(f"Sending file: {filename}")
    while True:
        # Read the data from the file
        data = file.read(BUFFER_SIZE)

        # Check if the data is empty
        if not data:
            # If the data is empty, break the loop
            break

        # Encrypt the data using the key
        encrypted_data = f.encrypt(data)

        # Send the encrypted data to the server
        s.send(encrypted_data)

# Close the socket
s.close()

# Print the success message
print("File sent successfully.")
