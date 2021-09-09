#!/usr/bin/python
from socket import *
from threading import Thread
import sys
users = []
connt = []

#broadcast to all clients
def broadcast(sentence):
	print(sentence)
	for i in connt:
		i.send(sentence.encode())
		
#get message from client
def receive_message_client(connectionSocket,addr):
	while True:
		sentence = connectionSocket.recv(1024).decode()
		if sentence:
			index = connt.index(connectionSocket)
			sentence = users[index]+" : "+ sentence
			broadcast(sentence)
		
def main():
	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverName = '127.0.0.1'
	serverPort = int(sys.argv[1])
	serverSocket.bind((serverName, serverPort))
	serverSocket.listen()
	print("Chat Room opened!!")
	while True:
		connectionSocket, addr = serverSocket.accept()
		username = connectionSocket.recv(1024).decode()
		users.append(username)
		connt.append(connectionSocket)
		broadcast(username + " joined the chatroom!!")
		th = Thread(target = receive_message_client, args = (connectionSocket, addr))
		th.start()


if __name__ == "__main__":
	main()
	connectionSocket.close()
	serverSocket.close()
