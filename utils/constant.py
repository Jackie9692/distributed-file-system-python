# -*- coding:utf-8 -*-
__author__ = 'Jackie'

"""
define some constant here
"""

#about the ip and port
MONITOR__SERVER_IP = "localhost" #monitor static ip and port
MONITOR__SERVER_PORT = 5001

SERVER_IP_LENGTH = 15 #255.255.192.108
SERVER_PORT_LENGTH = 5 #65535

PORT_START = 5001 # server ip port

BLOCK_SIZE = 1024*1024*16
# BLOCK_SIZE = 1024*128

ONCE_READ_FILE_SIZE = 1024

#about the message type
from_client_01 = "01" #connect server upload file
from_client_02 = "02" #connect server download file

from_client_03 = "03" #connect monitor to get the upload file message
from_client_04 = "08" #connect monitor to get the download file message

from_server_01 = "05" #connect the monitor to say hi
from_server_02 = "06" #connect the monitor to be alive
from_server_03 = "07" #connect to the other server to back files
# from_server_01 = "09" #connect server to upload file


#文件块信息字段定义
FILE_NAME_LENGTH = 20
FILE_NAME_NUMBER_LENGTH = 4

# 头文件
HEAD_FILE_LENGTH = 147


