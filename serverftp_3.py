import os
import netifaces

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def yes_or_no(question):
    reply = str(input(question+' (y/n) ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("wrong answer , please selecta valid answer to : "+question)

def createuser(authorizer):
	user=input("insert the username: " )
	password=input("insert the password: ")
	print("select the category of the user:")
	permission=['elradfmw','elr','adfmw'] #1=completo,2=readonly,3=writeonly
	category=0
	while (category <1 or category>3):
		try:
			category=int(input("insert the category,1 to complete,2 to readonly ,3 to write only"))
		except ValueError:
			print ('invalid value')
	authorizer.add_user(user, password, '.', perm=permission[category])

def main():
	localip=[]
	for i in range(0,netifaces.interfaces().__len__() ):
		try:
			ip=netifaces.ifaddresses(netifaces.interfaces()[i])[netifaces.AF_INET][0]['addr']
			print("the local ip is:"+ip)
			localip.append(ip)
		except KeyError:
			ip=''
	port = input("insert the port: ")
	authorizer = DummyAuthorizer()
	adduser = True
	while(adduser==True):
		createuser(authorizer)
		adduser=yes_or_no('do you want to add other user?')

	#Read permissions:
		# - "e" = change directory (CWD command)
		# - "l" = list files (LIST, NLST, MLSD commands)
		# - "r" = retrieve file from the server (RETR command)

	#Write permissions:
		# - "a" = append data to an existing file (APPE command)
		# - "d" = delete file or directory (DELE, RMD commands)
		# - "f" = rename file or directory (RNFR, RNTO commands)
		# - "m" = create directory (MKD command)
		# - "w" = store a file to the server (STOR, STOU commands)
	authorizer.add_anonymous(os.getcwd())

	# Instantiate FTP handler class
	handler = FTPHandler
	handler.authorizer = authorizer

	# Define a customized banner (string returned when client connects)
	handler.banner = "pyftpdlib based ftpd ready."

	# Instantiate FTP server class and listen on declarated port
	address = ('', port)
	server = FTPServer(address, handler)

	# set a limit for connections
	server.max_cons = 256
	server.max_cons_per_ip = 50

	# start ftp server
	print("to connect to this server you should use the adderess:")
	for ip in localip:
		print(" ftp://"+ip+":"+port)
	print("to turn this server off just press Crtl+c or close the terminal window")
	server.serve_forever()

if __name__ == '__main__':
    main()
