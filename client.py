import socket

# Define the server's IP address and port
HOST = '127.0.0.1'
PORT = 8000

# Create a TCP socket and connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print(f"Connected to server {HOST} on port {PORT}")

# Registration process
while True :
    # Ask the user if they want to register or login
    action = input("Enter 'R' to register or 'L' to login: ").lower()
    
    if action == "r":
        # Get the new username and password from the user
        username = input("Enter your desired username: ")
        password = input("Enter your desired password: ")
        
        # Send the new username and password to the server for registration
        s.sendall(username.encode())
        s.sendall(password.encode())
        
        # Receive the registration status from the server
        status = s.recv(1024).decode()
        if status == "OK":
            print(f"User {username} registered successfully!")
            break
        else:
            print(f"Registration failed for {username}. Try a different username.")
            continue
    elif action == "l":
        # Get the username and password from the user
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        
        # Send the username and password to the server for authentication
        s.sendall(username.encode())
        s.sendall(password.encode())
        
        # Receive the authentication status from the server
        status = s.recv(1024).decode()
        if status == "OK":
            print(f"User {username} authenticated successfully!")
            break
        else:
            print(f"Authentication failed for {username}. Try again.")
            continue
    else:
        print("Invalid action. Try again.")
        continue
