'''
I did not specifically copy code from anywhere; however, I used the links below 
and the textbook to learn about UDP socket programming in Python.

https://www.geeksforgeeks.org/socket-programming-python/
https://docs.python.org/3/library/socket.html#socket.socket.setblocking

Textbook: J. Kurose and K. Ross, “Computer Networking: A Top-Down Approach Featuring the Internet”, 
Addison-Wesley, 7th Edition (May 2016). Pages: 194-199 & 202-205.
'''
import socket
import sys

# same for server and client
BUFFER_SIZE = 1024

def checkConnection(clientSocket, udpIP, udpPort):
    # check if port is in number range (if valid)
    if udpPort < 0 or udpPort > 65535:
        return "Invalid port number."
    try:
        # send "Ping" to UDP port to see if it succeeds
        if(clientSocket.sendto("Ping".encode(), (udpIP, udpPort)) == 0):
            return "Could not connect to server."
        return "OK"
    except:
        return "Could not connect to server."

def sendCommand(clientSocket, udpIP, udpPort, command):
    for i in range(4):
        try:
            # send length
            length_command = str(len(command))
            clientSocket.sendto(length_command.encode(), (udpIP, udpPort))
            # send command
            clientSocket.sendto(command.encode(), (udpIP, udpPort))
            
            clientSocket.settimeout(1) # wait 1 second
            response, serverAddress = clientSocket.recvfrom(BUFFER_SIZE)
            
            if (response.decode() == "ACK"):
                return "OK"
            clientSocket.setblocking(True)         
        except socket.timeout:
            # retry
            continue  
    
    # failed 3 times, return failure message
    return "Failed to send command. Terminating."


def receiveDataToFile(clientSocket, filename):
    # set long timeout to allow server exec command
    clientSocket.settimeout(3)      

    try:
        # get size of file
        fileLength, serverAddress = clientSocket.recvfrom(BUFFER_SIZE)
        lengthToGet = int(fileLength.decode())
        # open file for writing
        with open(filename, 'w') as writeFile:
            while (lengthToGet > 0):
                # get data
                data, serverAddress = clientSocket.recvfrom(BUFFER_SIZE)
                if(lengthToGet > BUFFER_SIZE):
                    # respond with ACK first and then wait for next block
                    clientSocket.sendto("ACK".encode(), serverAddress)
                    lengthToGet = lengthToGet - writeFile.write(data.decode())
                else:
                    if(lengthToGet == len(data.decode())):
                        # last block of data; respond with ACK
                        clientSocket.sendto("ACK".encode(), serverAddress)
                        writeFile.write(data.decode())
                        return "File {0} saved.".format(filename)
        return "Incorrect transmission size"    # size calculation is wrong somewhere
    except socket.timeout:
        return "Did not receive response."
    except ValueError:
        return "Protocol error"

def main():
    # enter server name or IP address
    udp_IP = str(input("Enter server name or IP address: "))

    # enter PORT
    udp_PORT = int(input("Enter port: "))
      
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    results = checkConnection(clientSocket, udp_IP, udp_PORT)
    if(results != 'OK'):
        print(results)
        return

    command = input("Enter command: ")

    results = sendCommand(clientSocket, udp_IP, udp_PORT, command)
    if(results != 'OK'):
        print(results)
        return
  
    filename = (command.split(" > "))[1]
    print(receiveDataToFile(clientSocket, filename))
 
if __name__ == '__main__':
    main()