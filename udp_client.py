import socket
import sys

while True:
    # take IP as input
    IP = input("Enter server name or IP addres: ")
    # Validate IP in family ipV4
    try:
        socket.inet_aton(IP)
        break
    except socket.error:
        print("Could not connect to server.")

while True:
    # Take port # as input
    #Check that it's integer
    try:
        port = int(input("Enter port: "))
        while port < 0 or port > 66535:
            print("Invalid port number.")
        break
    except Exception:
        print("Invalid port number.")
'''
# Check valid port number
while port < 0 or port > 66535:
    print("Invalid port number.")
    while True:
        # Ensure inputted port is integer
        try:
            port = int(input("Enter port: "))
            break
        except Exception:
            print("Invalid port number.")
'''

# Input Command
command = input("Enter command: ")

if command.find(" > ") == -1:
    command = command + " > " + command + ".txt"

temp = command.split(" > ")
filename = temp[1]

#Make UDP Socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

addr = (IP, port)

#Test if connection successful
try: 
    s.sendto("bigmac".encode(), addr)
except:
    print("Could not connect to server")
    sys.exit()

# Tries to send command
for i in range(4):
    if i == 3:
        print("Failed to send command. Terminating")
        sys.exit()
    try:
        s.sendto((str(len(command))).encode(), addr)
        s.sendto(command.encode(), addr)
        s.settimeout(1)
        resp, addr = s.recvfrom(1024)
        while(resp.decode() != "ACK"):
            resp, addr = s.recvfrom(1024)
        s.settimeout(None)
        break
    except socket.timeout:
        pass
    s.settimeout(None)

# Receives response
total_length, addr = s.recvfrom(1024)
print(total_length.decode())

if total_length.decode() == "Did not receive response.":
    print("Did not receive response.")
    sys.exit()

total_length = int(total_length.decode())
length, addr = s.recvfrom(1024)
l, addr = s.recvfrom(1024)

f = open(filename, 'w')
f.write(l.decode())
counting_length = int(length.decode())

s.sendto("ACK".encode(), addr)

while(total_length != counting_length):
    try:
        length, addr = s.recvfrom(1024)
        s.settimeout(0.5)
        l, addr = s.recvfrom(1024)
        while(int(length.decode()) != len(l.decode())):
            l, addr = s.recvfrom(1024)
        s.sendto("ACK".encode(), addr)
        s.settimeout(None)
    except socket.timeout:
        print("Did not receive response.")
        s.settimeout(None)
        sys.exit()
    f.write(l.decode())
    counting_length += int(length.decode())
f.close()
s.close()

print("File ", filename, " saved.")
