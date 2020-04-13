import socket
import server_python_tcp
import client_python_tcp
import threading
import queue
import unittest

# global value for client and server functions
serverPort = 3500
BUFFER_SIZE = 1024

# set a separate thread as normal working server
def normalServer():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(('', serverPort))
    serverSocket.listen()
    connectionSocket, addr = serverSocket.accept()
    server_python_tcp.fileTransmission(connectionSocket)

# set a separate thread as mock server that does not execute command
def mockServer():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(('', serverPort))
    serverSocket.listen()
    connectionSocket, addr = serverSocket.accept()
    command = connectionSocket.recv(BUFFER_SIZE)


# unit test cases
class Test_Client_TCP(unittest.TestCase):
    # Case 1: "File debugOutput.txt saved."
    def test_case1(self):
        # start server thread
        t = threading.Thread(target=normalServer)
        t.start()
        # use functions in client source code to do normal operation
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_python_tcp.checkConnection(clientSocket, "localhost", serverPort)
        rc = client_python_tcp.getCommandAndData(clientSocket, "ls > debugOutput.txt") 
        self.assertEqual(rc, "File debugOutput.txt saved.")
        # check server function return value
        t.join(5.0)
        self.assertFalse(t.is_alive())      # server thread should have completed   

    # Case 2: "Invalid port number."
    def test_case2(self):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rc = client_python_tcp.checkConnection(clientSocket, "localhost", 99999)
        self.assertEqual(rc, "Invalid port number.")

    # Case 3: "Could not connect server."
    def test_case4(self):
        # this case may indicate wrong IP address
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rc = client_python_tcp.checkConnection(clientSocket, "gizmo.cs.ucsb.", 12321)
        self.assertEqual(rc, "Could not connect to server.")
        rc = client_python_tcp.checkConnection(clientSocket, "428.163.7.19", 12321)
        self.assertEqual(rc, "Could not connect to server.")
   
    # Case 4: "Did not receive response."
    def test_case5(self):
        # start server thread
        t = threading.Thread(target=mockServer)
        t.start()
        # use functions in client source code to do normal operation
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_python_tcp.checkConnection(clientSocket, "localhost", serverPort)
        rc = client_python_tcp.getCommandAndData(clientSocket, "ls > debugOutput.txt") 
        self.assertEqual(rc, "Did not receive response.")
        # check server function return value
        t.join(5.0)
        self.assertFalse(t.is_alive())      # server thread should have completed   


if __name__ == '__main__':
    unittest.main()
