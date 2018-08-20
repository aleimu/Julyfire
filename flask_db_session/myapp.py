# -*- coding:utf-8 -*-
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import scoped_session

import time
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@172.16.4.120:3306/mytest?charset=utf8'
db = SQLAlchemy(app)    # db.init_app(app) 提供了两种将app与db绑定的方式，具体区别看文档，这里不做分析
db_session = db.session

def instrument(name):
    def do(self, *args, **kwargs):
        return getattr(self.registry(), name)(*args, **kwargs)
    return do

class role(db.Model):
    id = db.Column(db.INT, primary_key=True,autoincrement=True)
    name = db.Column(db.String(99), unique=False)
    name_cn = db.Column(db.String(99), unique=False)

    def __init__(self, name, name_cn):
        self.name = name
        self.name_cn = name_cn

    def __repr__(self):
        return '<User %r>' % self.name

# db.create_all()

@app.route('/add1')
def add1():
    print("db.session:", vars(db_session))
    print("id(db_session)",db_session)
    test_role1 = role('supervisol', '11')
    # test_role2 = role('your try', '11')
    db_session.add(test_role1)
    #db_session.add(test_role2)
    #db.session.commit() # 这里不去提交
    # time.sleep(60)
    return "add1"

@app.route('/add2')
def add2():
    print("db.session:",vars(db.session))
    print("id(db_session)", db_session)
    test_role1 = role('supervisol', '22')
    #test_role2 = role('your try', '22')
    db_session.add(test_role1)
    #db_session.add(test_role2)
    db_session.commit()
    # time.sleep(60)
    return "add2"

# db_session在两个route中不会相互影响，虽然db_session是同一个
# 在 flask_sqlalchemy.SQLAlchemy类的定义中有self.session = self.create_scoped_session(session_options)以及最后返回的
# return orm.scoped_session(self.create_session(options), scopefunc=scopefunc)可以追溯到
# sqlalchemy.orm.session与sqlalchemy.orm.scoped_session的关系
# 可以参考 http://www.cnblogs.com/ctztake/p/8277372.html 会为每一个请求创建独立的session由线程id或者
# _app_ctx_stack.__ident_func__为标记
# 这篇也是很有参考意义的 https://stackoverflow.com/questions/39480914/why-db-session-remove-must-be-called
# 当然看前人的路最方便基本上把前后都说清楚了https://blog.csdn.net/yueguanghaidao/article/details/40016235
"""
# 绑定app然后初始化sql配置
if app is not None:
    self.init_app(app)
    
# 使用钩子，当请求结束后若没有配置自动提交，则移除此session
@app.teardown_appcontext
def shutdown_session(response_or_exc):
    if app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']:
        if response_or_exc is None:
            self.session.commit()

    self.session.remove()
    return response_or_exc  
    
# sqlalchemy.orm.scoping.scoped_session
# sqlalchemy.util._collections.ScopedRegistry 定义
def clear(self):
    #Clear the current scope, if any.
    try:
        del self.registry[self.scopefunc()]
    except KeyError:
        pass
"""


if __name__ == '__main__':
    app.run(threaded=True)

# 不使用线程或进程模式时，请求都会发向同一个socket，处理时间会有先后顺序，相互影响。
# threaded模式会为每个进来的请求创建新的线程去处理，请求之间不会相互影响，通过下面的测试就可以了解。
# processes 模式就是创建进程。

"""
root@(none):# date ;curl "http://127.0.0.1:5000/add2";date
Tue Aug 14 08:38:14 CST 2018
add2Tue Aug 14 08:39:14 CST 2018

root@(none):~# date ;curl "http://127.0.0.1:5000/add1";date
Tue Aug 14 08:38:16 CST 2018
add1Tue Aug 14 08:39:16 CST 2018

root@(none):~# ps -T -p 8657
  PID  SPID TTY          TIME CMD
 8657  8657 pts/7    00:00:00 python
 8657  8662 pts/7    00:00:00 python
 8657  8666 pts/7    00:00:00 python

"""


"""
# sqlalchemy.util._collections.ScopedRegistry 函数加了打印可以看出每次请求进来都是不同的id，已经不同的session去处理
('db.session:', {'session_factory': 127.0.0.1 - - [15/Aug/2018 15:48:19] "GET /add1 HTTP/1.1" 200 -
sessionmaker(class_='SignallingSession', autocommit=False, query_cls=<class 'flask_sqlalchemy.BaseQuery'>, expire_on_commit=True, bind=None, db=<SQLAlchemy engine=mysql://root:***@172.16.4.120:3306/mytest?charset=utf8>, autoflush=True), 'registry': <sqlalchemy.util._collections.ScopedRegistry object at 0x000000000379D748>})
('id(db_session)', <sqlalchemy.orm.scoping.scoped_session object at 0x000000000379D710>)
('1 __call__:', <greenlet.greenlet object at 0x00000000038605A0>)
('2 __call__:', {})
('3 has:', {<greenlet.greenlet object at 0x00000000038605A0>: <sqlalchemy.orm.session.SignallingSession object at 0x00000000038756A0>})
('1 __call__:', <greenlet.greenlet object at 0x00000000038605A0>)
('2 __call__:', {<greenlet.greenlet object at 0x00000000038605A0>: <sqlalchemy.orm.session.SignallingSession object at 0x00000000038756A0>})
('4 clear start:', {<greenlet.greenlet object at 0x00000000038605A0>: <sqlalchemy.orm.session.SignallingSession object at 0x00000000038756A0>})
('5 clear end:', {})


('db.session:', {'session_factory': sessionmaker(class_='SignallingSession', autocommit=False, query_cls=<class 'flask_sqlalchemy.BaseQuery'>, expire_on_commit=True, bind=None, db=<SQLAlchemy engine=mysql://root:***@172.16.4.120:3306/mytest?charset=utf8>, autoflush=True), 'registry': <sqlalchemy.util._collections.ScopedRegistry object at 0x000000000379D748>})
('id(db_session)', <sqlalchemy.orm.scoping.scoped_session object at 0x000000000379D710>)
('1 __call__:', <greenlet.greenlet object at 0x00000000039843D8>)
('2 __call__:', {})
('1 __call__:', <greenlet.greenlet object at 0x00000000039843D8>)
('2 __call__:', {<greenlet.greenlet object at 0x00000000039843D8>: <sqlalchemy.orm.session.SignallingSession object at 0x000000000398DE48>})
127.0.0.1 - - [15/Aug/2018 15:49:29] "GET /add2 HTTP/1.1" 200 -
('3 has:', {<greenlet.greenlet object at 0x00000000039843D8>: <sqlalchemy.orm.session.SignallingSession object at 0x000000000398DE48>})
('1 __call__:', <greenlet.greenlet object at 0x00000000039843D8>)
('2 __call__:', {<greenlet.greenlet object at 0x00000000039843D8>: <sqlalchemy.orm.session.SignallingSession object at 0x000000000398DE48>})
('4 clear start:', {<greenlet.greenlet object at 0x00000000039843D8>: <sqlalchemy.orm.session.SignallingSession object at 0x000000000398DE48>})
('5 clear end:', {})

"""