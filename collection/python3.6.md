```shell
#支持类型提示 typing
{
def greeting(name: str) -> str:
	return 'Hello ' + name

#在函数greeting中，参数名称的类型为str，返回类型为str。 接受子类型作为参数。
#例子
>>> def gg(name:str)->str:
	return 'hello'+name

>>> gg('a')
'helloa'
>>> gg('bbb')
'hellobbb'
>>> gg(1)
Traceback (most recent call last):
  File "<pyshell#19>", line 1, in <module>
	gg(1)
  File "<pyshell#16>", line 2, in gg
	return 'hello'+name
TypeError: must be str, not int
>>> 


}

base64{

import base64
>>> base64.decodebytes(b'c3Vic2NyaWJlcjpTc01pbmkxQA==').decode('utf8')
'subscriber:SsMini1@'
>>> base64.encodebytes(b'subscriber:SsMini1@')
b'c3Vic2NyaWJlcjpTc01pbmkxQA==\n'
}
#给[1,2,3]加权重
random .choices([1,2,3],[1,1,10])

# asyncio
{
#http://www.cnblogs.com/styier/p/6415850.html  例子



#程序总共等待10s
import asyncio
async def print5s():
       print("开始运行！")
       await asyncio.sleep(5.0) #挂起后台运行
       print("结束运行！")
       
async def print10s():
       print("开始运行！")
       await asyncio.sleep(10.0) #挂起后台运行
       print("结束运行！")

loop = asyncio.get_event_loop()

loop.create_task(print5s())
loop.create_task(print10s())
loop.run_forever()

#程序总共等待5s
import asyncio
 
async def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    await asyncio.sleep(5.0)
    return x + y
 
async def print_sum(x, y):
    result = await compute(x, y)
    print("%s + %s = %s" % (x, y, result))
 
loop = asyncio.get_event_loop()
tasks = [print_sum(1,2),print_sum(3,4)]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

#程序总共等待2s
import asyncio

async def my_task(seconds):
    print("This task is take {} seconds to cpmplete".format(seconds))
    await asyncio.sleep(seconds)
    return "task finished"

if __name__ == "__main__":
    my_event_loop = asyncio.get_event_loop()
    tasks = []
    try:
        print("task creation started")
        task_obj1 = my_event_loop.create_task(my_task(seconds = 2))
        task_obj2 = my_event_loop.create_task(my_task(seconds = 2))
        task_obj3 = my_event_loop.create_task(my_task(seconds = 2))
        tasks = [task_obj1,task_obj2,task_obj3]		#创建事件循环的列表
        #my_event_loop.run_until_complete(tasks)
        my_event_loop.run_until_complete(asyncio.wait(tasks)) #创建事件循环的列表
    finally:
        my_event_loop.close()

#可以看出 是在同一个线程中执行的
import threading
import asyncio


async def hello():
    print('Hello world! (%s)' % threading.currentThread())
    asyncio.sleep(1)
    print('Hello again! (%s)' % threading.currentThread())

loop = asyncio.get_event_loop()
tasks = [hello(), hello()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()


#使用Process类控制子进程和StreamReader类从标准输出读取的示例。子过程由create_subprocess_exec()函数创建：
import asyncio.subprocess
import sys
 
@asyncio.coroutine
def get_date():
    code = 'import datetime; print(datetime.datetime.now())'
 
    # Create the subprocess, redirect the standard output into a pipe
    create = asyncio.create_subprocess_exec(sys.executable, '-c', code,
                                            stdout=asyncio.subprocess.PIPE)
    proc = yield from create
 
    # Read one line of output
    data = yield from proc.stdout.readline()
    line = data.decode('ascii').rstrip()
 
    # Wait for the subprocess exit
    yield from proc.wait()
    return line
 
if sys.platform == "win32":
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()
 
date = loop.run_until_complete(get_date())
print("Current date: %s" % date)
loop.close()


}
queue 队列
{


import queue
#测试定义类传入队列
class Foo(object):
    def __init__(self,n):
        self.n = n
new = queue.Queue(maxsize=3)
print('先进先出')
new.put(1)
new.put(Foo(1),timeout=2) # 超时时间后，抛出队列full异常
new.put([1, 2, 3],timeout=2)
print(new.full()) #判断队列是否满 True
#new.put("abc",timeout=1) #队列已满，再放报错
print(new.qsize()) # 查看当前队列长度
print(new.get())
print(new.get())
print(new.get())
print(new.empty()) #判断队列是否为空 True
#print(new.get_nowait()) #队列已空，取不到数据报异常
print('后进先出')
q = queue.LifoQueue() #指定使用LifoQueue
q.put(3)
q.put(2)
print(q.get_nowait())
print(q.get_nowait())

print('存入一个元组，第一个为优先级，第二个为数据，第三个默认超时时间')
new = queue.PriorityQueue(maxsize=3)
new.put((10,[1,2,3]))
new.put((5,"strings"))
new.put((20,"strings"))
print(new.get_nowait())
print(new.get_nowait())
print(new.get_nowait())


import threading, queue, time
#生产者消费者模型为了程序松耦合，多对多
def consumer(n):
    while True:
        print(" consumer [%s]  get task: %s" % (n, q.get()))
        time.sleep(1)  # 每秒吃一个
        q.task_done()  # get()1次通知队列减少1

def producter(n):
    count = 1
    while True:
        print("producter [%s] produced a new task : %s" % (n, count))
        q.put(count)
        count += 1
        q.join()  #消息阻塞 队列为空重新触发
        print("all task has been cosumed by consumers ...")

q = queue.Queue()
c1 = threading.Thread(target=consumer, args=[1, ])
c2 = threading.Thread(target=consumer, args=[2, ])
c3 = threading.Thread(target=consumer, args=[3, ])
p1 = threading.Thread(target=producter, args=["p1", ])
p2 = threading.Thread(target=producter, args=["p2", ])
c1.start()
c2.start()
c3.start()
p1.start()
p2.start()

}
####################################################################################################
#1.研究pty项目sh中，为什么在第一个pythonshell中导入ifconfig后能获取返回，两个伪终端如何传递数据库的？
#2.在子进程中执行shell后返回结果到父进程 在不使用subprocess的情况下，进程间怎么交互数据
####################################################################################################

1.os.popen() 调用的是subprocess 库，找到subprocess.Popen('dwad',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
{
def __init__(self, args, bufsize=-1, executable=None,
                 stdin=None, stdout=None, stderr=None,
                 preexec_fn=None, close_fds=_PLATFORM_DEFAULT_CLOSE_FDS,
                 shell=False, cwd=None, env=None, universal_newlines=False,
                 startupinfo=None, creationflags=0,
                 restore_signals=True, start_new_session=False,
                 pass_fds=(), *, encoding=None, errors=None):

感觉全是io库中的函数


os.openpty()                    # 打开一个新的伪终端对。返回 pty 和 tty 的文件描述符。
os.pipe()                       # 创建一个管道. 返回一对文件描述符(r, w) 分别为读和写
os.popen(command[, mode[, bufsize]])  # 从一个 command 打开一个管道
os.read(fd, n)                  # 从文件描述符 fd 中读取最多 n 个字节，返回包含读取字节的字符串，文件描述符 fd对应文件已达到结尾, 返回一个空字符串。
os.write(fd, str)               # 写入字符串到文件描述符 fd中. 返回实际写入的字符串长度
os.ttyname(fd)                  # 返回一个字符串，它表示与文件描述符fd 关联的终端设备。如果fd 没有与终端设备关联，则引发一个异常。

'''
os.dup2(fd，fd2，inheritable = True)
#将文件描述符fd重复到fd2，如有必要，关闭后者。
'''

>>> os.pipe() #8用于写，7用于读
(7, 8)
>>> os.write(8,b'1122')
4
>>> os.read(7,10)
b'1122'


>>> os.openpty()
(11, 12)
>>> os.ttyname(11)
'/dev/ptmx'
>>> os.ttyname(12) #并没有在linux上真实产生一个/dev/pts/9
'/dev/pts/9'

11是主，12是从
#任何从主设备的输入都会输出到从设备上


#! /usr/bin/env python
#coding=utf-8

import pty
import os
import select

def mkpty():
    # 打开伪终端
    master1, slave = pty.openpty()
    slaveName1 = os.ttyname(slave)
    master2, slave = pty.openpty()
    slaveName2 = os.ttyname(slave)
    print ('\nslave device names: ', slaveName1, slaveName2)
    return master1, master2

if __name__ == "__main__":

    master1, master2 = mkpty()
    while True:
	
	
        rl, wl, el = select.select([master1,master2], [], [], 1)
        for master in rl:
            data = os.read(master, 128)
            print ("read %d data." % len(data))
            if master==master1:
                os.write(master2, data)
            else:
                os.write(master1, data)



python3.4 test_pty.py &
#另一终端上执行				
root@api:/home/lgj/pty# echo 11 > /dev/pts/12
root@api:/home/lgj/pty# echo 11 > /dev/pts/11

#本终端显示
root@api:/home/lgj/pty# read 4 data.
the data: b'11\r\n'				
root@api:/home/lgj/pty# read 4 data.
the data: b'11\r\n'
#主从伪终端
>>> os.openpty()
(4, 5)
>>> os.ttyname(4)
'/dev/ptmx'
>>> os.ttyname(5)
'/dev/pts/9'
>>> os.write(4,b'ls\r\n')
4
>>> os.read(4,100)
b'ls\r\n\r\n'
>>> os.read(5,100)
b'ls\n'
>>> os.read(5,100)
b'\n'

#管道
>>> os.pipe()
(6, 7)
>>> os.write(7,str(1).encode('utf-8'))
1
>>> os.read(6,10)
b'1'

>>> a=open("lgj",'a')
>>> a.fileno() #文件句柄
8
>>> os.dup(8) #复制文件句柄
9

'''
os.dup2(fd，fd2，inheritable = True)
#将文件描述符fd重复到fd2，如有必要，关闭后者。
'''

命令tty 查看当前终端对应的设备
ps -ax 查看进程对应的控制台

pts(pseudo-terminal slave)是pty的实现方法，与ptmx(pseudo-terminal master)配合使用实现pty。
1、串行端口终端(/dev/ttySn)
2、伪终端(/dev/pty/)
3、控制终端(/dev/tty)
4、控制台终端(/dev/ttyn, /dev/console)
5 虚拟终端(/dev/pts/n)
/dev/tty代表当前tty设备，在当前的终端中输入 echo “hello” > /dev/tty ，都会直接显示在当前的终端中。

os.execv("/sbin/ifconfig",('-a',)) #可以输出ifconfig的返回

#应该是在子进程中执行os.execv("/sbin/ifconfig",('-a',)) 然后读取输出。

'''
stdin,stdout是设置是否打开这些管道，如果他的值是subprocess.PIPE的话，就会打开,同stdin一样的还有stderr
参数stdin, stdout, stderr分别表示程序的标准输入、输出、错误句柄。他们可以是PIPE，文件描述符或文件对象，也可以设置为None，表示从父进程继承。
可以在Popen()建立子进程的时候改变标准输入、标准输出和标准错误，并可以利用subprocess.PIPE将多个子进程的输入和输出连接在一起，构成管道(pipe):

import subprocess
child1 = subprocess.Popen(["ls","-l"], stdout=subprocess.PIPE)
child2 = subprocess.Popen(["wc"], stdin=child1.stdout,stdout=subprocess.PIPE)
out = child2.communicate()
print(out)
# http://www.cnblogs.com/icejoywoo/p/3627397.html
# http://www.cnblogs.com/yangxudong/p/3753846.html
在POSIX上，subprocess类使用os.execvp（） - 类行为来执行子程序。 在Windows上，类使用Windows CreateProcess（）函数
'''
sys.stdin.fileno()
>>> import os
>>> import sys
>>> sys.stdin.fileno()
0
>>> os.ttyname(0)
'/dev/pts/2'
>>> os.ttyname(1)
'/dev/pts/2'
>>> os.ttyname(2)
'/dev/pts/2'
>>> os.ttyname(3)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
OSError: [Errno 9] Bad file descriptor
>>> 
>>> os.openpty()
(4, 5)
>>> os.ttyname(4)
'/dev/ptmx'
>>> os.ttyname(5)
'/dev/pts/10'

fd_r_list, fd_w_list, fd_e_list = select.select(rlist, wlist, xlist, [timeout])
 
参数： 可接受四个参数（前三个必须）
rlist: wait until ready for reading
wlist: wait until ready for writing
xlist: wait for an “exceptional condition”
timeout: 超时时间

返回值：三个列表
 
select方法用来监视文件描述符(当文件描述符条件不满足时，select会阻塞)，当某个文件描述符状态改变后，会返回三个列表
1、当参数1 序列中的fd满足“可读”条件时，则获取发生变化的fd并添加到fd_r_list中
2、当参数2 序列中含有fd时，则将该序列中所有的fd添加到 fd_w_list中
3、当参数3 序列中的fd发生错误时，则将该发生错误的fd添加到 fd_e_list中


}
#os.fork()
{
ret = os.fork()
if ret == 0:
    child_suite # 子进程代码
else:
    parent_suite # 父进程代码
	
#Python中的fork() 函数可以获得系统中进程的PID ( Process ID )，返回0则为子进程，否则就是父进程，然后可以据此对运行中的进程进行操作；	
}

#异步执行
os.fork() 
{

import os
import sys
import time
 
processNmae = '父进程'
print ("Program executing ntpid:%d,processNmae:%s"%(os.getpid(),processNmae))
#attempt to fork child process
try:
    forkPid = os.fork()
except OSError:
    sys.exit("Unable to create new process.")
# Am I parent process?
if forkPid != 0:
    processName = "父进程"
    print ("Parent executingn"+"tpid:%d,forkPid:%d,processNmae:%s"%(os.getpid(), forkPid,processName))
# Am I child process?
elif forkPid == 0:
        processName = "子进程"
        print ("Child executingn" + "tpid: %d, forkPid: %d, processName: %s" % (os.getpid(), forkPid,processName))
        print ("Process finishingntpid: %d, processName: %s" % (os.getpid(), processName))
		
		
''' 都能打印在一起，应该是子进程继承了父进程的输入输出端
root@api:/home/lgj/pty# python3.4 cmd_pty2.py 
Program executing ntpid:121728,processNmae:父进程
Parent executingntpid:121728,forkPid:121729,processNmae:父进程
Child executingntpid: 121729, forkPid: 0, processName: 子进程
Process finishingntpid: 121729, processName: 子进程

#########################下面这段话很重要##############################
程序每次执行时，操作系统就会创建一个新的进程来运行程序指令。进程还可以调用os.fork，要求操作系统新建一个进程。“父进程”是调用os.fork的进程。父进程所创建的任何进程都是子进程。每个进程都有一个不重复的“进程ID号”，或称“pid”，它对进程进程进行标识。进程调用fork函数时，操作系统会新建一个子进程，它本质上与父进程完全相同。子进程从父进程继承了多个值的拷贝，比如全局变量和环境变量。两个进程唯一的区别就是fork的返回值。
child（子）进程接收返回值为0，而父进程接收子进程的pid作为返回值。调用fork函数后，两个进程并发执行同一个程序，首先执行的是调用了fork之后的下一行代码。父进程和子进程既并发执行，又相互独立；也就是说，它们是“异步执行”的。
'''

'''
pid, fd =os.forkpty（）
分叉子进程，使用新的伪终端作为子进程的控制终端。 返回一对(pid,fd)，其中pid在新子进程中为0，在父进程中为新子进程在父进程中的id，fd是伪终端的主端的文件描述符。 对于更便携的方法，使用pty模块。 如果出现错误，则引发OSError。
>>> os.forkpty()
(123573, 4)
>>> os.ttyname(4)
'/dev/ptmx'
'''



}

#子进程与父进程(pid,ppid)
{
import os
import sys
def runpager():
    fdin, fdout = os.pipe()
    pid = os.fork()
    print("fdin,fdout,pid,ppid",fdin,fdout,pid,os.getppid())
    print("sys.stdin.fileno(),sys.stdout.fileno(),sys.stderr.fileno()",sys.stdin.fileno(),sys.stdout.fileno(),sys.stderr.fileno())
    if pid == 0:
        os.close(fdin)
        os.dup2(fdout, sys.stdout.fileno())
        os.dup2(fdout, sys.stderr.fileno())
        os.close(fdout)
        return
    os.dup2(fdin, sys.stdin.fileno())
    os.close(fdin)
    os.close(fdout)
    #os.execvp('/bin/ls', ['/bin/ls', '-l'])
    os.execvp('/bin/sleep', ['/bin/sleep','10'])

a=input("a=")
print("pid",os.getpid())	
print("ppid",os.getppid())	
runpager()

'''
##########################################################################

root@api:/home/lgj/pty# python3.4 cmd_pty1.py 
a=1
pid 118983
ppid 109823
fdin,fdout,pid,ppid 3 4 119005 109823
sys.stdin.fileno(),sys.stdout.fileno(),sys.stderr.fileno() 0 1 2
fdin,fdout,pid,ppid 3 4 0 118983
sys.stdin.fileno(),sys.stdout.fileno(),sys.stderr.fileno() 0 1 2


root@api:~# ps -ef|grep python
root     118983 109823  0 16:29 pts/10   00:00:00 python3.4 cmd_pty1.py
root@api:~# ps -ef|grep sleep
root     118996 115824  0 16:29 pts/2    00:00:00 grep --color=auto sleep
root@api:~# 
##输入a后
root@api:~# ps -ef|grep python
root     119005 118983  0 16:29 pts/10   00:00:00 [python3.4] <defunct>
root@api:~# ps -ef|grep sleep
root     118983 109823  0 16:29 pts/10   00:00:00 /bin/sleep 10
root@api:~# 


#exec 函数都执行一个新的程序，然后用新的程序替换当前子进程的进程空间，而该子进程从新程序的main函数开始执行。在Unix下，该新程序的进程id是原来被替换的子进程的进程id。在原来子进程中打开的所有描述符默认都是可用的，不会被关闭。
##########################################################################
root@api:~# ps -ef|grep python
root     115968 115967  0 16:05 pts/10   00:00:00 [python3.4] <defunct>
root     115974 115824  0 16:06 pts/2    00:00:00 grep --color=auto python
         PID    PPID
UID     //用户ID、但输出的是用户名
PID     //进程的ID
PPID    //父进程ID

>>> import os
>>> os.getuid()
0
>>> os.getpid()
116485
>>> os.getppid()
115824

root@api:~# ps -ef|grep python
root     116485 115824  0 16:10 pts/2    00:00:00 python3.4
root     116565 116523  0 16:11 pts/11   00:00:00 grep --color=auto python

'''

}


#Python进程间通信之匿名管道
{

#管道是一个单向通道,有点类似共享内存缓存.管道有两端,包括输入端和输出端.对于一个进程的而言,它只能看到管道一端,即要么是输入端要么是输出端.

os.pipe()返回2个文件描述符(r, w),表示可读的和可写的.示例代码如下:

#!/usr/bin/python
import time
import os

def child(wpipe):
    print('hello from child', os.getpid())
    while True:
        msg = 'how are you\n'.encode()
        os.write(wpipe, msg)
        time.sleep(1)

def parent():
    rpipe, wpipe = os.pipe()
    pid = os.fork()
    if pid == 0:
        child(wpipe)
        assert False, 'fork child process error!'
    else:
        os.close(wpipe)
        print('hello from parent', os.getpid(), pid)
        while True:
            recv = os.read(rpipe, 32)
            print (recv)

parent()
输出如下:

('hello from parent', 5053, 5054)
('hello from child', 5054)
how are you

how are you

how are you

how are you
我们也可以改进代码,不用os.read()从管道中读取二进制字节,而是从文件对象中读取字符串.这时需要用到os.fdopen()把底层的文件描述符(管道)包装成文件对象,然后再用文件对象中的readline()方法读取.这里请注意文件对象的readline()方法总是读取有换行符’\n’的一行,而且连换行符也读取出来.还有一点要改进的地方是,把父进程和子进程的管道中不用的一端关闭掉.

#!/usr/bin/python
import time
import os

def child(wpipe):
    print('hello from child', os.getpid())
    while True:
        msg = 'how are you\n'.encode()
        os.write(wpipe, msg)
        time.sleep(1)

def parent():
    rpipe, wpipe = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(rpipe)
        child(wpipe)
        assert False, 'fork child process error!'
    else:
        os.close(wpipe)
        print('hello from parent', os.getpid(), pid)
        fobj = os.fdopen(rpipe, 'r')
        while True:
            recv = fobj.readline()[:-1]
            print (recv)
			
parent()
输出如下:

('hello from parent', 5108, 5109)
('hello from child', 5109)
how are you
how are you

#如果要与子进程进行双向通信,只有一个pipe管道是不够的,需要2个pipe管道才行.以下示例在父进程新建了2个管道,然后再fork子进程.os.dup2()实现输出和输入的重定向.spawn功能类似于subprocess.Popen(),既能发送消息给子进程,由能从子子进程获取返回数据. 
​

#!/usr/bin/python
#coding=utf-8
import os, sys

def spawn(prog, *args):
    stdinFd = sys.stdin.fileno()
    stdoutFd = sys.stdout.fileno()

    parentStdin, childStdout = os.pipe()
    childStdin, parentStdout= os.pipe()

    pid = os.fork()
	#程序分叉，子进程中关闭父进程的文件符并将自己用到的文件符重定向到通道，父进程中关闭子进程的文件符并将自己用到的文件符重定向到通道
    if pid: #父进程
        os.close(childStdin)
        os.close(childStdout)
        os.dup2(parentStdin, stdinFd)#输入流绑定到管道,将输入重定向到管道一端parentStdin
        os.dup2(parentStdout, stdoutFd)#输出流绑定到管道,发送到子进程childStdin
    else:   #子进程
        os.close(parentStdin)
        os.close(parentStdout)
        os.dup2(childStdin, stdinFd)#输入流绑定到管道
        os.dup2(childStdout, stdoutFd)
        args = (prog, ) + args
        os.execvp(prog, args)
        assert False, 'execvp failed!'

if __name__ == '__main__':
    mypid = os.getpid()
    spawn('python', 'pipetest.py', 'spam')

    print 'Hello 1 from parent', mypid #打印到输出流parentStdout, 经管道发送到子进程childStdin
    sys.stdout.flush()
    reply = raw_input()
    sys.stderr.write('Parent got: "%s"\n' % reply)#stderr没有绑定到管道上

    print 'Hello 2 from parent', mypid
    sys.stdout.flush()
    reply = sys.stdin.readline()#另外一种方式获得子进程返回信息
    sys.stderr.write('Parent got: "%s"\n' % reply[:-1]) 

pipetest.py代码如下:

#coding=utf-8
import os, time, sys

mypid = os.getpid()
parentpid = os.getppid()
sys.stderr.write('child %d of %d got arg: "%s"\n' %(mypid, parentpid, sys.argv[1]))

for i in range(2):
    time.sleep(3)
    recv = raw_input()#从管道获取数据,来源于父经常stdout
    time.sleep(3)
    send = 'Child %d got: [%s]' % (mypid, recv)
    print(send)#stdout绑定到管道上,发送到父进程stdin
    sys.stdout.flush()
输出:

child 7265 of 7264 got arg: "spam"
Parent got: "Child 7265 got: [Hello 1 from parent 7264]"
Parent got: "Child 7265 got: [Hello 2 from parent 7264]"

}


#伪终端tty\pty
{
import os
import sys
import time
import pty
import select
#################使用pty和select 处理子进程的返回， 这样的用例是不能在shell中一步一步敲的，因为存在两个进程
pid, fd = pty.fork()
print(pid) #你会发现这里打印了两个值
mystr=""
#处理子进程
if pid == 0:
	os.execvp('/bin/ls', ['/bin/ls', '-l'])
#处理父进程，监听子进程中的返回	
if pid !=0:
	while True:
		i, o, e = select.select([fd], [], [], 2)
		if fd in i:
			try:
				bytes = os.read(fd,600)
				mystr=bytes.decode("utf-8")+mystr
				print(bytes.decode("utf-8"))
			except OSError:
				print("子进程监听结束")
				break
#继续处理父进程
print("==============")
print(mystr) #父进程中取得了子进程的返回！

'''
pid, fd = pty.fork()
程序分叉。 将子进程的控制终端连接到伪终端，返回值为(pid，fd)。注意: 子进程获取pid为0，fd在子进程中是无效的。fork返回非0的pid是子进程的在父进程中的pid，fd是连接到子进程的控制终端（以及子进程的标准输入和输出）的文件描述符。

fd_r_list, fd_w_list, fd_e_list = select.select(rlist, wlist, xlist, [timeout])
 select方法用来监视文件描述符(当文件描述符条件不满足时，select会阻塞)，当某个文件描述符状态改变后，会返回三个列表
1、当参数1 序列中的fd满足“可读”条件时，则获取发生变化的fd并添加到fd_r_list中
2、当参数2 序列中含有fd时，则将该序列中所有的fd添加到 fd_w_list中
3、当参数3 序列中的fd发生错误时，则将该发生错误的fd添加到 fd_e_list中
'''
#################使用os.fork,pipe 处理子进程的返回，不使用pty又怎么写呢？pty.fork会把子进程的fd返回给父进程读取，这样很方便进程间的交流。
'''
os.dup2(fd，fd2，inheritable = True)  #最大的作用就是重定向，将fd2重定向到fd。
#将文件描述符fd重复到fd2，如有必要，关闭后者。
'''
##通常一个进程打开伪终端设备，然后调用fork。子进程建立了一个新会话，打开一个相应的伪终端从设备，将其描述符复制到标准输入、标准输出和标准出错，然后调用exec。伪终端从设备成为子进程的控制终端。
# encoding: utf-8
import os
import sys
import time

def child(master, slave):
    os.close(master) #关闭不需要的主设备，因为主设备是给父进程传送指令到子进程的
    os.dup2(slave, 0) #最大的作用就是重定向，将子进程中的0,1,2 都重定向到从端。
    os.dup2(slave, 1)
    os.dup2(slave, 2)
    os.execvp("/bin/bash", ["bash", "-l", "-i"])
	#os.execvp("/bin/ls", ["bash", "-l", "-i"])


def parent():
    master, slave = os.openpty() #新建虚拟终端，将从端分配给子进程，主端给主进程。#打开一个新的伪终端对。 分别为pty和tty返回一对文件描述符（主，从）
    new_pid = os.fork()
    if new_pid == 0:
        child(master, slave)

    time.sleep(0.1)
    os.close(slave) #关闭主进程中的从设备

    os.write(master, b"fg\n") #把作业放置前台执行，下发指令到子进程，将子进程中的执行放到前台
    time.sleep(0.1)
   # _ = os.read(master, 1024) #>>见后面的解析1

    #os.write(master, (sys.argv[1] + "\n").encode('utf8'))
    time.sleep(0.1)
    lines = []
    while True:
        tmp = os.read(master, 1024)
        tmp=tmp.decode('utf8')
        lines.append(tmp)
        if len(tmp) < 1024:
            break
    output = "".join(lines)
    output = "\n".join(output.splitlines()[1:])
    print (output)

parent()

'''
#执行结果
解析1，注释掉后会多打印这些东西。这些是父进程中的多余数据，可以先读出丢弃
bash: no job control in this shell
root@api:/home/lgj/pty# fg
bash: fg: no job control
root@api:/home/lgj/pty# ll

bg（将作业放置于后台执行）（在前台执行时间过长，则可以按ctrl+z，暂停进程，用bg放其至后台）
bg 作业ID
fg（把作业放置前台执行）
jobs（查看后台作业）

#http://www.cnblogs.com/nufangrensheng/p/3577853.html
##通常一个进程打开伪终端设备，然后调用fork。子进程建立了一个新会话，打开一个相应的伪终端从设备，将其描述符复制到标准输入、标准输出和标准出错，然后调用exec。伪终端从设备成为子进程的控制终端。

对于ssh，telnet等远程登录程序而言，当你ssh到某个sshd服务器上去时，这个sshd会打开一个伪终端主设备，然后fork出一个子进程，在子进程中打开一个从设备，
这样，主进程和子进程之间就可以通过伪终端的主从设备进行交流，任何从主设备的输入都会输出到从设备上
使用主从伪终端之后，当sshd收到指令时会将指令输入到主设备，然后主设备会把执行输出到从设备，这样就相当于指令输入到了从设备，而从设备是和某个shell连接的,从而这个指令或者毫无意义的字符串就被发往了远程的shell去解释
'''

#使用 python3.4 cmd_pty1.py ls

}

{
try ... except 语句可以带有一个 else子句 ，该子句只能出现在 有 except 子句之
后。 try语句没有出现异常时，还想要行执行一些代码，可以使这个子句。例 :
for arg in sys.argv[1:]:
	try:
		f = open(arg, ’r’)
	except IOError:
		print(’cannot open’, arg)
	else:
		print(arg, ’has’, len(f.readlines()), ’lines’)
		f.close()
#例子
def dome():
	try:
		a=7
		print(1)
	except OSError:
		print(2)
	else:
		print(3)
		return a
	a=8
	print(5)
	return a

print(dome())


'''result
1
3
7
'''

}
双通道
{
#!/usr/bin/python
import time
import os

def child(wpipe,rpipe1):
	print("""child's pid:""", os.getpid())
	for x in range(100):
		print("子程序读取到:",os.read(rpipe1,1024))
		msg = (str(x)+'from son\n').encode()
		print("子进程发送:")
		os.write(wpipe, msg)
		time.sleep(1)

def parent():
	rpipe, wpipe = os.pipe() #子进程的写，和父进程的读
	rpipe1, wpipe1 = os.pipe() #父进程的写，和子进程的读
	pid = os.fork()
	if pid == 0:
		os.close(rpipe)
		os.close(wpipe1)
		child(wpipe,rpipe1)
		assert False, 'fork child process error!'
	else:
		os.close(wpipe)
		os.close(rpipe1)
		print("""parent,child's pid:""", os.getpid(), pid)
		fobj = os.fdopen(rpipe, 'r')
		for x in range(100):
			print("父进程发送:")
			os.write(wpipe1,(str(x)+'from father\n').encode())
			print("父进程读取:")
			print (fobj.readline())
			
parent()
}

蒙提霍尔问题
{
"""蒙提霍尔问题:
有一个游戏 节目，参赛者会看见三扇关闭了的门，其中一扇的后面有一辆汽车，
选中后面有车的那扇门就可以赢得该汽车，而另外两扇门后面则各藏有一只山羊。
当参赛者选定了一扇门，但未去开启它的时候，节目主持人开启剩下两扇门的其中一扇，
露出其中一只山羊。主持人其后会问参赛者要不要换另一扇仍然关上的门。
问题是：换另一扇门会否增加参赛者赢得汽车的机会率？换与不换赢得汽车的概率分别是多少？
"""
import random
def guess(ischange):
       wintimes=0
       for a in range(1,1000): #游戏进行1000次
              carid=random.randint (0,2)
              yourguessid=random.randint (0,2)
              
              if carid==yourguessid: #第一次选择就是汽车，主持人随机开一个空门
                     openid=[x for x in range(0,3) if x !=carid][random.randint (0,1)]
              if carid !=yourguessid: #第一次选择不是汽车，主持人开另一个空门
                     for b in range(0,3):
                            if b!=yourguessid and b!=carid:
                                   openid=b
              #print("主持人开启一门后,carid,yourguessid,openid:",carid,yourguessid,openid)
              if ischange:
                     for c in range(0,3):
                            if c != openid and c != yourguessid:
                                   yourguessid=c
                                   #print(yourguessid)
                                   break
              #print("交换后,carid,yourguessid,openid:",carid,yourguessid,openid)
              if carid==yourguessid:
                     wintimes+=1
       print("wintimes:",wintimes)

print("不换赢的次数:")
guess(False)
print("换后赢的次数:")
guess(True)

"""
被主持人打开一个有羊的门之后，剩下的两个的概率不是各50%，因为已不是随机概率了(已被知情的主持人处理过)。
换另一个赢的概率是2/3，要换。

也许有人对此答案提出质疑，认为在剩下未开启的两扇门后有汽车的概率都是1/2，因此不需要改猜。为消除这一质疑，
不妨假定有10扇门的情形，其中一扇门后面有一辆汽车，另外9扇门后面各有一只山羊。
当竞猜者猜了一扇门但尚未开启时，主持人去开启剩下9扇门中的8扇，露出的全是山羊。
显然：原先猜的那扇门后面有一辆汽车的概率只是1/10，这时改猜另一扇未开启的门赢得汽车的概率是9/10。

若主持人不知情，则概率无变化。剩余两门：1/2,1/2，无放回抽样类似。
若主持人知情，概率就会发生变化。剩余两门：未开门的概率为2/3，1/3，非概率事件。

其实这个问题根本就不复杂，大家无论说50%还是66.6%都没有错，因为驳论的关键就在整个事件的条件设置上！
只是多数人不在意提问的所基于的整个条件设置，或者提出这个问题的人没有强调或者交代清楚整个设置，所以才很容易出现不一样的理解和答案。
关键还是在于条件混淆了大家思考的逻辑的起始点还有时间点
 """
#参考博客
http://www.cnblogs.com/antineutrino/p/4821580.html

}


```