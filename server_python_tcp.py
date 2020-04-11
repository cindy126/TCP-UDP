import socket
import sys
import subprocess

tcp_IP = ''
tcp_PORT = int(sys.argv[1])

BUFFER_SIZE = 1024

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((tcp_IP, tcp_PORT))
serverSocket.listen()

while(True):
    connectionSocket, addr = serverSocket.accept()
    command = connectionSocket.recv(BUFFER_SIZE)

    x = command.decode().split(" > ")
    text = x[0] + " > output.txt"
    
    '''
    # Run command using a shell - ensure errors are caught
    try:
        out = subprocess.check_output(text, shell=True)
    #Any error will mean the command did not execute successfully - send a no response message to client signifying the command failed
    except subprocess.CalledProcessError as grepexc:
        connectionSocket.send("Did not receive response.".encode())
        continue
    '''
    readFile = open("output.txt", 'r')
    r = readFile.read(BUFFER_SIZE)
    while(r):
        try:
            connectionSocket.send(r.encode())
            r = readFile.read(BUFFER_SIZE)
        except socket.timeout:
            connectionSocket.send("Did not receive response.".encode())
            continue


    print("Successful File Transmission")

    connectionSocket.close()
serverSocket.close()