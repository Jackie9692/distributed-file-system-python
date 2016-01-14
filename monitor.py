# -*- coding:utf-8 -*-
__author__ = 'Jackie'

import shutil
import os
from socket import *
import logging
import pickle
import threading
from utils import constant as CONS

class Filemonitor:
	#initialize the monitor
	def __init__(self, port):
		self.ip = gethostbyname(gethostname())
		self.port = port
		self.aliveServerData = []#活着的服务器信息
		self.fileInfo = dict() #上传文件的文件名和block大小

		logging.info('monitor running at {0:s}:{1:4d}'.format(self.ip, self.port))
		try:
			self.monitor = socket(AF_INET, SOCK_STREAM)
			self.monitor.bind(('', self.port))
			self.monitor.listen(5) # Max connections
			logging.info('monitor start successfully...')
		except Exception as e:
			logging.warn("socket create fail{exec}".format(exce=e))#socket create fail

		#start to listen port
		self.waitConnection()


	#向客户端返回上传服务器信息
	def sendServerUploadInfoToClient(self, dicData, client):
		if 'blockSize' in dicData and 'fileName' in dicData:
			self.fileInfo['fileName'] = dicData['fileName']
			self.fileInfo['blockSize'] =  dicData['blockSize']
			aliveLength = len(self.aliveServerData) #只考虑为四台或三台
		else:
			logging.warn("can not get necessary information(blocksize) form client")
			return
		# 两台服务器直接接受客户端文件  and 一台或两台通过服务器备份
		firstServerFileEndSize = int(dicData['blockSize']/2)

		self.aliveServerData[0]['blockStart'] = 1
		self.aliveServerData[0]['blockEnd'] = firstServerFileEndSize
		self.aliveServerData[1]['blockStart'] = firstServerFileEndSize + 1
		self.aliveServerData[1]['blockEnd'] = dicData['blockSize']
		if aliveLength == 3: #上传时就已经损坏一台
			self.aliveServerData[2]['blockStart'] = 1
			self.aliveServerData[2]['blockEnd'] = dicData['blockSize']
		elif aliveLength == 4:
			self.aliveServerData[2]['blockStart'] = 1
			self.aliveServerData[2]['blockEnd'] = firstServerFileEndSize
			self.aliveServerData[3]['blockStart'] = firstServerFileEndSize + 1
			self.aliveServerData[3]['blockEnd'] = dicData['blockSize']
		else:
			logging.warn("the server number is not right")
		packetData = pickle.dumps(self.aliveServerData)
		client.send(packetData)
		logging.info("send server info: '{0}' to monitor".format(packetData))

	#向客户端返回下载服务器信息
	def sendServerDownloadInfoToClient(self):
		pass

	# 服务器信息初始化
	def initServerInfo(self, dicData):
		if 'ip' in dicData and 'port' in dicData:
			serverDic = dict()
			serverDic['ip'] = dicData['ip']
			serverDic['port'] = dicData['port']
			serverDic['blockStart'] = 0
			serverDic['blockEnd'] = 0
			self.aliveServerData.append(serverDic)

			# #for simulate 4machine
			# serverDic1 = dict()
			# serverDic1['ip'] = dicData['ip']
			# serverDic1['port'] = dicData['port']
			# serverDic1['blockStart'] = 0
			# serverDic1['blockEnd'] = 0
			# self.aliveServerData.append(serverDic1)
		else:
			logging.warn('can not get server connection necessary info')

	# 刷新服务器信息
	def refreshServerInfo(self):
		for each in self.aliveServerData:
			each['timeRefresh'] = 'hah'


	def waitConnection(self):
		while True:
			try:
				conn, addr = self.monitor.accept()
				logging.info('Connection from {address} connected!'.format(address=addr))

				helloMsg = conn.recv(1024)
				dicData = pickle.loads(helloMsg)
				if 'msgType' in dicData:
					msgType = dicData['msgType']
					if msgType == CONS.from_client_03: #上传
						self.sendServerUploadInfoToClient(dicData, conn)
					elif msgType == CONS.from_client_04: #下载
						self.sendServerDownloadInfoToClient(dicData, conn)
					elif msgType == CONS.from_server_01: #服务器创建状态
						self.initServerInfo(dicData)
					elif msgType == CONS.from_server_02: #服务器运行状态
						self.refreshServerInfo(dicData)
				else:
					logging.info("can't get message type")
					continue

			except Exception as e:
				logging.error('monitor fail.{0}'.format(e))
			finally:
				conn.close()


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
	initLog('monitor.log')
	monitor = Filemonitor(CONS.PORT_START)
	monitor.destroy()





























