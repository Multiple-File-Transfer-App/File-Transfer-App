import socket
import os
from cryptography.fernet import Fernet
import bcrypt
from tqdm import tqdm

# Define the encryption key
key = b'_vIt8OKkWlDGid-hI9MG9MpkvJc8fWdhrCp4F3qkGv4='
f = Fernet(key)

# Define the host and port to receive the file
host = "localhost"
port = 8000

# Create the socket object
s = socket.socket()

# Bind the socket to a specific address and port
s.bind((host, port))

# Listen for incoming connections
s.listen(1)

# Wait for a connection
print("Waiting for a connection...")
conn, addr = s.accept()
print(f"Connected to {addr}")

# Receive the hashed username from the client
hashed_username = conn.recv(1024)

# Receive the hashed password from the client
hashed_password = conn.recv(1024)

# Get the username and password from the user
username = input("Enter your username: ")
password = input("Enter your password: ").encode()

# Hash the entered username and password
hashed_entered_username = bcrypt.hashpw(username.encode(), hashed_username)
hashed_entered_password = bcrypt.hashpw(password, hashed_password)

# Check if the entered username and password match the received username and password
if hashed_entered_username == hashed_username and hashed_entered_password == hashed_password:
    print("Authentication successful.")
    # Send an OK message to the client to indicate successful authentication
    conn.send("OK".encode())

    # Receive the file size from the client
    filesize_bytes = conn.recv(1024)

    # Decode the file size to an integer
    filesize = int(filesize_bytes.decode())

    # Allocate the buffer size based on the file size
    buffer_size = min(filesize, 65536)

    # Initialize the progress bar
    progress = tqdm(total=filesize, unit="B", unit_scale=True, desc="Receiving file")

    # Receive the file data in chunks and write it to a file
    with open("received_file.txt", "wb") as file:
        while filesize > 0:
            # Receive the encrypted data from the client
            encrypted_data = conn.recv(buffer_size)

            # Decrypt the data using the key
            try:
                data = f.decrypt(encrypted_data)
            except Exception as e:
                print("Error decrypting data packet.")
                print(f"Encrypted data: {encrypted_data}")
                print(f"Exception: {e}")
                break

            # Write the data to the file
            file.write(data)

            # Subtract the number of bytes received from the file size
            filesize -= len(data)

            # Update the progress bar
            progress.update(len(data))

            # Update the buffer size if needed
            if filesize < buffer_size:
                buffer_size = filesize

    # Close the progress bar
    progress.close()

    # Close the connection and socket
    conn.close()
    s.close()

    print("File received successfully.")
else:
    print("Authentication failed.")

    # Close the connection and socket
    conn.close()
    s.close()
