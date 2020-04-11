import socket
import sys

while True:
    # enter server name or IP address
    tcp_IP = input("Enter server name or IP address: ")
    try:
        socket.inet_aton(str(tcp_IP))
        break
    except socket.error:
        # OSError
        print("Could not connect to server.")

while True:
    # enter port + check if it's a port
    try:
        tcp_PORT = int(input("Enter port: "))
        if tcp_PORT < 0 or tcp_PORT > 66535:
            raise ValueError
        break
    except Exception:
        print("Invalid port number.")
    except ValueError:
        print("Invalid port number.")

# enter command
command = input("Enter command: ")

BUFFER_SIZE = 1024

# tcp connection
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# test connection
try:
    clientSocket.connect((tcp_IP,tcp_PORT))
except Exception:
    # exit if cannot connect
    print("Could not connect to server.")
    sys.exit()

# find command
if command.find(" > ") == -1:
    command = command + " > " + command + ".txt"

# get command
clientSocket.send(command.encode())
data = clientSocket.recv(BUFFER_SIZE)

# if response to the command was not successfully received
error = data.decode()
if error == "Did not receive response.":
    print("Did not receive response.")


# get filename
x = command.split(" > ")
filename = x[1]

# write file
writeFile = open(filename, 'w')
writeFile.write(data.decode())
writeFile.close()

print ("File", filename, "saved.")

clientSocket.close()

