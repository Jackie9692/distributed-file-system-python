# coding=utf-8

# test decorator

# def log(func, *args, **kw):
#     def wrapper():
#         print('call %s():' %func.__name__)
#         print(args)
#         return func(*args, **kw)
#     return wrapper
#
# def originalFunc(*args, **kw ):
#     print("origianl function")
#     print(args)
#
#
# testF = log(originalFunc, 1,23,4)
# testF()

# words = ['cat', 'window', 'defenestrate']
# for w in words:
#      if len(w) > 6:
#         pass
#         # words.insert(0, w)
# print('before:'+ str(words))
#
# for w in words[:]:
#     if len(w) > 6:
#         words.insert(0, w)
#     # print(w, len(w))
# print('after:'+ str(words))

#
# @log
# def now():
#     print('2014-3-25')

#erro
# try:
#     print('try...')
#     r = 10 / 0
#     print('result:', r)
# except ZeroDivisionError as e:
#     print('except:', e)
# finally:
#     print('finally...')
# print('END')

# def foo(s):
#     return 10 / int(s)
#
# def bar(s):
#     return foo(s) * 2
#
# def main():
#     bar('0')
#
# main()

#logging
# import logging
#
# def foo(s):
#     return 10 / int(s)
#
# def bar(s):
#     return foo(s) * 2
#
# def main():
#     try:
#         bar('0')
#     except Exception as e:
#         logging.exception(e)
#
# main()
# print('END')

#raise
# def foo(s):
#     n = int(s)
#     if n==0:
#         raise ValueError('invalid value: %s' % s)
#     return 10 / n
#
# def bar():
#     try:
#         foo('0')
#     except ValueError as e:
#         print('ValueError!')
#         raise
#
# bar()

#debug
# import pdb
#
# s = '0'
# n = int(s)
#
# print("pause before")
# pdb.set_trace() # 运行到这里会自动暂停
# print("pause after")
#
# print(10 / n)

#global and nonlocal
# def scope_test():
#     def do_local():
#         spam = "local spam"
#     def do_nonlocal():
#         nonlocal spam
#         spam = "nonlocal spam"
#     def do_global():
#         global spam
#         spam = "global spam"
#     spam = "test spam"
#     do_local()
#     print("After local assignment:", spam)
#     do_nonlocal()
#     print("After nonlocal assignment:", spam)
#     do_global()
#     print("After global assignment:", spam)
#
# scope_test()
# print("In global scope:", spam)

# gcount = 0
#
# def global_test():
#     gcount+=1
#     print(gcount)
# global_test()

# MAX_LINE_NUM = 100000;
#
# with open(r"data/lipsum.txt", 'w') as f:
#     for i in range(MAX_LINE_NUM):
#         f.write('{i}\n'.format(i=i))


#import time, threading

# 新线程执行的代码:
# import threading
# import time
# class timer(threading.Thread): #The timer class is derived from the class threading.Thread
#     def __init__(self, num, interval):
#         threading.Thread.__init__(self)
#         self.thread_num = num
#         self.interval = interval
#         self.thread_stop = False
#
#     def run(self): #Overwrite run() method, put what you want the thread do here
#         while not self.thread_stop:
#             print('Thread Object(%d), Time:%s\n' %(self.thread_num, time.ctime()))
#             time.sleep(self.interval)
#     def stop(self):
#         self.thread_stop = True
#
#
# def test():
#     thread1 = timer(1, 1)
#     thread2 = timer(2, 2)
#     thread1.start()
#     thread2.start()
#     time.sleep(10)
#     thread1.stop()
#     thread2.stop()
#     return
#
# if __name__ == '__main__':
#     test()


# import socket
#
# hostname = socket.gethostname()
# ip = socket.gethostbyname(hostname)
#
# print(hostname)
# print(ip)


# import logging
# logging.basicConfig(filename='temp/myapp.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
# # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')

# import logging
#
# # set up logging to file - see previous section for more details
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#                     datefmt='%m-%d %H:%M',
#                     filename='temp/myapp.log')
# # define a Handler which writes INFO messages or higher to the sys.stderr
# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# # set a format which is simpler for console use
# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# # tell the handler to use this format
# console.setFormatter(formatter)
# # add the handler to the root logger
# logging.getLogger('').addHandler(console)
#
# # Now, we can log to the root logger, or any other logger. First the root...
# logging.info('Jackdaws love my big sphinx of quartz.')
#
# # Now, define a couple of other loggers which might represent areas in your
# # application:
#
# logger1 = logging.getLogger('myapp.area1')
# logger2 = logging.getLogger('myapp.area2')
#
# logger1.debug('Quick zephyrs blow, vexing daft Jim.')
# logger1.info('How quickly daft jumping zebras vex.')
# logger2.warning('Jail zesty vixen who grabbed pay from quack.')
# logger2.error('The five boxing wizards jump quickly.')



