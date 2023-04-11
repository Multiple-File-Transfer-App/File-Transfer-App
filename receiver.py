import socket
import os
from cryptography.fernet import Fernet

# Define the encryption key
key = b'_vIt8OKkWlDGid-hI9MG9MpkvJc8fWdhrCp4F3qkGv4='
f = Fernet(key)

# Define the buffer size
BUFFER_SIZE = 4096

# Define the host and port to receive the file
# host = "localhost"
# port = 8000

host = input("Enter the host to connect: ")
port = int(input("Enter the port to connect: "))

# Create the socket object
s = socket.socket()

# Bind the socket to the host and port
s.bind((host, port))

# Listen for incoming connections
s.listen(1)

# Accept the connection from the sender
print("Waiting for sender to connect...")
conn, addr = s.accept()
print(f"Sender {addr[0]} connected.")

# Receive the file size from the sender
filesize_bytes = conn.recv(BUFFER_SIZE)

# Decode the file size from bytes to string and convert it to integer
filesize = int(filesize_bytes.decode())

# Define the output file name
output_filename = "received_file.txt"

# Open the output file in binary mode
with open(output_filename, "wb") as output_file:
    # Receive the data in chunks and write it to the output file
    while True:
        # Receive the encrypted data from the sender
        encrypted_data = conn.recv(BUFFER_SIZE)

        # If the data is empty, break the loop
        if not encrypted_data:
            break

        # Decrypt the data using the key
        decrypted_data = f.decrypt(encrypted_data)

        # Write the decrypted data to the output file
        output_file.write(decrypted_data)

# Close the connection and the socket
conn.close()
s.close()

# Print the success message and the location of the received file
print(f"File received and saved as {output_filename}")
print(f"Location: {os.getcwd()}/{output_filename}")
