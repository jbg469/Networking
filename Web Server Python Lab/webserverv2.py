#import socket module
from socket import *
import sys # In order to terminate the program

def main():
    port=13331
    serverSocket = socket(AF_INET, SOCK_STREAM)

    #Prepare a sever socket
    serverSocket.bind(("localhost", port))
    serverSocket.listen(1)

    while True:
        #Establish the connection
        print("Ready to serve on port:", port)
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(1024)
            print("message:", message)
            filename = message.split()[1] #HTTP path 
            f = open(filename[1:])
            outputdata =f.read()
           #Send one HTTP header line into socket
            connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
            #Send the content of the requested file to the client
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
        except IOError:
            #Send response message for file not found (404)
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
            connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
            #Close client socket
            connectionSocket.close()

    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
    main()
