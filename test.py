# -*- coding:utf-8 -*-
__author__ = 'Jackie'

import os
import math
from socket import *
import logging
import datetime
import pickle
import threading
import sys
from utils import constant as CONS

class Client:
    #initialize the server
    def __init__(self, port):
        self.uploadFileThreadNum = 1
        self.downloadFileThreadNum = 1
        self.threads = []
        self.fileName = ""
        logging.info('client start...')

    # 上传文件多线程方法
    def uploadFileMutiThreading(self, serverInforLi, start, end):
        if not serverInforLi:
          logging.warning("can't get server information")
          return -1
        if len(serverInforLi) < 3 or len(serverInforLi) > 4:
          logging.warning("active server is less than Three or more than Four!")
          return -1

        server1FileEndNum = serverInforLi[0]["blockEnd"]
        currentPosition = start
        with open(self.fileName, 'rb') as f:
            while currentPosition <= end:
                if len(serverInforLi) == 3:
                        backServerIP = serverInforLi[2]["ip"]
                        backServerPort = serverInforLi[2]["port"]
                        if currentPosition <= server1FileEndNum:
                            serverIP = serverInforLi[0]["ip"]
                            serverPort = serverInforLi[0]["port"]
                        else:
                            serverIP = serverInforLi[1]["ip"]
                            serverPort = serverInforLi[1]["port"]
                else:
                    if currentPosition <= server1FileEndNum:
                        serverIP = serverInforLi[0]["ip"]
                        serverPort = serverInforLi[0]["port"]
                        backServerIP = serverInforLi[2]["ip"]
                        backServerPort = serverInforLi[2]["port"]
                    else:
                        serverIP = serverInforLi[1]["ip"]
                        serverPort = serverInforLi[1]["port"]
                        backServerIP = serverInforLi[3]["ip"]
                        backServerPort = serverInforLi[3]["port"]
                print("currentPosition:{0}, server:{1} {2},backServer:{3} {4}".format(currentPosition, serverIP,serverPort, backServerIP, backServerPort))
                f.seek(int((currentPosition - 1)*CONS.BLOCK_SIZE))
                # print("filePosition:", f.tell())

                msgType = CONS.from_client_01
                fileNameLi = self.fileName.split('.')
                if len(fileNameLi) >= 2:
                    fileNumber = '0' * (CONS.FILE_NAME_NUMBER_LENGTH - len(str(currentPosition))) + str(currentPosition)
                    fileName = fileNameLi[0] + fileNumber + '.' + fileNameLi[1]
                    fileName = fileName + (CONS.FILE_NAME_LENGTH-len(fileName)) * " "
                    # print("filename", fileName)
                else:
                    logging.info('File type is wrong!')

                packetDataDic = dict()#包括msgType, filename, back file host ip and port
                packetDataDic['msgType'] = msgType
                packetDataDic['fileName'] = fileName
                packetDataDic['backServerIP'] = backServerIP + " " * (CONS.SERVER_IP_LENGTH - len(str(backServerIP)))
                packetDataDic['backServerPort'] = str(backServerPort) + " " * (CONS.SERVER_PORT_LENGTH - len(str(backServerPort)))
                packetData = pickle.dumps(packetDataDic)

                #test currentPosition
                try:
                    client = socket(AF_INET, SOCK_STREAM)
                    client.connect((serverIP, serverPort))

                    #传递上传文件基本信息
                    # print("packetData length:", len(packetData))
                    client.send(packetData)

                    # fileSizeCount = 0
                    for i in range(int(CONS.BLOCK_SIZE/CONS.ONCE_READ_FILE_SIZE)):
                        content = f.read(CONS.ONCE_READ_FILE_SIZE)
                        # fileSizeCount = fileSizeCount + len(content)
                        if not content:
                            break
                        client.send(content)

                    # print("length of file send", fileSizeCount)
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

        # self.uploadFileThreadNum = blockSize ?? test the best one
        if blockSize > 0:
            serverInforLi = self.getInfoFromMonitor(CONS.from_client_03, fileName, blockSize)
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

                if i == len(tempLi)-1:
                    end = blockSize
                print('start:{0}, end:{1}'.format(start, end))

                thread = threading.Thread(target=self.uploadFileMutiThreading,
                                          args=(serverInforLi, start, end))
                self.threads.append(thread)
                thread.start()
                logging.info("start threading{0} to upload file blocks {1}-{2}".format(i+1, start, end))
        else:
            logging.info("file size is not right")

    # 下载文件多线程方法
    def downloadFileMutiThreading(self, serverInforLi, start, end):
        firstBlockSize = serverInforLi[0]["blockEnd"]

        currentPosition = start
        while currentPosition <= end:
            msgType = CONS.from_client_02
            fileNameLi = self.fileName.split('.')
            if len(fileNameLi) >= 2:
                fileNumber = '0' * (CONS.FILE_NAME_NUMBER_LENGTH - len(str(currentPosition))) + str(currentPosition)
                fileName = fileNameLi[0] + fileNumber + '.' + fileNameLi[1]
                # fileName = fileName + (CONS.FILE_NAME_LENGTH - len(fileName)) * " "
                # print("filename", fileName)
            else:
                logging.info('File type is wrong!')

            packetDataDic = dict()#包括msgType, filename, back file host ip and port
            packetDataDic['msgType'] = msgType
            packetDataDic['fileName'] = fileName
            packetData = pickle.dumps(packetDataDic)

            try:
                if currentPosition <= firstBlockSize:
                    serverIP = serverInforLi[0]["ip"]
                    serverPort = serverInforLi[0]["port"]
                else:
                    serverIP = serverInforLi[1]["ip"]
                    serverPort = serverInforLi[1]["port"]

                client = socket(AF_INET, SOCK_STREAM)
                client.connect((serverIP, serverPort))

                #传递上传文件基本信息
                # print("packetData length:", len(packetData))
                client.send(packetData)

                with open('download{0}'.format(self.fileName), 'ab+') as f:
                    # print("position", currentPosition)
                    f.seek(CONS.BLOCK_SIZE * (currentPosition - 1))
                    while True:
                        revContent = client.recv(CONS.ONCE_READ_FILE_SIZE)
                        # fileSizeCount = fileSizeCount + len(revContent)
                        if not revContent:
                            print("文件所在位置:", f.tell())
                            break
                        f.write(revContent)

                client.close()
                logging.info("download file:{0} to server:{1}".format(fileName, serverIP))
            except Exception as e: #不考虑上传失败
                client.close()
                logging.error("send file:{0} to server:{1} fail! {2}".format(fileName, serverIP, e))

            currentPosition = currentPosition + 1

    def downloadFile(self, fileName):
        self.fileName = fileName
        serverInforLi = self.getInfoFromMonitor(CONS.from_client_04, fileName)

        if len(serverInforLi) < 2:
            logging.warning("valid server is less than 2!!!")
            return -1


        secondBlockSize = serverInforLi[1]["blockEnd"]

        blockSize = secondBlockSize
        # self.downloadFileThreadNum = blockSize ?? test the best one
        if serverInforLi:
            eachThreadBlockCeilSize = math.ceil(blockSize/self.downloadFileThreadNum)

            if eachThreadBlockCeilSize <= 1:
                self.downloadFileThreadNum = blockSize

            eachThreadBlockFloorSize = math.floor(blockSize/self.downloadFileThreadNum)

            leftBlockSizeNum = blockSize - eachThreadBlockFloorSize * self.downloadFileThreadNum

            tempLi = list(range(self.downloadFileThreadNum))

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

                if i == len(tempLi)-1:
                    end = blockSize
                print('start:{0}, end:{1}'.format(start, end))

                thread = threading.Thread(target=self.downloadFileMutiThreading,
                                          args=(serverInforLi, start, end))
                self.threads.append(thread)
                thread.start()
                logging.info("start threading{0} to download file blocks {1}-{2}".format(i+1, start, end))
        else:
            logging.info("file size is not right")

    def getInfoFromMonitor(self, msgType, fileName, blockSize = 0):
        recData = None
        try:
            client = socket(AF_INET, SOCK_STREAM)
            client.connect((CONS.MONITOR__SERVER_IP, CONS.MONITOR__SERVER_PORT))

            packetDataDic = dict()
            packetDataDic['msgType'] = msgType
            packetDataDic['fileName'] = fileName
            packetDataDic['blockSize'] = blockSize
            packetData = pickle.dumps(packetDataDic)

            client.send(packetData)#发送上传文件信息
            logging.info("Send request to monitor".format(packetDataDic))

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
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)-6s:%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


