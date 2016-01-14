# -*- coding:utf-8 -*-
__author__ = 'Jackie'

import shutil
import os
from socket import *
import logging
import pickle
import threading
import datetime
from utils import constant as CONS

class FileServer:
	#initialize the server
	def __init__(self, port):
		self.ip = gethostbyname(gethostname())
		self.port = port
		self.threads = []
		logging.info('Server running at {0:s}:{1:4d}'.format(self.ip, self.port))
		try:
			self.server = socket(AF_INET, SOCK_STREAM)
			self.server.bind(('', self.port))
			self.server.listen(20) # Max connections
			logging.info('Server start successfully...')
		except Exception as e:
			logging.warn("socket create fail.{0}".format(e)) #socket create fail

		# notify the monitor
		self.notifyConnect()
		#start to listen port
		self.waitConnection()

	def notifyConnect(self):
		try:
			socketConnect = socket(AF_INET, SOCK_STREAM)
			socketConnect.connect((CONS.MONITOR__SERVER_IP, CONS.MONITOR__SERVER_PORT))

			packetDataDic = dict()
			packetDataDic['msgType'] = CONS.from_server_01
			packetDataDic['ip'] = self.ip
			packetDataDic['port'] = self.port
			packetData = pickle.dumps(packetDataDic)

			socketConnect.send(packetData)
			logging.info("send server info: '{0}' to monitor".format(packetData))
		except Exception as e:
			socketConnect.close()
			logging.error('Connect to monitor fail! {0}'.format(e))

	def waitConnection(self):
		upLoadTime = -1
		downLoadTime = -1
		while True:
			try:
				conn, addr = self.server.accept()
				logging.info('Connection from {address} connected!'.format(address=addr))

				msgDic = conn.recv(73)
				print("msgDic length:{1}", len(msgDic))
				dicData = pickle.loads(msgDic)
				if 'msgType' in dicData and 'fileName'in dicData:
					msgType = dicData['msgType']
					print("message type received:", msgType)
					if msgType == CONS.from_client_01: #上传
						print("execute:", CONS.from_client_01)
						threads = []
						if upLoadTime == -1:
							upLoadTime = 1
							starttime = datetime.datetime.now()  #统计服务器从开始接收文件到结束文件上传时间
							logging.info('服务器开始接收上传文件时间：{0}'.format(starttime))

						thread = threading.Thread(target=self.fromClientUploadmsgHandler,
												  args=(conn, dicData))#开启进程处理文件上传
						threads.append(thread)
						thread.start()

						for t in threads:
							t.join()
						endtime = datetime.datetime.now()
						logging.info('服务器结束上传文件时间：{0}'.format(starttime))
					elif msgType == CONS.from_client_02: #下载
						print("execute:", CONS.from_client_02)
						self.threads = []
						if downLoadTime == -1:
							upLoadTime = 1
							starttime = datetime.datetime.now()  #统计服务器从开始下载文件到结束文件下载时间
							logging.info('服务器开始接收下载文件时间：{0}'.format(starttime))

						thread = threading.Thread(target=self.fromClientDownloadmsgHandler,
												  args=(conn, dicData))#开启进程处理文件下载
						self.threads.append(thread)
						thread.start()
						for t in self.threads:
							t.join()

						endtime = datetime.datetime.now()
						logging.info('服务器开始结束上传文件时间：{0}'.format(starttime))
					else:
						conn.close()
						logging.info('message type error')

			except Exception as e:
				conn.close()
				logging.error('connect to with client error.{0}'.format(e))

	def fromClientUploadmsgHandler(self, client, dicData = []):
		#back file list
		print("execute: fromClientUploadmsgHandler")
		if 'fileName'in dicData:
			fileName = dicData['fileName'].rstrip()
			content = ""
			while True:
				tempRevContent = client.recv(1024)
				tempRevContent = tempRevContent.decode('utf-8')
				content = content + tempRevContent
				if tempRevContent[-1] == '$':
					content = content[0:-1]
					print("end file receive")
					break

			print("final content length:", len(content))

			with open('data-{0}/{1}'.format(self.port, fileName), 'wb') as f:
				f.write(content.encode('utf-8'))

			client.close()
			logging.info("write file {0} finished!".format(fileName))
		else:
			logging.info('message error')

	def fromClientDownloadmsgHandler(self):
		pass

	def fromMonitorBackFile(self):
		pass
	# visite the monitor continuously
	def notityAlive(self):
		pass

	def getFileStatus(self):
		pass

	def destroy(self):
		self.server.close()
		# shutil.rmtree('data-{port}'.format(port=self.port))

	def hellp(self):
		pass



# initialize the log
def initLog(logName):
	# createa log folder
	if not os.path.isdir('log'):
		os.mkdir('log')
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M', filename='log/' + logName)
	# define a Handler which writes INFO messages or higher to the sys.stderr
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	# set a format which is simpler for console use
	formatter = logging.Formatter('%(levelname)-6s:%(message)s')
	# tell the handler to use this format
	console.setFormatter(formatter)
	# add the handler to the root logger
	logging.getLogger('').addHandler(console)

if __name__ == "__main__":
	initLog('server3.log')
	server = FileServer(CONS.PORT_START + 3)
	# server.destroy()

