import socket
import threading
import os
import datetime

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.server_thread = threading.Thread(target=self.start_server)

    def start_server(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        while True:
            conn, addr = self.sock.accept()
            self.connections.append(conn)
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

    def handle_client(self, conn, addr):
        file_data = b''
        while True:
            data = conn.recv(1024)
            if not data:
                break
            file_data += data
        conn.close()
        
        # Write received file to disk
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        file_name = f"received_file {current_time}"
        with open(file_name, "wb") as f:
            f.write(file_data)
        
        print(f"File received from {addr} and saved as {file_name}")

        # Broadcast to other peers
        for connection in self.connections:
            if connection != conn:
                connection.send(file_data)

    def start(self):
        self.server_thread.start()

def send_file():
    host = input("Enter the IP address of the peer you want to send the file to: ")
    port = int(input("Enter the port of the peer you want to send the file to: "))
    file_path = input("Enter the path of the file you want to send: ")
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            file_data = f.read()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.sendall(file_data)
        sock.close()
        print(f"File sent to {host}:{port}")
    else:
        print("File not found.")

if __name__ == "__main__":
    while True:
        print("Choose an option:")
        print("1. Send a file")
        print("2. Start peer-to-peer server")
        print("3. Quit")
        choice = input()
        if choice == "1":
            send_file()
        elif choice == "2":
            peer = Peer('', 12345)
            peer.start()
            print("Peer-to-peer server started.")
            input("Press Enter to continue...")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")
