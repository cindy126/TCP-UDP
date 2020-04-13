import socket
import subprocess
import sys
import os

# same for server and client
BUFFER_SIZE = 1024

# main loop of server
def listenAndRespond(serverSocket):
    # socket will wait for incoming data
    serverSocket.setblocking(True)
    try:
        # get length of command 
        length_command, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
        if(length_command.decode() == "Ping"):
            return "Ping Successful"
        if(int(length_command.decode()) <= 0):
            # invalid length
            return "Invalid Length"
    except ValueError:      # when first part of command is not number
        return "Protocol error"      

    try:
        serverSocket.settimeout(0.5) # waits 0.5 seconds
        # get command
        command, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
        if(int(length_command.decode()) != len(command.decode())):
            return "Failed to receive instructions from the client."
        # ACK to client
        serverSocket.sendto("ACK".encode(), clientAddress)  
    except socket.timeout:
        return "Failed to receive instructions from the client."

    # replace the output file name with "output.txt"
    x = command.decode().split(" > ")
    text = x[0] + " > output.txt" 
    try:     
        # run output
        subprocess.run(text, shell=True)
    except subprocess.CalledProcessError:
        return "Command process error"

    # size of file + send size of file to client
    size = os.path.getsize("output.txt")
    if(size <= 0):
        return "No output file"
    serverSocket.sendto((str(size)).encode(), clientAddress)

    # open file and sent data
    with open("output.txt", 'r') as readFile:
        read = readFile.read(BUFFER_SIZE)
        while(read):
            # try 3 times to transfer every block
            for i in range(4):
                if (i >= 3):    # failed after 3 attemps
                    return "File transmission failed."
                serverSocket.sendto(read.encode(), clientAddress) 
                # wait for ACK
                try:
                    clientResponse, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
                    if(clientResponse.decode() == "ACK"):
                        break
                except socket.timeout:
                    continue
            # read next block of file
            read = readFile.read(BUFFER_SIZE)  

    # file transmission completed
    return "Successful file transmission."


def main():
    udp_IP = '127.0.0.1'
    udp_PORT = int(sys.argv[1])
  
    # create udp socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind((udp_IP, udp_PORT))
    print("Starting server at UDP port {0}\n".format(udp_PORT))
    while True:
        print (listenAndRespond(serverSocket))

if __name__ == '__main__':
    main()
