# distributed-file-system-python
分布式文件系统文档1.0
1.系统简介

本系统主要实现了在分布式文件系统中的文件的自动分块上传和下载。其实例分为三个部分:Monitor、Server和Client。Monitor相当于name node，用来监听Server的存活状态，并维护文件块在Server上的分布。Server相当于data node，用来存储、备份文件块。Client在上传和下载文件之前，会先跟Monitor进行通信，获取Server的地址和文件块与Server之间的关系，接着再连接到Server上进行文件上传或者下载。

2.主要算法与设计

1)客户端文件上传与下载线程任务分配
Client 类中通过 self.uploadFileThreadNum self.downloadFileThreadNum控制上传与下载的最大线程数目，customer.py中114—142行，实现了每个线程上传文件块数基本相同的目标，一定程度上实现了负载均衡。例self.uploadFileThreadNum=4， blockSize = 18时,四个线程分别上传文件块下标1-5,6-10,11-14,15-18，块数分别为5,5,4,4.
2)服务器之间文件备份
当客户端上传文件时，客户端首先向Monitor发送请求，Monitor根据服务器的活跃情况，制定上传策略，具体策略分为两种，当服务器有4台时，前两台服务器通过客户端直接上传文件（整个文件大小），前两台服务器在接收文件的同时，向后台发送备份文件。例如，文件可分为17块，则前两台服务器分别接收1-9,10-17，后两台分别接收前两台服务器的备份，即为接收1-9,10-17。当只有3台服务器工作时，第三台进行整个文件的备份，及接收1-17.具体实现在customer.py第74行，通过”backServerIP”, “backServerPort”向目标服务器的上传数据的时候，同时告知服务器进行备份。
3)服务器状态的刷新以及Monitor对服务器状态的检查
先启动Monitor服务，每当有新的服务器启动时，首先向服务器发送连接信息，Monitor会将服务器的状态保存在一个数组中self.aliveServerData，而在self.fileInfo中保存文件的名称，块大小等信息(注，支持多次上传)，而Monitor会开启一个线程，每间隔2.5秒检查self.aliveServerData中每个服务器的最新连接时间，如果跟现在的时间相比超过3秒则进行删除操作，包括self.aliveServerData中本身服务器的信息，还有self.fileInfo所有文件中包含存储在该服务器的存储信息。详见Monitor.py中checkServerStatus函数。
4)客户端，服务器，Monitor之间消息类型的定义
为了实现客户端，服务器以及Monitor之间的不同访问情况，特定义了以下八种消息类型。

消息编号	消息描述
from_Client_01 = "01"	connect Server to upload file
from_Client_02 = "02"	connect Server to download file
from_Client_03 = "03"	connect Monitor to get the upload file message
from_Client_04 = "04"	connect Monitor to get the download file message
from_Server_01 = "05"	connect the Monitor to say hi
from_Server_02 = "06"	connect the Monitor to be alive
from_Server_03 = "07"	connect to the other Server to back files

3.实验参数设置

操作系统：Windows、Linux、Mac OS均可
所需环境：Python 3
Monitor：1台
Server：4台（其中2台用于存储数据，2台用于备份数据）
Client：2台（从其中1台上传数据，并从另外1台下载下来）
所传文件大小：937M和3745M
文件块大小：128MB
并发线程数：上传10个，下载10个

4.实验结果

通过MD5校验工具hash.exe验证上传前的文件和下载后的文件保持一致。
实验
编号
	大小(M)	服务器
数量	上传时间	上传平均速度M/s	下载
时间	上传平均速度M/s	带宽
占比

1	936	3	0:01:26.91	10.75	0:00:48.84	19.16	100%
2	3745	3	0:05:24.82	11.52	0:03:11.21	19.58	100%
3	936	4	0:01:06.10	14.16	0:00:44.33	21.11	100%
4	3745	4	0:04:26.24	14.07	0:03:19.97	18.73	100%

由实验可知，3台服务器上传速度大概在11M/s，4台时约为14M/s,e而下载速度约在19.5M/s。实验1，2对比3,4类比在不同服务器数目下的上传和下载情况，1,2可以分别看做3，4宕机之后的情况，显然4台服务器情况比3台服务器上传的速度要快。由3,4可以看出文件较大的情况下，文件的平均下载速度较小，因为在文件块下载完成之后，本地需要进行一个文件的组装，需要耗费不少的时间。

5.项目小结

项目在服务器数量固定，上传和下载过程中服务器不出异常的情况下，就没有太大难度了。为了实现功能，主要学习了socket编程和多线程并发编程。本项目选用了python作为编程语言，代码简洁，有效代码量不超过700行，这是一般采用Java所不能比的。当然，python代码只能在单个cpu上执行，计算处理速度较慢，但本项目的的瓶颈主要在于IO和网络速度，并未对整体效率上造成不良影响。
实验环境
操作系统：Windows、Linux、Mac OS均可
所需环境：Python 3
Monitor：1台
Server：4台（其中2台用于存储数据，2台用于备份数据）
Client：2台（从其中1台上传数据，并从另外1台下载下来）

How to run:
运行步骤
1.在所有的服务器中配置Python 3的环境。
2.修改./utils/constant.py文件第9行的IP地址（设为Monitor的IP地址）。Server、Client与Monitor连接后，Monitor会记录它们的IP并且广播给其他机器。
3.将修改好参数的原始代码分发到所有的服务器上。
4.在Monitor上执行"python monitor.py"。
5.在Server上执行"python server.py"。
6.在Client上执行"python client.py"。

实验一：上传文件
将需要传输的文件（如office.iso）放到client的目录中，然后在client的命令行中输入"upload"，回车，再输入"office.iso"。查看client、server的日志，记录下实验结果。

实验二：下载文件
在另外一台服务器上开启client，并在命令行中输入"download"，回车，再输入"office.iso"，文件块会下载到当前目录的tmp文件夹进行拼装，拼装好后会放置在download文件夹。使用hash.exe工具比较上传前和下载后的文件的MD5码有没有变动。查看client、server的日志，记录下实验结果。

实验三：下载文件（1台服务器宕机）
关闭一台server的python实例（存储server、备份server均可），然后重复实验二的步骤，记录下实验结果。
