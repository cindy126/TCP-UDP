'''
I did not specifically copy code from anywhere; however, I used the links below 
and the textbook to learn about TCP socket programming in Python.

https://wiki.python.org/moin/TcpCommunication
https://www.geeksforgeeks.org/socket-programming-python/
https://docs.python.org/3/library/socket.html#socket.socket.setblocking

Textbook: J. Kurose and K. Ross, “Computer Networking: A Top-Down Approach Featuring the Internet”, 
Addison-Wesley, 7th Edition (May 2016). Pages: 202-205.
'''
import socket
import sys
import subprocess

def fileTransmission(connectionSocket):
    # same for server and client
    BUFFER_SIZE = 1024

    command = connectionSocket.recv(BUFFER_SIZE)

    text = (command.decode().split(" > "))[0] + " > syslog.txt"

    # check if error
    try:
        # run output
        subprocess.run(text, shell=True)
    except subprocess.CalledProcessError:
        # error
        connectionSocket.send("Did not receive response.".encode())
        return "Error."

    readFile = open("syslog.txt", 'r')
    r = readFile.read(BUFFER_SIZE)
    
    # if r is true, keep on reading file and sending
    try:
        while(r):
            connectionSocket.send(r.encode())
            r = readFile.read(BUFFER_SIZE)
    except Exception:
        readFile.close()
        connectionSocket.close()
        return "Error."

    # close socket connection
    connectionSocket.close()

    # successful file transmission
    return "Successful file transmission."

def main():
    tcp_IP = ''
    tcp_PORT = int(sys.argv[1])

    # create socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((tcp_IP, tcp_PORT))

    serverSocket.listen()


    while(True):
        connectionSocket, addr = serverSocket.accept()
        print (fileTransmission(connectionSocket))

    serverSocket.close()

if __name__ == '__main__':
    main()
