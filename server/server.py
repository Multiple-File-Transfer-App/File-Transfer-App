import os
import socket

# Define the server's IP address and port
HOST = '127.0.0.1'
PORT = 8000

# Create a TCP socket and bind it to the server address
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

# Listen for incoming connections
s.listen()
print(f"Server listening on port {PORT}")

# Dictionary to store the registered users and passwords
users = {'john': 'pass123', 'jane': 'pass456'}

# Function to handle client connections
def handle_connection(conn, addr):
    print(f"New client connected: {addr}")
    
    # Login process
    while True:
        # Receive the username and password from the client
        username = conn.recv(1024).decode()
        password = conn.recv(1024).decode()
        
        # Check if the username and password are valid
        if username in users and users[username] == password:
            print(f"User {username} authenticated successfully!")
            conn.sendall(b"OK")
            break
        else:
            print(f"User authentication failed for {username}!")
            conn.sendall(b"FAIL")
            continue
    
    # Send the list of files to the client
    file_list = "\n".join(os.listdir())
    conn.sendall(file_list.encode())
    
    # Download process
    while True:
        # Receive the filename from the client
        filename = conn.recv(1024).decode()
        
        # Check if the user wants to quit
        if filename == "QUIT":
            break
        
        # Check if the file exists and is not a directory
        if os.path.isfile(filename):
            # Send the file size to the client
            file_size = os.path.getsize(filename)
            conn.sendall(str(file_size).encode())
            
            # Send the file data to the client in chunks
            with open(filename, 'rb') as f:
                chunk_size = 1024 * 1024  # 1 MB
                num_chunks = file_size // chunk_size
                if file_size % chunk_size != 0:
                    num_chunks += 1
                print(f"Number of chunks: {num_chunks}")
                
                for i in range(num_chunks):
                    data = f.read(chunk_size)
                    while data:
                        conn.sendall(data)
                        data = f.read(chunk_size)
                    print(f"Sent chunk {i+1} of {num_chunks}")
        else:
            conn.sendall(b"FAIL")
    
    # Close the connection
    conn.close()
    print(f"Connection closed for client {addr}")

# Accept incoming connections and start a new thread for each connection
while True:
    conn, addr = s.accept()
    handle_connection(conn, addr)
