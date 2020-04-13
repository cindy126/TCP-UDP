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












'''
def checkIP(tcp_IP):
    try:
        socket.inet_aton(str(tcp_IP))
        return True
    except socket.error:
        # OSError
        print("Could not connect to server.")
        return False

def checkPort(tcp_port):
    # enter port + check if it's a port
    try:
        tcp_PORT = int(tcp_port)
        if tcp_PORT < 0 or tcp_PORT > 66535:
            raise ValueError
        return True
    except Exception:
        print("Invalid port number.")
        return False
    except ValueError:
        print("Invalid port number.")
        return False

def connection(tcp_IP, tcp_PORT, clientSocket):
    # test connection
    try:
        clientSocket.connect((tcp_IP,tcp_PORT))
        return True
    except Exception:
        # exit if cannot connect
        print("Could not connect to server.")
        return False

def getCommand(clientSocket, command):
    BUFFER_SIZE = 1024
    
    clientSocket.send(command.encode())
    # get command
    data = clientSocket.recv(BUFFER_SIZE)

     # if response to the command was not successfully received
    error = data.decode()
    if error == "Did not receive response.":
        print("Did not receive response.")
        return False

    # get filename
    x = command.split(" > ")
    filename = x[1]

    # write file
    writeFile = open(filename, 'w')
    writeFile.write(data.decode())
    writeFile.close()

    print ("File", filename, "saved.")
    
    clientSocket.close()
    return True
    
   

def main():
    while True:
        # enter server name or IP address
        tcp_IP = input("Enter server name or IP address: ")
        if checkIP(tcp_IP) == True:
            break
        
    while True:
        tcp_PORT = int(input("Enter port: "))
        if checkPort(tcp_PORT) == True:
            break

    # enter command
    command = input("Enter command: ")
    BUFFER_SIZE = 1024
    # tcp connection
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if not connection(tcp_IP,tcp_PORT, clientSocket):
        sys.exit()
    

    if not getCommand(clientSocket, command):
        clientSocket.close()

if __name__ == '__main__':
    main()
'''
