import socket 
import time 
from _thread import *
import sys
import threading

#===##===##===##===##===##===##===##===#
#SERVER INFO
#===##===##===##===##===##===##===##===#

host = '127.0.0.1'
print ('HOST: ',host)
port = 5552
port = int(input("Select a port: "))
global clients
clients = []
connexs = []
usernames = []

#===##===##===##===##===##===##===##===#
#BROADCAST
#===##===##===##===##===##===##===##===#

#def senddata(data, source):
def senddata(data, source):
	for connex in connexs:
		print ('Current client: ', connex.getpeername())
#		connex.sendto(source.encode(),connex.getpeername())
		print('Source: ', source)
		connex.sendto(str.encode(data),connex.getpeername())

#===##===##===##===##===##===##===##===#
#INDIVIDUAL THREAD OPERATION
#===##===##===##===##===##===##===##===#

def serverrun(conn, loop):
	print ('Server has started')
	Inner = True
	print('Current Thread: ', threading.current_thread())
	usersname=conn.recv(1024).decode('utf-8')
	print ('Username added: ', usersname)
	if usersname not in clients: 
		clients.append(usersname)
#		clients[usersname] = conn.getpeername()
	while True:
		data = conn.recv(1024).decode('utf-8')
		print('Received data', data)
		if 'Quit' in str(data):
			break 
		if 'Finish' in str(data): 
			print('Shutting Down.....\nPlease Wait a Moment')
			s.close()
			break
		print (time.ctime(time.time()) + str(addr) + " : :" + str(data.encode()))
#		senddata(data, source)
		source = conn.getpeername()
		senddata(data, source)
	s.close()

#===##===##===##===##===##===##===##===#
#SERVER GO CODE
#===##===##===##===##===##===##===##===#

global s
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print ('INFO: ' + host + ':' + str(port))
s.bind((host,port))

s.listen(3)
print ('Waiting for connection.....')

Loop = True 

while Loop: 
	conn, addr = s.accept()
	print('Establishing connection with: ', conn.getpeername())

	if conn.getpeername() not in clients:
		clients.append(conn.getpeername())
		connexs.append(conn)
	print ('Clients:', clients)

	#Threading and Looping
	nT = threading.Thread(target = serverrun, args =(conn, Loop)) 
	nT.daemon =True
	nT.start() 





