# -*- coding:utf-8 -*-
__author__ = 'Jackie'

"""
define some constant here
"""

#about the ip and port
MONITOR__SERVER_IP = "localhost" #monitor static ip and port
MONITOR__SERVER_PORT = 5001

PORT_START = 5001 # server ip port

BLOCK_SIZE = 1024*1024*16
# BLOCK_SIZE = 1024*128

#about the message type
from_client_01 = "01" #connect server upload file
from_client_02 = "02" #connect server download file

from_client_03 = "03" #connect monitor to get the upload file message
from_client_04 = "08" #connect monitor to get the download file message

from_server_01 = "05" #connect the monitor to say hi
from_server_02 = "06" #connect the monitor to be alive
from_server_03 = "07" #connect to the other server to back files


#文件块信息字段定义
FILE_NAME_SIZE = 20
FILE_NAME_NUMBER_SIZE = 4

# 头文件
HEAD_FILE_LENGTH = 73