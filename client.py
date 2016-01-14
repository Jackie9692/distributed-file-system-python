# -*- coding:utf-8 -*-
__author__ = 'Jackie'

import os
import math
from socket import *
import logging
import datetime
import pickle
import threading
from utils import constant as CONS

class Client:
	#initialize the server
	def __init__(self, port):
		self.uploadFileThreadNum = 1
		self.downloadFileThreadNum = 4
		self.threads = []
		self.fileName = ""
		logging.info('client start...')


	# 上传文件多线程方法
	def uploadFileMutiThreading(self, serverIP, serverPort, start, end, ):
		EOF = b'$'
		currentPosition = start
		with open(self.fileName, 'rb') as f:
			while currentPosition <= end:
					f.seek(int((currentPosition - 1)*CONS.BLOCK_SIZE))
					print("filePosition:", f.tell())
					content = f.read(CONS.BLOCK_SIZE)
					print("length of content:", len(content))
					# content = content.decode('utf-8')

					msgType = CONS.from_client_01
					fileNameLi = self.fileName.split('.')
					if len(fileNameLi) >= 2:
						fileNumber = '0' * (CONS.FILE_NAME_NUMBER_SIZE - len(str(currentPosition))) + str(currentPosition)
						fileName = fileNameLi[0] + fileNumber + '.' + fileNameLi[1]
						fileName = fileName + (CONS.FILE_NAME_SIZE-len(fileName)) * " "
						print("filename", fileName)

					else:
						logging.info('File type is wrong!')
					# print("content:{0}".format(content))

					packetDataDic = dict()
					packetDataDic['msgType'] = msgType
					packetDataDic['fileName'] = fileName
					# packetDataDic['content'] = content
					packetData = pickle.dumps(packetDataDic)

					#test currentPosition
					if currentPosition == 12:
						pass
					try:
						client = socket(AF_INET, SOCK_STREAM)
						client.connect((serverIP, serverPort))

						#传递两次 消息类型与文本内容
						print("packetData length:", len(packetData))
						client.send(packetData)

						sendContent = content + EOF
						print("send content length:", len(sendContent.decode('utf-8')))
						client.send(sendContent)

						client.close()
						logging.info("send file:{0} to server:{1}".format(fileName, serverIP))
					except Exception as e: #不考虑上传失败
						client.close()
						logging.error("send file:{0} to server:{1} fail! {2}".format(fileName, serverIP, e))

					currentPosition = currentPosition + 1

	def uploadFile(self, fileName):
		self.fileName = fileName
		blockSize = 0
		if os.path.isfile(self.fileName): #block 大小为64M
			fileSize = os.path.getsize(fileName)
			# print(fileSize)
			blockSize = math.ceil(fileSize/CONS.BLOCK_SIZE)
			# blockSize = math.ceil(fileSize/CONS.BLOCK_SIZE*16)

		# blockSize = 20
		if blockSize > 0:
			serverInforLi = self.getInfoFromMonitor(fileName, blockSize)
			eachThreadBlockCeilSize = math.ceil(blockSize/self.uploadFileThreadNum)

			if eachThreadBlockCeilSize <= 1:
				self.uploadFileThreadNum = blockSize

			eachThreadBlockFloorSize = math.floor(blockSize/self.uploadFileThreadNum)

			leftBlockSizeNum = blockSize - eachThreadBlockFloorSize * self.uploadFileThreadNum

			tempLi = list(range(self.uploadFileThreadNum))

			currentPos = 0  #控制各线程文件上传起始位置
			label = -1
			for i, each in enumerate(tempLi):
				if i < leftBlockSizeNum:
					start = eachThreadBlockCeilSize * i + 1
					end =  eachThreadBlockCeilSize * (i + 1)
					if i == (leftBlockSizeNum - 1):
						currentPos = end
						label = i
				else:
					start = currentPos + eachThreadBlockFloorSize * (i - label - 1) + 1
					end =  currentPos + eachThreadBlockFloorSize * (i - label)

				serverIP = serverInforLi[0]['ip']
				serverPort = serverInforLi[0]['port']
				# if i <= int(self.uploadFileThreadNum/2):
				# 	serverIP = serverInforLi[0]['ip']
				# 	serverPort = serverInforLi[0]['port']
				# else:
				# 	serverIP = serverInforLi[1]['ip']
				# 	serverPort = serverInforLi[1]['port']
				if i == len(tempLi)-1:
					end = blockSize
				print('start:{0}, end:{1}'.format(start, end))
				thread = threading.Thread(target=self.uploadFileMutiThreading,
										  args=(serverIP, serverPort, start, end))
				self.threads.append(thread)
				thread.start()
				logging.info("start threading{0} to upload file blocks {1}-{2}".format(i+1, start, end))

		else:
			pass
	def downloadFile(self):
		pass

	def getInfoFromMonitor(self, fileName, blockSize):
		recData = None
		try:
			client = socket(AF_INET, SOCK_STREAM)
			client.connect((CONS.MONITOR__SERVER_IP, CONS.MONITOR__SERVER_PORT))

			packetDataDic = dict()
			packetDataDic['msgType'] = CONS.from_client_03
			packetDataDic['fileName'] = fileName
			packetDataDic['blockSize'] = blockSize
			packetData = pickle.dumps(packetDataDic)

			client.send(packetData)#发送上传文件信息
			logging.info("send request to monitor".format(packetData))

			recData = client.recv(1024)
			recData = pickle.loads(recData)
			logging.info("get server information from monitor".format(recData))
			client.close()
		except Exception as e:
			client.close()
			logging.error('Connect to monitor fail.{0}'.format(e))
		return recData

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
	initLog('client.log')
	client = Client(CONS.PORT_START + 5)

	starttime = datetime.datetime.now()
	logging.info('上传文件开始时间：{0}'.format(starttime))
	# filename = input("Input file name\n")
	# client.uploadFile(fileName = "linux.avi")
	client.uploadFile(fileName = "lipsum.txt")
	for t in client.threads:
		t.join()
	print("thread out join")
	endtime = datetime.datetime.now()


	logging.info('上传文件结束时间：{0}'.format(endtime))
	logging.info('上传文件所耗时间：{0}秒'.format((endtime - starttime).seconds))

	#input to choose which action
	# client.destroy()

# threads = []
# #get real size from monitor
# filesize = os.path.getsize('data/lipsum.txt')
# splitsize = filesize / len(PORTS)
# remainder = filesize % len(PORTS)

#print 'Total size %d' % filesize

# for i in range(len(PORTS)):
# 	if i == 0:
# 		final = splitsize
# 		initial = 0
# 	elif i < len(PORTS) -1:
# 		final += splitsize
# 		initial += splitsize + 1
# 	else:
# 		final += splitsize + remainder
# 		initial += splitsize
#
# 	params = {
# 		'port': PORTS[i],
# 		'initial': int(initial),
# 		'final': int(final)
# 	}
#
# 	#print 'Initial size: %s, final size: %s' % (params['initial'], params['final'])
# 	thread = ClientThread(download, params)
# 	thread.start()
# 	threads.append(thread)
#
# # Waiting for threads to finish
# for thread in threads:
# 	thread.join()
#
# # Concatenate temporary files
# out = open('out.txt', 'wb')
#
# for port in PORTS:
# 	try:
# 		# Append temporary file content to output file
# 		shutil.copyfileobj(open('{port}.tmp'.format(port=port), 'rb'), out)
# 		# Remove temporary file
# 		# os.remove('{port}.tmp'.format(port=port))
# 	except IOError:
# 		sys.exit('Error to append temporary file content to output file')
#
# out.close()