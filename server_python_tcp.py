import socket
import sys
import subprocess

def fileTransmission(connectionSocket):
    BUFFER_SIZE = 1024

    command = connectionSocket.recv(BUFFER_SIZE)

    text = (command.decode().split(" > "))[0] + " > syslog.txt"

    try:
        subprocess.run(text, shell=True)
    except subprocess.CalledProcessError:
        connectionSocket.sendto("Did not receive response.".encode())
        return "Error."

    readFile = open("syslog.txt", 'r')
    r = readFile.read(BUFFER_SIZE)
    try:
        while(r):
            connectionSocket.send(r.encode())
            r = readFile.read(BUFFER_SIZE)
    except Exception:
        readFile.close()
        connectionSocket.close()
        return "Error."
    connectionSocket.close()
    return "Successful file transmission."

def main():
    tcp_IP = ''
    tcp_PORT = int(sys.argv[1])

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((tcp_IP, tcp_PORT))

    serverSocket.listen()


    while(True):
        connectionSocket, addr = serverSocket.accept()
        '''
        command = connectionSocket.recv(BUFFER_SIZE)

        text = (command.decode().split(" > "))[0] + " > syslog.txt"

        try:
            subprocess.run(text, shell=True)
        except subprocess.CalledProcessError:
            connectionSocket.sendto("Did not receive response.".encode())
            continue
        '''
        print (fileTransmission(connectionSocket))

    serverSocket.close()

if __name__ == '__main__':
    main()
