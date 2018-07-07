# -*- coding:utf-8 -*-
#!/bin/env python
import os
import time
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen
import tornado.httpclient
import tornado.concurrent
import tornado.ioloop
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from tornado.options import define, options
import sys

reload(sys)
sys.setdefaultencoding('utf8')

"""
https://blog.csdn.net/chenyulancn/article/details/45888949 �ο�����չ
https://blog.csdn.net/hjhmpl123/article/details/53673108

curl http://localhost:8000/sleep
curl http://localhost:8000/justnow

��2��url,һ���Ǻ�ʱ������һ���ǿ��Ի���˵��Ҫ���̷��ص�����,ϣ�����ʺ�ʱ�����󲻻�Ӱ��Ҳ���ᱻ�����˵�����
רҵ�㽲����:�����tornado�����첽�ķ�ʽ����ͬ������?

"""


define("port", default=8000, help="run on the given port", type=int)

class My(object):
    def __init__(self):
        self.executor = ThreadPoolExecutor(2)   #��������Ϊ1��0

    @run_on_executor
    def f(self):
        print(os.path.join(os.path.dirname(__file__), 'python'))
        time.sleep(2)
        print(10)
        return 1,2,3

    @run_on_executor
    def f1(self):
        time.sleep(1)
        print(15)
        return 4,5,6    #��Ҫ yield 4,5,6

    @run_on_executor
    def f2(self):
        time.sleep(1.5)
        print('hello, world1')
        f11=self.f1()
        f12=self.f()
        a,b,c= f11.result()
        d,e,f= f12.result()
        # a,b,c= yield self.f1()    # �����ǲ����Ե�
        # d,e,f= yield self.f()
        print "a,b,c:",a,b,c
        print "d,e,f:",d,e,f
        print('hello, world2')
        return 'success',a+b+c+d+e+f    #��Ҫ yield 'success',a+b+c+d+e+f

class SleepHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        #yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + 5)
        m = My()
        result, m = yield tornado.gen.maybe_future(m.f2())
        yield self.write({"result":result, "sum":m})


class JustNowHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("i hope just now see you")


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
        (r"/sleep", SleepHandler), (r"/justnow", JustNowHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()