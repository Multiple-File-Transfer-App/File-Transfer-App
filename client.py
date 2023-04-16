import socket
import libtorrent as lt
import time

host_c = '127.0.0.1'
port_c = 65432

# Function to send file to receiver
def send_file():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.connect((host_c, port_c))
        filename = soc.recv(1024).decode().strip()
        with open(filename, 'rb') as f1:
            data = f1.read(1024)
            while data:
                soc.sendall(data)
                data = f1.read(1024)
        print('> File sent successfully...')

# Function to receive file from sender
def receive_file(filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        host_temp = input('> Enter the ip of the sender.\n')
        port_temp = input('> Enter the port number\n')
        soc.bind((host_temp, int(port_temp)))
        soc.listen()
        con, addr = soc.accept()
        con.sendall(filename.encode())
        print('> Waiting for the Sender...\n')
        with open('received_file.txt', 'wb') as f3:
            while True:
                data = con.recv(1024)
                if not data:
                    break
                f3.write(data)
        print('> File received successfully')


# creating a socket object
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# initialize host and port
HOST = 'localhost'
PORT = 5000

# binding the socket to a public host
s.connect((HOST,PORT))

print(s.recv(1024).decode())

# prompting user choice 
choice = input('> ')

# sending uses choice to server
s.sendall(choice.encode())

# handling user's choice
if choice == '1' : 
    #login
    username = input('Username: ')
    password = input('Password: ')

    #sending username and password to server
    s.sendall(username.encode())
    s.sendall(password.encode())


    temp = s.recv(1024).decode().strip()
    
    if temp == 'Login Successful' :
        
        new_choice = input('> Select:\n (1) To download from multiple peers (2) To download from a specific peer.\n ')
        
        if new_choice == '1' :

            ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})

            file_name = input('> Please enter the name of the .torrent file\n')
            info = lt.torrent_info(file_name)

            h = ses.add_torrent({'ti': info, 'save_path': '.'})
            s2 = h.status()
            print('Starting to download', s2.name)

            while (not s2.is_seeding) :
                s2 = h.status()

                print('\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % (
        s2.progress * 100, s2.download_rate / 1000, s2.upload_rate / 1000,
        s2.num_peers, s2.state), end=' ')
                
                time.sleep(1)
            
            print(h.status().name, 'complete')

        elif new_choice == '2' :

            in_choice = input("> Please enter if you are (1) sending or (2) receiving file.\n")

            if in_choice == '1' :
                send_file()
            elif in_choice == '2' :
                filename = input('> Please enter the file name.\n')
                receive_file(filename)
            else:
                print("> Invalid choice. Please try again.\n")
    
    else :
        print(temp)
    

elif choice == '2' :
    # prompt the user for their username and password
    username = input('Choose a username: ')
    password = input('Choose a password: ')

    # send the username and password to the server
    s.sendall(username.encode())
    s.sendall(password.encode())

    # receive the response from the server
    print(s.recv(1024).decode())

elif choice == 'quit' : #do nothing
    print('quitting the server')

else : #invalid choice
    print('Invalid choice.')

s.close()