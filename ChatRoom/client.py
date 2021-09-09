#!/usr/bin/python
from socket import *
import sys
from threading import Thread

serverName = '127.0.0.1'
serverPort = int(sys.argv[1])
clientSocket = socket(AF_INET, SOCK_STREAM)

username = str(sys.argv[2])

clientSocket.connect((serverName, serverPort))
#print(username," joined the chat room");
#send username
clientSocket.send(username.encode())
print(clientSocket.recv(1024).decode())

#sending messages to server
def sending(clientSocket):
	while True:
		sentence = input()
		clientSocket.send(sentence.encode())
		

while True:
	th1 = Thread(target = sending, args = (clientSocket,))
	th1.start()
	#receiving message from server
	while True:
		sentence = clientSocket.recv(1024).decode()
		print(sentence)
	

clientSocket.close()
print(username," left the chat room");
