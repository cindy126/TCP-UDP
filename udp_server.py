import subprocess
import socket
import sys
import os

PORT = 3000

#Create socket instance with address family ip4 and UDP protocol
s = socket.socket(socket.AP_INET, socket.SOCK_DGRAM)

# Bind socket to any machine & port 3000
s.bind(('', PORT))

while True:
    bigmac, addr = s.recvfrom(1024)
    #Receive command with buffer size 1024
    data, addr = s.recvfrom(1024)
    try:
        s.settimeout(0.5)
        cmd, addr = s.recvfrom(1024)
        while(int(data.decode('utf-8')) != len(cmd.decod('utf-8'))):
            cmd, addr = s.recvfrom(1024)
        s.sendto("ACK".encode('utf-8'), addr)
        s.settimeout(None)
    except socket.timeout:
        print("Failed to receive instructions from the client.")
        s.settimeout(None)
        continue

    #Get command and place output in output.txt
    temp = cmd.decode("utf-8").split(" > ")
    command = temp[0] + " > output.txt"

    #Run command using a shell - ensure errors are caught
    try:
        out = subprocess.check_output(command, shell=True)
    #Any error will mean the command did not execute successfully - send a no response message to client signifying the command failed
    except subprocess.CalledProcessError as grepexc:
        s.sendto(str(len("Did not receive response.")).encode('utf-8'), addr)
        s.sendto("Did not receive response.".encode('utf-8'), addr)
        continue

    #Open files that command's output was stored in
    f = open("output.txt", 'r')
    l = f.read(1024)

    s.sendto((str(os.path.getsize("output.txt"))).encode('utf-8'), addr)

    flag = False
    #read output back to client(potential multiple segments if size(line)> 1024)
    while(l):
        i = 0
        while(i < 3):
            try:
                # send length of message
                length = (str(len(l)).encode('utf-8'))
                s.sendto(length, addr)
                # send actual message
                s.sendto(l.encode('utf-8'), addr)
                s.settimeout(1)
                resp, addr = s.recvfrom(1024)
                #wait for ACK
                while(resp.decode('utf-8') != "ACK"):
                    resp,addr = s.recvfrom(1024)
                s.settimeout(None)
                break
            except socket.timeout:
                s.settimeout(None)
            i+=1
        if(i == 3):
            print("File transmission failed.")
            flag = True
            break
        l = f.read(1024)
    if flag:
        continue
    #Tell client finished reading and shutdown the socket
    print("Successful File Transmission")
        
