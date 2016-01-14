__author__ = 'Jackie'

import sys
import shutil
import os
from socket import *
import time
import threading

PORT = 5005

MONITOR__SERVER_IP = "localhost"
MONITOR__SERVER_PORT = 5006

class FileServer:
	#initialize the server
	def __init__(self, port):
		self.ip = gethostbyname(gethostname())
		self.port = port
		print('Server running at {0:s}:{1:4d}'.format(self.ip, self.port))
		try:
			self.server = socket(AF_INET, SOCK_STREAM)
			self.server.bind(('', self.port))
			self.server.listen(5) # Max connections
			print('Server start successfully...')
		except Exception as e:
			print("socket create fail{exec}".format(exce=e))#socket create fail

		# Duplicate data to new directory (data-PORT) to simulate server logical disk if does not exists
		# if os.path.exists('data-{port}'.format(port=self.port)) == False:
		# 	shutil.copytree('data', 'data-{port}'.format(port=self.port))

		#start to listen port
		self.waitConnection()


	def waitConnection(self):
		while True:
			try:
				conn, addr = self.server.accept()
				print('Connection from {address} connected!'.format(address=addr))
				#new thread to handle the request
				#
				data = conn.recv(4096)
				data = data.decode('utf-8')
				print("Received data: {0}".format(data))

				initial, final = data.split(';')

				# Reading a file in mode reading byte
				with open('data-{0}/lipsum.txt'.format(self.port), 'rb') as f:
					#f.seek(int(initial))
					#content = f.read(int(final) - int(initial))
					content = f.read()

				# Sent binary data to connected client
				conn.send(content)
				print('Data sent to client!')
				conn.close()
			except Exception as e:
				print(e)
			finally:
				self.__destroy__()

	#visite the monitor continuously
	def notityAlive(self):
		pass

	def notifyConnect(self):
		socketConnetc = socket(AF_INET, SOCK_STREAM)
		socketConnetc.connect(MONITOR__SERVER_IP, MONITOR__SERVER_PORT)
		sendData = '{ip}'

	def getFileStatus(self):
		pass

	def __destroy__(self):
		self.server.close()
		shutil.rmtree('data-{port}'.format(port=self.port))

	def hellp(self):
		pass


# run servers by threads
def runThreadSever(threadNum):
	global ports
	global servers
	server = FileServer(ports[threadNum])
	servers.append(server)

class ThreadServer(threading.Thread): #The timer class is derived from the class threading.Thread
	def __init__(self, fun, num):
		threading.Thread.__init__(self)
		self.fun = fun
		self.num = num

	def run(self,):
		self.fun(self.num)
	def stop(self):
		self.thread_stop = True

if __name__ == "__main__":
	#many machines
	#port = 5001
	# server = new FileServer(port)

	# one machine many ports
	ports = [5001, 5002, 5003, 5004, 5005]
	servers = []
	threads = []
	for i, v in enumerate(ports):
		t = ThreadServer(runThreadSever, i)
		t.start()
		threads.append(t)
	# for i in len(threads):
	# 	servers[i].server.close()
	# 	threads[i].stop()

































# if len(sys.argv) < 2:
# 	sys.exit('Usage: %s [PORT]' % sys.argv[0])

# port = int(sys.argv[1])

# port = 5001
#
# try:
# 	server = socket(AF_INET, SOCK_STREAM)
# 	server.bind(('', port))
# 	server.listen(5) # Max connections
#
# 	# Duplicate data to new directory (data-PORT) to simulate server logical disk if does not exists
# 	if os.path.exists('data-{port}'.format(port=port)) == False:
# 		shutil.copytree('data', 'data-{port}'.format(port=port))
# except Exception as e:
# 	print("socket create error{exec}".format(exce=e))#socket 创建失败
#
# print('Server running at {0:4d}'.format(port))
#
# while True:
# 	try:
# 		conn, addr = server.accept()
# 		print('Client connected!')
# 		print('Connection from {address}'.format(address=addr))
#
# 		data = conn.recv(4096)
# 		data = data.decode('utf-8')
# 		print("Received data: {0}".format(data))
#
# 		initial, final = data.split(';')
#
# 		# Reading a file in mode reading byte
# 		with open('data-{0}/lipsum.txt'.format(port), 'rb') as f:
# 			#f.seek(int(initial))
# 			#content = f.read(int(final) - int(initial))
# 			content = f.read()
#
# 		# Sent binary data to connected client
# 		conn.send(content)
# 		print('Data sent to client!')
# 		conn.close()
# 	except Exception as e:
# 		print(e)
#
# shutil.rmtree('data-%d' % port)
# server.close()





