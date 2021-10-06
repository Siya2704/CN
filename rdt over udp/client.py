#!/usr/bin/python
from library import*
prob = float(sys.argv[1])
server =('127.0.0.1', 12000)
sock = socket(AF_INET, SOCK_DGRAM)
	
def sum_data(data):
	sum = 0
	for x in data:
		sum += x
	return sum
	
ID = str(uuid.uuid4())
ID = ID.split('-',1)[0]#sending ID
n = random.randint(1,5)
print("client:",n)
seq_no = 1
#sending packet1
rdtsend(sock,server,n, prob,seq_no,ID)
response = rdtrecv(sock,server,n, prob,seq_no,ID)
print("server:",response)
if int(response) != n:
	print("packet",seq_no,", ID: ", ID, "corrupted")
#sending packet2
seq_no += 1
numbers=[]
for i in range (n):
	numbers.append(random.randint(1,10))
print("client:",end=" ")
for i in numbers:
	print(i, end=" ")
print()
rdtsend(sock,server,numbers, prob,seq_no,ID)
response = rdtrecv(sock,server,numbers, prob,seq_no,ID)
sum_ = sum_data(numbers) #for locally checking sum
if int(response) != sum_:
	print("packet",seq_no,", ID: ", ID, "corrupted")
print("server:",response)
sock.close()


