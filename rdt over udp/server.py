#!/usr/bin/python
from library import*
server =('127.0.0.1', 12000)
s = socket(AF_INET, SOCK_DGRAM)
s.bind(server);
prob = float(sys.argv[1])
	
while True:
	packet,addr,ID,seq_no,data = udtrecv(s)
	sum = 0
	while True:
		try:
			sum += int(data.split(':',1)[0])
			data = data.split(':',1)[1]
		except:
			break
	pack = udt_packet(sum, ID,seq_no)
	udtsend(s, addr,pack, prob)
s.close()	
