import socket


# creating a socket object
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# initialize host and port
HOST = 'localhost'
PORT = 5000

# binding the socket to a public host
s.bind((HOST,PORT))

s.listen(1)


# dict to store credentials
creds = dict()

with open('server/login_cred.txt','r') as f :
    for line in f :
        temp = line.split(' ')
        creds[temp[0]] = temp[1].rstrip()


print('Server Started')

while True :

    # wait for a connection
    conn, addr = s.accept()

    # Welcome message to client asking for log
    conn.sendall(b'Welcome to the UGA Torrent server! Please choose an option: log in (1) or register (2).\n')

    choice = conn.recv(1024).decode().strip()

    # handling the choice
    if choice == '1' :
        # login
        username = conn.recv(1024).decode().strip()
        password = conn.recv(1024).decode().strip()

        if username in creds and creds[username] == password :
            conn.sendall(b'Login Successful\n')
        
        else:
            conn.sendall(b'Invalid Username or Password\n')

    elif choice == '2' :
        #register
        username = conn.recv(1024).decode().strip()
        password = conn.recv(1024).decode().strip()
        
        creds[username] = password

        with open('login_cred.txt','w') as f :
            for k,v in creds.items() :
                f.write(k + ' ' + v + '\n')

        f.close()

        conn.sendall(b'Account created rerun to login!\n')

    elif choice.lower() == 'quit' :
        break

    else : #invalid choice 
        conn.sendall(b'Invalid choice.\n')



conn.close()

