import socket
import tqdm
import os
import datetime

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024


def send_file(filename, host, port):
    filesize = os.path.getsize(filename)
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    # send the filename and filesize
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # use 'with open' to read the file contents and send it
    with open(filename, "rb") as f:
        # start sending the file
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transmission in busy networks
            s.sendall(bytes_read)
            # update the progress bar manually
            progress.update(len(bytes_read))

    # close the socket
    s.close()
    print(f"[+] File {filename} sent successfully to {host}:{port}")


def receive_file(host, port):
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    print(f"[*] Listening as {host}:{port}")
    while True:
        client_socket, address = s.accept()
        print(f"[+] {address} is connected.")

        # receive the file info
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)

        # create a new filename with the current date and time
        now = datetime.datetime.now()
        new_filename = f"Received File {now.strftime('%Y-%m-%d %H-%M-%S')}_{filename}"

        # use 'with open' to write the file contents
        with open(new_filename, "wb") as f:
            # start receiving the file
            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                # update the progress bar manually
                progress.update(len(bytes_read))

        # close the client socket
        client_socket.close()
        print(f"[*] File {filename} received from {address[0]}:{address[1]}")
        print(f"[*] File saved as {new_filename}")


def send_multiple_files(host, port):
    while True:
        folder = input("Enter folder name containing files to send: ")
        try:
            file_list = os.listdir(folder)
            break
        except FileNotFoundError:
            print(f"[!] Folder '{folder}' not found. Try again.")

    for filename in file_list:
        full_path = os.path.join(folder, filename)
        if os.path.isfile(full_path):
            send_file(full_path, host, port)

    print("[+] All files sent successfully.")


if __name__ == "__main__":
    print("Choose an option:")
    print("1. Send a file")
    print("2. Receive a file")
    print("3. Send multiple files")

    option = int(input("Enter option number: "))
    host = input("Enter IP address to connect to: ")
    port = int(input("Enter port number to connect to: "))

    if option == 1:
        filename = input("Enter filename to send: ")
        send_file(filename, host, port)
    elif option == 2:
        receive_file(host, port)
    elif option == 3:
        send_multiple_files(host, port)
    else:
        print("Invalid option. Program will exit.")
