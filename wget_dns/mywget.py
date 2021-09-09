import sys
import struct
from socket import*
import os.path
from threading import Thread
import time
#the primary DNS server for Google DNS.
server = '8.8.8.8'
#DNS server runs on port 53
serverPort = 53 

#function to give filename, hostname and url
def getFileName_and_Url(hostname):
	url = ''
	#split and return a list with two element
	try:
		url = hostname.split('/',1)[1]
		hostname = hostname.split('/',1)[0]
	except:
		pass

	if(url != ''):
		try:
			filename = url.split('/',1)[1]
		except:
			filename = url
			pass
	else:
		filename = "index.html"
	#renaming file name if already exist
	i = 0
	filename_final = filename
	while(os.path.isfile(filename_final)):
		i += 1
		filename_final = filename+"["+str(i)+"]"
	return hostname, url, filename_final

def constructQuery(hostname):
	query = bytes("\x12\x12" + "\x00\x00" + "\x00\x01" + "\x00\x00" + "\x00\x00" + "\x00\x00", 'utf-8')
	d = bytes("", 'utf-8')

	for a in hostname.split('.'):
		d += struct.pack("!b" + str(len(a)) + "s", len(a), bytes(a, "utf-8"))

	query = query +  d +  bytes("\x00", 'utf-8') #terminate domain with zero len

	query = query + bytes("\x00\x01" + "\x00\x01", 'utf-8') #type A, class IN
	#print('query is', query)
	return query

def createConnection(query,hostname,url):
	flag = 0 #set to 1 if ip address not resolved
	sock = socket(AF_INET, SOCK_DGRAM)
	sock.sendto(query, (server, serverPort))
	reply, addr = sock.recvfrom(2048)
	#last 4 bytes contains ip address
	ip = reply[len(reply)- 4:]
	#ip address in bytes
	#convert byte to string
	ipv4 = ""
	for i in range(0,4):
		if(ip[i] == 0):
			print("Resolving " + hostname+"...")
			flag = 1
			print("Retrying...")
			return 0, flag
		ipv4 += str(ip[i])
		if(i != 3):
			ipv4 += "."
	#ipv4 has ip address
	print("Resolving " + hostname+"..."+ ipv4)
	#making TCP connection
	print("Connecting to " + hostname+"|"+ ipv4+"|:80")
	s = socket(AF_INET, SOCK_STREAM)
	s.connect((ipv4, 80))
	print("\t\t\t\t...connected.")
	if(url != ''):
		message = "GET /"+url+" HTTP/1.1\r\n"
	else:
		message = "GET / HTTP/1.1\r\n"
	message += "HOST: "+hostname+"\r\n"
	message += "User-Agent: Firefox/86\r\n"
	message += "\r\n"
	x = s.send(message.encode())
	print('HTTP request sent, awaiting response... Length: '+ str(x) + ' bytes')
	return s, flag

def receive_chunks(s, filename):
	data=''
	data = s.recv(1024).decode()
	#split of http headers
	data = data.split('\r\n\r\n',1)[1]
	fp = open(filename, "a")
	fp.write(data)
	fp.close()
	#receiving in chunks
	while True:
		#recv something
		try:
			data = s.recv(1024).decode()
			if len(data) < 1:
				break
			#print(data)
			fp = open(filename, "a")
			fp.write(data)
			fp.close()
		except:
			break
	return

def finalCall(website):
	retry = 0
	hostname, url, filename = getFileName_and_Url(website)
	query = constructQuery(hostname)
	s, flag = createConnection(query,hostname,url)
	#if ip not resolved
	while flag == 1 and retry < 5:
		query = constructQuery(hostname)
		s, flag = createConnection(query,hostname,url)
		retry+=1
		if retry == 5:
			print("Something wrong , couldn't get ip address of ",hostname," from response")
			return
			
	print("Saving to: '"+filename+"'\n")
	receive_chunks(s, filename)
	s.close()
	
def main():
	n = len(sys.argv)
	i=1
	while i<n:
		website = sys.argv[i]
		th = Thread(target = finalCall, args = (website,))
		th.start()
		#delaying execution so that file is not overwritten
		time.sleep(1)
		i+=1

if __name__ == "__main__":
	main()
	time.sleep(5)

