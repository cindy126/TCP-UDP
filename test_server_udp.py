import socket
import server_python_udp
import client_python_udp
import threading
import queue
import unittest

# global value for client and server functions
serverPort = 3500       

# separate thread for server function
def threadServer(returnQue):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    returnValue = server_python_udp.listenAndRespond(serverSocket)
    returnQue.put(returnValue)

# unit test cases

class Test_Server_UDP(unittest.TestCase):

    # Case 1: "Successful file transmission"
    def test_case1(self):
        # start server thread
        que = queue.Queue()
        t = threading.Thread(target=threadServer, args=(que,))
        t.start()
        # Use functions in client source code to do normal operation
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_python_udp.sendCommand(clientSocket, "localhost", serverPort, "ls")
        client_python_udp.receiveDataToFile(clientSocket, "debugOutput.txt")    
        # Check server function return value
        t.join(5.0)
        self.assertFalse(t.is_alive())      # Server thread should have completed   
        self.assertEqual(que.get(), "Successful file transmission.")

    # Case 2: "Failed to receive instructions from the client."
    def test_case2(self):
        # Start server thread
        que = queue.Queue()
        t = threading.Thread(target=threadServer, args=(que,))
        t.start()
        # Send incorrect command length from client to server
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        command = "ls"
        length_command = str(len(command) + 2)      # make command length incorrect
        clientSocket.sendto(length_command.encode(), ("localhost", serverPort))
        clientSocket.sendto(command.encode(), ("localhost", serverPort))
        # Check server function return value
        t.join(5.0)
        self.assertFalse(t.is_alive())      # Server thread should have completed   
        self.assertEqual(que.get(), "Failed to receive instructions from the client.")

    # Case 3: "File transmission failed."
    def test_case3(self):
        # Start server thread
        que = queue.Queue()
        t = threading.Thread(target=threadServer, args=(que,))
        t.start()
        # Use functions in client source code to send command
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_python_udp.sendCommand(clientSocket, "localhost", serverPort, "ls")
        # Client does not respond to data
        
        # Check server function return value
        t.join(5.0)
        self.assertFalse(t.is_alive())      # Server thread should have completed   
        self.assertEqual(que.get(), "File transmission failed.")

if __name__ == '__main__':
    unittest.main()