if __name__ == "__main__":
    initLog('client.log')
    client = Client(CONS.PORT_START + 5)

    commandLis = ["download", "upload", "abort"]
    while True:
        print("请选择所要的操作：")
        inputCmd = input("download, upload, abort?\n")
        fileName = ""
        if inputCmd == commandLis[0]:
            fileName = input("请输入文件名:")
            starttime = datetime.datetime.now()
            logging.info('开始文件下载...{0}'.format(starttime))
            client.uploadFile(fileName)
            for t in client.threads:
                t.join()
            endtime = datetime.datetime.now()

            logging.info('客户端结束时间：{0}'.format(endtime))
            logging.info('客户端所花时间：{0}'.format(endtime - starttime))
            break
        elif inputCmd == commandLis[1]:
            starttime = datetime.datetime.now()
            fileName = input("请输入文件名:{0}")
            logging.info('开始文件上传...{0}'.format(starttime))
            client.uploadFile(fileName)
            for t in client.threads:
                t.join()
            endtime = datetime.datetime.now()

            logging.info('客户端结束时间：{0}'.format(endtime))
            logging.info('客户端所花时间：{0}'.format(endtime - starttime))
            break
        elif inputCmd == commandLis[2]:
            print("想好再来^=^")
            sys.exit()
        else:
            print("输入不对,再来一遍！")

    for t in client.threads:
        t.join()
    endtime = datetime.datetime.now()

    # logging.info('客户端结束时间：{0}'.format(endtime))
    # logging.info('客户端所花时间：{0}'.format(endtime - starttime))
    #
    # logging.warning('客户端开始时间：{0}'.format(starttime))


