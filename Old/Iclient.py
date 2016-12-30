from tkinter import * 
from tkinter import ttk 
from PIL import Image, ImageTk
from lib2to3 import *

import socket 
import time 
from _thread import *
import sys
import threading
import argparse

def Main(username,server, changed):

#WIDGET CREATION 
#===##===##===##===##===##===##===##===#
#GUI CLASS CONSTRUCTOR  
#===##===##===##===##===##===##===##===#

	class MainP: 

		def __init__(self, master): 

			master.title("Jimmy's Instant Messaging App")
			master.geometry('400x400+700+200')
		#	master.resizable(False, False)

	#INITIAL SCREEN 

			self.icanvas = Canvas(master, bg = 'black')
			self.icanvas.pack(fill = BOTH, expand = True)

			self.ilabeluser = Label(self.icanvas, text = 'Username', bg ='black', fg = 'white', font = ('Arial',15, 'bold'))
			self.ilabelserver = Label(self.icanvas, text = 'Server Address', bg ='black', fg = 'white', font = ('MS Serif',15, 'bold'))
			self.ilabelport = Label(self.icanvas, text = 'Port', bg ='black', fg = 'white', font = ('MS Serif',15, 'bold'))
			self.ientryuser = Entry(self.icanvas, width = 20)
			self.ientryserver = Entry(self.icanvas, width = 10)
			self.ientryport = Entry(self.icanvas, width = 6)
			self.ibuttonserver = ttk.Button(self.icanvas, text='Connect')

			#Geometry Manager
			self.ilabeluser.place(relx = 0.5, rely = 0.5, anchor = CENTER, y=-100 )
			self.ientryuser.place(relx = 0.5, rely = 0.5, anchor = CENTER,y= -50)
			self.ilabelserver.place(relx = 0.5, rely = 0.5, anchor = CENTER, x=-75,y= 0)
			self.ilabelport.place(relx = 0.5, rely = 0.5, anchor = CENTER, x=50,y= 0)
			self.ientryserver.place(relx = 0.5, rely = 0.5, anchor = CENTER, x=-75, y= 50)
			self.ientryport.place(relx = 0.5, rely = 0.5, anchor = CENTER, x= 50,  y= 50)
			self.ibuttonserver.place(relx = 0.5, rely = 0.5, anchor = CENTER, y= 110)


			self.ibuttonserver.config(command = lambda: get_info()) 

			def get_info():
				if len(self.ientryuser.get()) > 0 and len(self.ientryserver.get()) > 0: 
					global store_user,store_address,store_port
					store_user,store_address,store_port = self.ientryuser.get(),self.ientryserver.get(),int(self.ientryport.get()) 
					print ('Entered Username: ', store_user) 
					print ('Entered Address: ', store_address)
					print ('Entered Port', store_port)	
