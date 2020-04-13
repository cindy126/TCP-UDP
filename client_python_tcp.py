import socket
import sys

def checkConnection(clientSocket, tcpIP, tcpPort):
    # check if port is in number range (if valid)
    if tcpPort < 0 or tcpPort > 65535:
        return "Invalid port number."
    try:
        # try connection
        clientSocket.connect((tcpIP,tcpPort))
        return "OK"
    except Exception:
        return "Could not connect to server."

def getCommandAndData(clientSocket, command):
    # same for server and client
    BUFFER_SIZE = 1024
    
    clientSocket.send(command.encode())
    # get command
    data = clientSocket.recv(BUFFER_SIZE)
    

     # if response to the command was not successfully received
    error = data.decode()
    if len(error) == 0:
        return "Did not receive response."
    if error == "Did not receive response.":
        return "Did not receive response."

    # get filename
    x = command.split(" > ")
    filename = x[1]

    # write file
    writeFile = open(filename, 'w')
    writeFile.write(data.decode())
    writeFile.close()

    return "File {0} saved.".format(filename)
    


def main():
    # enter server name or IP address
    tcp_IP = str(input("Enter server name or IP address: "))

    # enter PORT
    tcp_PORT = int(input("Enter port: "))
  
    # make tcp socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    results = checkConnection(clientSocket, tcp_IP, tcp_PORT)
    if(results != 'OK'):
        print(results)
        return

    # enter command
    command = input("Enter command: ")

    results = getCommandAndData(clientSocket, command)
    if(results == "Did not receive response."):
        print(results)
        return
    
    print (results)

    clientSocket.close()

 
if __name__ == '__main__':
    main()
