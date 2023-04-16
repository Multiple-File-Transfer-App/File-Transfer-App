UGA torrent

This Project Implements -
1. Bit torrent Protocol : 
    --- Where a client can download a file from multiple peers [The client gets different parts of the file from multiple peers]. 
    --- The code keeps track of the amount of the file downloaded, Download speed, Upload speed and the number of peers using a UDP tracker.
    --- To start the download client has to specify the .torrent file name as an input [ Here we have taken winrar.torrent as an example and it is available in the root folder ]
    --- When the client enters the .torrent file name the download starts by displaying all the details and waits for the peers to send their part of the file.
    --- Once the download is done we can see the downloaded folder/file in the root folder.

2. Single Peer Transfer -
    --- Here the client gets the required file from a single peer [ i.e the entire file comes from one peer ]
    --- When the client selects this option they are requested to give the name of the file they want and then it waits for the sender to send the file.
    --- Once the sender sends the file the download starts at the client side and we can see the downloaded file at the client side.

3. Encrypted Download -
    --- The code automatically encrypts and decrypts at sender and recevier side respectively.

4. UDP Tracker - 
    --- The tracker tracks the following and shows them in a progress bar - Download percentage, download speed, upload speed and the number of peers.

5. Security -
    --- Every client must login/register before downloading or sending a file.


steps to run the code -

First run - pip install -r requirements.txt  - This installs all the required packages for the Project

Then run server -  python server/server.py

Now open a new terminal and run client - python client.py 

Or Run makefile in 2 terminals [ one for server and one for client respectively ].


The client has to login first - You can find the already registered clients in login_cred.txt in server folder.
--- A new client can register to the server by selecting the (2) register option after running the client.py
--- After the client logsin they are given 2 options - i. To download the file from multiple peers ii. To download the file from a single peer [ for single peer for example please use ip - 127.0.0.1 and port no - 65432 and for .torrent file please use winrar.torrent as an example.
--- After the client make an selection the name of the file is taken as the input from the client and then the download starts.