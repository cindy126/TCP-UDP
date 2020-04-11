import socket
import subprocess
import sys
import os

udp_IP = ''
udp_PORT = int(sys.argv[1])

BUFFER_SIZE = 1024
# create udp sockert
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((udp_IP, udp_PORT))

while True:
    # get length command 
    length_command, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
    try:
        serverSocket.settimeout(0.5) # waits 0.5 seconds
        # get command
        command, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
        print ("test")
        if(int(length_command.decode()) != len(command.decode())):
            serverSocket.sendto("Failed to receive instructions from the client.".encode(), clientAddress)
        else:
            serverSocket.sendto("ACK".encode(), clientAddress)  
        serverSocket.setblocking(True)
        
    except socket.timeout:
        print("Failed to receive instructions from the client.")
        serverSocket.setblocking(True)
        continue
    
    x = command.decode().split(" > ")
    text = x[0] + " > output.txt"

    # open files
    readFile = open("output.txt", 'r')
    r = readFile.read(BUFFER_SIZE)

    # size of file + send size of file to client
    size = os.path.getsize("output.txt")
    serverSocket.sendto((str(size)).encode(), clientAddress)

    # send messages containing the output one by one
    while(r):
        for i in range(4):
            if(i == 3):
                print("File transmission failed.")
                break
            try:
                # send length
                length_file = (str(len(r)).encode())
                serverSocket.sendto(length_file, clientAddress)
                
                # send message
                serverSocket.sendto(r.encode(), clientAddress)
                serverSocket.settimeout(1)
                
                # get "ACK"
                modifiedMessage, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
              
                while(modifiedMessage.decode() != "ACK"):
                    modifiedMessage,clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
                serverSocket.setblocking(True)
                break
            except socket.timeout:
                serverSocket.setblocking(True)
        r = readFile.read(BUFFER_SIZE)
        

    print("Successful File Transmission")