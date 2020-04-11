import socket
import sys

while True:
    # enter server name or IP address
    udp_IP = input("Enter server name or IP address: ")
    try:
        socket.inet_aton(str(udp_IP))
        break
    except socket.error:
        # OSError
        print("Could not connect to server.")

while True:
    # enter port + check if it's a port
    try:
        udp_PORT = int(input("Enter port: "))
        if udp_PORT < 0 or udp_PORT > 66535:
            raise ValueError
        break
    except Exception:
        print("Invalid port number.")
    except ValueError:
        print("Invalid port number.")

# enter command
command = input("Enter command: ")

BUFFER_SIZE = 1024


if command.find(" > ") == -1:
    command = command + " > " + command + ".txt"
# get filename
x = command.split(" > ")
filename = x[1]

# udp socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for i in range(4):
    if i == 3:
        # closing connection if failed by the 3rd time
        print("Failed to send command. Terminating.")
        sys.exit()
    try:
        # send length 
        length_command = str(len(command))
        clientSocket.sendto(length_command.encode(), (udp_IP, udp_PORT))
        # send command
        clientSocket.sendto(command.encode(), (udp_IP, udp_PORT))
        
        clientSocket.settimeout(1) # wait 1 second
        modifiedMessage, serverAddress = clientSocket.recvfrom(BUFFER_SIZE)
        
        if (modifiedMessage.decode() == "ACK"):
            break
            clientSocket.setblocking(True)
    except socket.timeout:
        if i < 2:
            print("Did not receive response.")
        pass
    clientSocket.setblocking(True)


# get size of file
fileLength, serverAddress = clientSocket.recvfrom(BUFFER_SIZE)
fileLength = int(fileLength.decode())


# get length
dataLength, serverAddress = clientSocket.recvfrom(BUFFER_SIZE)
# get message
data, serverAddress = clientSocket.recvfrom(BUFFER_SIZE)
x = int(dataLength.decode())

writeFile = open(filename, 'w')
writeFile.write(data.decode())

# send "ACK"
clientSocket.sendto("ACK".encode(), serverAddress)

# loop to all messages go through
while(fileLength != (int(dataLength.decode()))):
    try:
        # get length
        dataLength, serverAddress = clientSocket.recvfrom(BUFFER_SIZE)
        clientSocket.settimeout(0.5)
        # get message
        data, serverAddress = clientSocket.recvfrom(BUFFER_SIZE)
        
        if(int(dataLength.decode()) != len(data.decode())):
            clientSocket.sendto("Did not receive response. ".encode(), (udp_IP, udp_PORT))
        
        clientSocket.sendto("ACK".encode(), (udp_IP, udp_PORT))
        clientSocket.settimeout(None)
    except socket.timeout:
        print("Did not receive response.")
        clientSocket.settimeout(None)
        sys.exit()

    writeFile.write(data.decode())
    x += int(dataLength.decode())

writeFile.close()
clientSocket.close()

print ("File", filename, "saved.")
