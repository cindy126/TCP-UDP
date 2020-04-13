'''
I did not specifically copy code from anywhere; however, I used the link 
below to learn about unit testing in Python.

https://www.devdungeon.com/content/unit-testing-tcp-server-client-python

'''
import socket
import server_python_udp
import client_python_udp
import threading
import unittest

# global value for client and server functions
serverPort = 3500
BUFFER_SIZE = 1024

# set a separate thread as normal working server
def normalServer():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    server_python_udp.listenAndRespond(serverSocket)

# set a separate thread as mock server that does not execute command
def mockServer():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    serverSocket.setblocking(True)      # make sure socket will wait for incoming data
    length_command, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
    command, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
    serverSocket.sendto("ACK".encode(), clientAddress)  

# unit test cases
class Test_Client_UDP(unittest.TestCase):
    # Case 1: "File debugOutput.txt saved."
    def test_case1(self):
        # start server thread
        t = threading.Thread(target=normalServer)
        t.start()
        # use functions in client source code to do normal operation
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_python_udp.sendCommand(clientSocket, "localhost", serverPort, "ls")
        rc = client_python_udp.receiveDataToFile(clientSocket, "debugOutput.txt") 
        self.assertEqual(rc, "File debugOutput.txt saved.")
        # check server function return value
        t.join(5.0)
        self.assertFalse(t.is_alive())      # server thread should have completed   

    # Case 2: "Invalid port number."
    def test_case2(self):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rc = client_python_udp.checkConnection(clientSocket, "localhost", 99999)
        self.assertEqual(rc, "Invalid port number.")

    # Case 3: "Failed to send command. Terminating."
    def test_case3(self):
        # indicate server is not running
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rc = client_python_udp.sendCommand(clientSocket, "localhost", serverPort, "ls")
        self.assertEqual(rc, "Failed to send command. Terminating.")

    # Case 4: "Could not connect server."
    def test_case4(self):
        # indicate wrong IP address
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rc = client_python_udp.checkConnection(clientSocket, "gizmo.cs.ucsb.", 12321)
        self.assertEqual(rc, "Could not connect to server.")
        rc = client_python_udp.checkConnection(clientSocket, "428.163.7.19", 12321)
        self.assertEqual(rc, "Could not connect to server.")
   
    # Case 5: "Did not receive response."
    def test_case5(self):
        # start server thread
        t = threading.Thread(target=mockServer)
        t.start()
        # use functions in client source code to do normal operation
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_python_udp.sendCommand(clientSocket, "localhost", serverPort, "ls")
        rc = client_python_udp.receiveDataToFile(clientSocket, "debugOutput.txt") 
        self.assertEqual(rc, "Did not receive response.")
        # check server function return value
        t.join(5.0)
        self.assertFalse(t.is_alive())      # server thread should have completed   


if __name__ == '__main__':
    unittest.main()
