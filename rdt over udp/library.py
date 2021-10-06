import random
import time
import sys
from socket import*
import uuid
timeout = 2

def rdt_packet(message, seq_no,ID):
	if type(message) == int:
		msg = str(message)
	else:#list of numbers
		msg = ":".join(str(x) for x in message)
	pckt = str(seq_no)+'/'+str(len(msg))+'/'+msg
	#ID
	packet_ = ID +'/'+pckt
	#print(pckt)
	return packet_
	
def udt_packet(message, ID, seq_no):
	pack = ID+'/'+seq_no+'/'+str(message)
	#print(pack, type(pack))
	return pack
		
def rdtsend(sock,server,message, prob,seq_no,ID):
	pack = rdt_packet(message, seq_no,ID)
	sock.settimeout(timeout)
	r = round(random.random(),2)
	if r <= prob:#else drop packet
		#random delay
		t = random.uniform(0.5, 2.5)
		time.sleep(t)
		sock.sendto(pack.encode(), server)
	return
				
def rdtrecv(sock,server,message, prob,seq_no, ID):
	ID_ = 0
	seq_ = -1
	while True:
		try:
			while ID != ID_ or seq_no != seq_:#prevents duplicates
				message, serverAddress = sock.recvfrom(2048);
				message = message.decode()
				ID_ = message.split('/',1)[0]#ID
				x = message.split('/',1)[1]
				seq_ = int(x.split('/',1)[0])
				message = x.split('/',1)[1]
			break
		except Exception as e:#timeout
			print("Dropped packet ",seq_no,", ID: ", ID)
			m = "Timeout packet "+str(seq_no)+", ID: "+ID
			sock.sendto(m.encode(), server)
			#retransmitting
			print("Retransmitting packet ", seq_no,", ID: ", ID)
			rdtsend(sock,server,message, prob,seq_no, ID)
			message = rdtrecv(sock,server,message, prob,seq_no, ID)
			break	
	return message

def udtrecv(s):
	while True:
		message, clientAddress =  s.recvfrom(2048)
		message = message.decode()
		try:
			ID = message.split('/',1)[0]#ID
			x = message.split('/',1)[1]	
			seq_no = x.split('/',1)[0]#seq_no
			x = x.split('/',1)[1]	
			length = x.split('/',1)[0]
			data = x.split('/',1)[1]
			return message,clientAddress,ID,seq_no,data
		except:
			print(message)
    	
def udtsend(s, clientAddress,message, prob):
	r = round(random.random(),2)
	if r <= prob:#else drop packet
		#random delay
		t = random.uniform(0.5, 2.5)
		time.sleep(t)
		s.sendto(message.encode(), clientAddress)
	return