# try:
#     import cPickle as pickle
# except:
#     import pickle
#
# class AA():
#     def a(self):
#         print("123")
#
# ddd = AA()
# data = pickle.dumps(ddd)
#
# print("hahah")
#
#
# data1 = pickle.unpack(data)
#
# print("haha")


# import struct
# import os
#
# # a = 200
# # b = 300
# # li = [a, b]
# # str = struct.pack('ii', *li)
# #
# # aa, bb = struct.unpack('ii',str)
# #
# values = (1, 'abc', 2.7)
# packed_data = struct.pack('i3sf', 1, 'abc'.encode('utf-8'), 2.7)
# unpacked_data = struct.unpack('i3sf', packed_data)
#
# print("haha")


# import pickle
# class Person:
#   def __init__(self,n,a):
#     self.name=n
#     self.age=a
#   def show(self):
#     print(self.name+"_"+str(self.age))
# # aa = Person("JGood", 2)
# #
# # temp = pickle.dump(aa)
# #
# # aa.show()
# # f=open('p.txt','wb')
# # pickle.dump(aa,f,0)
# # f.close()
# # #del Person
# # f=open('p.txt','rb')
# # bb=pickle.load(f)
# # f.close()
#
# a_dict = { x:str(x) for x in range(5) }
# serialized_dict = pickle.dumps(a_dict)
# # Send it through the socket and on the receiving end:
# a_dict = pickle.loads(serialized_dict)
# # bb.show()
#
# print("haha")

# dic1 = dict()
# dic1["ip"] = "localhost"
# dic2 = dict()
# dic2['filename'] = 'filename'
#
# dictest1 = dict()
# dictest1['hostname'] = '1'
# dictest1['detail'] = dic1
#
# dictest2 = dict()
# dictest2['hostname'] = '1'
# dictest2['detail'] = dic1
#
# li = []
#
# li.append(dictest1)
# li.append(dictest2)
#
# print('haha')
#
# import time
# if __name__ == '__main__':
#     time.sleep(1)
#     print("clock1:%s" % time.clock())
#     time.sleep(1.7)
#     print("clock2:%s" % time.clock())
#     time.sleep(1)
#     print( "clock3:%s" % time.clock())

import os
# aa = os.path.getsize('data/lipsum.txt')

# with open('data/lipsum.txt', 'rb') as f:
#     f.seek(0)
#     print(f.readline())

# from socket import *
# client = socket(AF_INET, SOCK_STREAM)
# serverIP = '192.168.3.93'
# serverPort = 5002
# client.connect((serverIP, serverPort))
#
# MAX_LINE_NUM = 30000000
#
# with open(r"lipsum.txt", 'w') as f:
#     for i in range(MAX_LINE_NUM):
#         f.write('{i}\n'.format(i=i))

import os
import sys
import glob
def dirTxtToLargeTxt(dir,outputFileName):
  '''从dir目录下读入所有的TXT文件,将它们写到outputFileName里去'''
  #如果dir不是目录返回错误
  if not os.path.isdir(dir):
    print("传入的参数有错%s不是一个目录", dir)
    return False
  #list all txt files in dir
  outputFile = open(outputFileName, "wb")

  textBlocks = glob.glob(os.path.join(dir,"*.txt"))

  fileNumArr = []
  for temp in textBlocks:
    fileNum = temp.split(".")[-2][-4:]
    fileNumArr.append(fileNum)
    fileNumArr.sort()

  fileNamePrifix = "lipsum"
  fileNamePostfix = ".txt"
  for fileNum in fileNumArr:
    fileName = dir + fileNamePrifix + str(fileNum) + fileNamePostfix
    print(fileName)
    inputFile = open(fileName, "rb")
    for line in inputFile:
      outputFile.write(line)

  # for txtFile in glob.glob(os.path.join(dir,"*")):
  #   print(txtFile)
  #   inputFile = open(txtFile, "rb")
  #   for line in inputFile:
  #     outputFile.write(line)
  return True
if __name__ =="__main__":
  # if len(sys.argv) < 3:
  #   print ("Usage:%s dir outputFileName", sys.argv[0])
  #   sys.exit()
  dir = "./data-5002/"
  outputFileName = "combine.txt"
  dirTxtToLargeTxt(dir, outputFileName)
