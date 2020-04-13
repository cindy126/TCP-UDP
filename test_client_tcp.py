import socket
import server_python_tcp
import client_python_tcp
import threading
import queue
import unittest

# global value for client and server functions
serverPort = 3500
BUFFER_SIZE = 1024


def normalServer():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(('', serverPort))
    serverSocket.listen()
    connectionSocket, addr = serverSocket.accept()
    server_python_tcp.fileTransmission(connectionSocket)

def mockServer():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(('', serverPort))
    serverSocket.listen()
    connectionSocket, addr = serverSocket.accept()
    command = connectionSocket.recv(BUFFER_SIZE)


# Establish unit test cases
class Test_Client_TCP(unittest.TestCase):
    # Case 1: "File debugOutput.txt saved."
    def test_case1(self):
        # Start server thread
        t = threading.Thread(target=normalServer)
        t.start()
        # Use functions in client source code to do normal operation
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_python_tcp.checkConnection(clientSocket, "localhost", serverPort)
        rc = client_python_tcp.getCommandAndData(clientSocket, "ls > debugOutput.txt") 
        self.assertEqual(rc, "File debugOutput.txt saved.")
        # Check server function return value
        t.join(5.0)
        self.assertFalse(t.is_alive())      # Server thread should have completed   

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
        # Start server thread
        t = threading.Thread(target=mockServer)
        t.start()
        # Use functions in client source code to do normal operation
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_python_tcp.checkConnection(clientSocket, "localhost", serverPort)
        rc = client_python_tcp.getCommandAndData(clientSocket, "ls > debugOutput.txt") 
        self.assertEqual(rc, "Did not receive response.")
        # Check server function return value
        t.join(5.0)
        self.assertFalse(t.is_alive())      # Server thread should have completed   


if __name__ == '__main__':
    unittest.main()
















'''
import socket
import sys
import subprocess
import unittest
from unittest.mock import Mock
from client_python_tcp import checkIP, checkPort, connection, getCommand

class Test_Client_TCP(unittest.TestCase):

    def test_checkIP(self):
        self.assertTrue(checkIP('127.0.0.1'))
        self.assertFalse(checkIP('fakeIP'))
        self.assertFalse(checkIP('500.500.500.500'))

    def test_checkPort(self):
        self.assertTrue(checkPort(3300))
        self.assertFalse(checkPort(1000000000))
        self.assertFalse(checkPort('fakePort'))
    
    def test_connection(self):
        # create mock object
        mock = Mock()
        IP = "127.0.0.1"
        PORT = 3300
        # successful connection
        self.assertTrue(connection(IP, PORT, mock))
        # unsuccessful connection
        mock.connect.side_effect = Mock(side_effect = Exception)
        self.assertFalse(connection(IP, PORT, socket))
    
    def test_getCommand(self):
        # creat mock object
        mock = Mock()

        # error
        mock.recv.side_effect = [(b"Did not receive response.")]
        self.assertFalse(getCommand(mock, "Did not receive response."))
        
        # correct file name
        mock.recv.side_effect = [b"correct data sent"]
        self.assertTrue(getCommand(mock, "ls > ls.txt"))
        


if __name__ == '__main__':
    unittest.main()
'''
