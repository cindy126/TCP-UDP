import socket
import server_python_tcp
import client_python_tcp
import threading
import queue
import unittest
import time

# global calue for client and server functions
serverPort= 3500

# separate thread for server function
def threadServer(returnQue):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(('', serverPort))
    serverSocket.listen()
    connectionSocket, addr = serverSocket.accept()
    returnValue = server_python_tcp.fileTransmission(connectionSocket)
    serverSocket.close()
    returnQue.put(returnValue)


# unit test cases

class Test_Server_TCP(unittest.TestCase):

    # Case 1: "Successful file transmission"
    def test_case1(self):
        # start server thread
        que = queue.Queue()
        t = threading.Thread(target=threadServer, args=(que,))
        t.start()
        time.sleep(1)
        # Use functions in client source code to do normal operation
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_python_tcp.checkConnection(clientSocket, "localhost", serverPort)
        client_python_tcp.getCommandAndData(clientSocket, "ls > debugOutput.txt")    
        # Check server function return value
        t.join(5.0)
        self.assertFalse(t.is_alive())      # Server thread should have completed   
        self.assertEqual(que.get(), "Successful file transmission.")

if __name__ == '__main__':
    unittest.main()













'''
class Test_Server_TCP(unittest.TestCase):
    
    def test_fileTransmission(self):
        mock = Mock()

        # correct file
        self.assertTrue(fileTransmission(mock))

        # error file
        mock.send.side_effect = Exception
        self.assertFalse(fileTransmission(mock))       


if __name__ == '__main__':
    unittest.main()
'''