#					auth(my_app, store_user, store_address, store_port)
					auth(my_app, store_user, (store_address, store_port,))

	#MAIN PROGRAM

			self.top_frame = Frame(master)
			self.top_frame.pack()

			self.toppanel = Canvas(self.top_frame, background='black', height=50, width=400)
			self.toppanel.pack()

			self.bimage = ImageTk.PhotoImage(Image.open('rsettings.png').resize((25,25)))
			self.toppanel.create_image(370,30, image = self.bimage)

			self.texts = Text(master,height=15, bg='white', borderwidth=5)
			self.texts.pack()

			self.bottom_frame = Frame(master, background='white')
			self.bottom_frame.pack()

			self.username = Label(self.bottom_frame, width = 10, text = 'username', background='white', fg='black', font=('Arial',14))
			self.username.grid(row=0,column=0)

			self.entry= Entry(self.bottom_frame, width = 20)
			self.entry.grid(row=0,column=1)

			self.send_button = ttk.Button(self.bottom_frame, text = 'Send', command = lambda :self.send_entry())
			self.send_button.grid(row=0,column=2)

			self.button_pressed = False

			def send_entrykey(event):
				self.send_entry()
			
			master.bind('<Return>', send_entrykey)

		def send_entry(self): 
			self.button_pressed = True

	#===##===##===##===##===##===##===##===#
			#END OF CLASS CONSTRUCTOR
	#===##===##===##===##===##===##===##===#


	#===##===##===##===##===##===##===##===#
	#THREAD ONE - SENDER
	#===##===##===##===##===##===##===##===#
	def connector(ser,my_app,username,c_shutdown):	
		print('Established connection with: ', server)
		ser.send(str.encode(username))
		print ('Username entered')
		while not c_shutdown:	
	#		print ('Waiting...')
			cLock.acquire()
			if my_app.button_pressed: 
				sendm = my_app.entry.get()
				my_app.entry.delete(0,END)
				themessage = username + " :: " + sendm
				if sendm != '':
					ser.send(str.encode(themessage))
					print ('Just sent: ', sendm)
				print ('Button pressed: ', my_app.button_pressed)
				my_app.button_pressed = False
			cLock.release()
			time.sleep(0.5) 

		r_shutdown = True
		c_shutdown =True
		cT.join()
		rT.join()
		ser.close()      

	#===##===##===##===##===##===##===##===#
	#THREAD TWO - RECEIVER
	#===##===##===##===##===##===##===##===#

	def receiver(sock, r_shutdown, username):
	#	receive_existing_clients = sock.revfrom(1024)
		while not r_shutdown:
		  try:
		  	rLock.acquire()
		  	while True:
		  		#sourcedata, saddr = sock.rev(1024)
		  		#print('Sender name is: ', sourcedata.decode('utf-8'))
		  		rdata, raddr = sock.recvfrom(1024)
		  		print ('Received:', str(rdata.decode('utf-8')))
		  		print ('FROM:', raddr)
		  		my_app.texts.insert(END, '\n' + rdata.decode('utf-8') + '\n')
		  		time.sleep(0.1)
		  except:
		  	pass
		  finally:
		  	rLock.release()
		r_shutdown = True
		c_shutdown =True
		cT.join()
		rT.join()
		ser.close()           

	#===##===##===##===##===##===##===##===#



	#===##===##===##===##===##===##===##===#
	#After authentication
	#===##===##===##===##===##===##===##===#
	def auth(my_app, user,server):
		
		#Unpacking and packing new items
		my_app.icanvas.pack_forget()
		my_app.top_frame.pack()
		my_app.texts.pack()
		my_app.bottom_frame.pack()

		my_app.username.configure(text=user) 
		print ("Completed 1st section")

		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect(server)

		create_threads(s,user) 				#Creating sender and receiver threads 

	#===##===##===##===##===##===##===##===#
	#Thread generator for sending and receiving messages
	#===##===##===##===##===##===##===##===#
	def create_threads(s,username): 
		global cT, rT
		cT = threading.Thread(target = connector, args = (s,my_app,username,c_shutdown))
		rT = threading.Thread(target = receiver, args = (s,r_shutdown,username))
		cT.start()
		print ("Connecting thread: started") 
		rT.start()
		print ("Receiving thread: started")

	#===##===##===##===##===##===##===##===#
	#Thread ZERO - GUI thread
	#===##===##===##===##===##===##===##===#
	def gui_thread(): 
		root.mainloop()

#===##===##===##===##===##===##===##===#
#Main operations
#===##===##===##===##===##===##===##===#

	global root, my_app,c_shutdown, r_shutdown, gT
	root = Tk()
	my_app = MainP(root)
	my_app.top_frame.pack_forget()
	my_app.texts.pack_forget()
	my_app.bottom_frame.pack_forget()

	input_username = "default"
	input_address = "127.0.0.01" 
	c_shutdown,r_shutdown = False, False
	cLock,rLock = threading.Lock(),threading.Lock()

	if changed == True:			#If arguments are initial entered 
		auth(my_app, username, server)
		gT = threading.Thread(target = gui_thread, args = ())
		gT.start()
	else:
		gT = threading.Thread(target = gui_thread, args = ())
		gT.start()
	print ("GUI initialized: started") 

#===##===##===##===##===##===##===##===#
#Terminal run code
#===##===##===##===##===##===##===##===#

if __name__ == '__main__': 

	parser = argparse.ArgumentParser()
	parser.add_argument("--u", help = "Username")
	parser.add_argument("--p", help = "Port number")
	parser.add_argument("--a", help = "Address number")
	args, changed = parser.parse_args(), False

	try: 
		username = str(args.u)
	except:
		username = 'Anonymous'
	try: 
		address = str(args.a)
	except:
		address = '127.0.0.1' 
	try: 
		port = int(args.p)
	except:
		port = 5000 
	
	server = (address,port,)

	if username != 'Anonymous' or address != '127.0.0.1' and port != 5000: 
		changed = True

	Main(username,server, changed)

