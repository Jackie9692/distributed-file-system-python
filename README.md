# distributed-file-system-python
Brief introduction:

    本系统主要实现了在分布式文件系统中的文件的自动分块上传和下载。其实例分为三个部分:Monitor、Server和Client。Monitor相当于name node，用来监听Server的存活状态，并维护文件块在Server上的分布。Server相当于data node，用来存储、备份文件块。Client在上传和下载文件之前，会先跟Monitor进行通信，获取Server的地址和文件块与Server之间的关系，接着再连接到Server上进行文件上传或者下载。


How to run:

运行步骤:
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
