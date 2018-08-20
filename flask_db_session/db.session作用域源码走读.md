本文主要是为了验证两个问题：
1. flask处理请求时通过新建线程、进程、协程的区别(顺带一提)
2. flask_sqlalchemy是如何使用db.session使多个请求中保函的改变同一个表的sql操作不相互影响的，专业名词是会话范围或Session作用域(主要探讨)

#### 一个简单的例子
```python
# -*- coding:utf-8 -*-
from sqlalchemy.orm.session import Session # 线程不安全
from sqlalchemy.orm import scoped_session  # 线程安全

import time
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@172.16.4.120:3306/mytest?charset=utf8'
db = SQLAlchemy(app)    # db.init_app(app) 提供了两种将app与db绑定的方式，具体区别看文档，这里不做分析
db_session = db.session


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
    time.sleep(60)
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
    time.sleep(60)
    return "add2"

if __name__ == '__main__':
    app.run(threaded=True)
```
#### 三种run的方式
```
# 不使用线程或进程模式时，请求都会发向同一个socket，处理时间会有先后顺序，相互影响。(flask会检查库中是否有协程greenlet库，但这里即使用了也是会影响的，因为并不是time.sleep不符合协程的要求)
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
```

#### db.session的探寻
```shell
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
```

#### 笨办法print
```
# sqlalchemy.util._collections.ScopedRegistry 函数加了打印可以看出每次请求进来都是不同的id，以及不同的session去处理
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

```
#### 总结上面的流程
```
Web Server          Web Framework        SQLAlchemy ORM Code
--------------      --------------       ------------------------------
startup        ->   Web framework        # Session registry is established
                    initializes          Session = scoped_session(sessionmaker())

incoming
web request    ->   web request     ->   # The registry is *optionally*
                    starts               # called upon explicitly to create
                                         # a Session local to the thread and/or request
                                         Session()

                                         # the Session registry can otherwise
                                         # be used at any time, creating the
                                         # request-local Session() if not present,
                                         # or returning the existing one
                                         Session.query(MyClass) # ...

                                         Session.add(some_object) # ...

                                         # if data was modified, commit the
                                         # transaction
                                         Session.commit()

                    web request ends  -> # the registry is instructed to
                                         # remove the Session
                                         Session.remove()

                    sends output      <-
outgoing web    <-
response
```

### 重点来了

sqlalchemy是python中最强大的orm框架，无疑sqlalchemy的使用比django自带的orm要复杂的多，
使用flask sqlalchemy扩展将拉近和django的简单易用距离。
先来说两个比较重要的配置

app.config['SQLALCHEMY_ECHO'] = True =》配置输出sql语句
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True =》每次request自动提交db.session.commit(),
如果有一天你发现别的写的视图中有db.session.add，但没有db.session.commit，不要疑惑，他肯定配置了上面的选项。
这是通过app.teardown_appcontext注册实现

```python
        @teardown
        def shutdown_session(response_or_exc):
            if app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']:
                if response_or_exc is None:
                    self.session.commit()
            self.session.remove()
            return response_or_exc
```
```
response_or_exc为异常值，默认为sys.exc_info()[1]
上面self.session.remove()表示每次请求后都会销毁self.session，为什么要这么做呢？
这就要说说sqlalchemy的session对象了。
from sqlalchemy.orm import sessionmaker
session = sessionmaker()
一帮我们会通过sessionmaker()这个工厂函数创建session，但这个session并不能用在多线程中，为了支持多线程
操作，sqlalchemy提供了scoped_session，通过名字反映出scoped_session是通过某个作用域实现的
所以在多线程中一帮都是如下使用session
from sqlalchemy.orm import scoped_session, sessionmaker
session = scoped_session(sessionmaker())

我们来看看scoped_session是如何提供多线程环境支持的
```
```python
class scoped_session(object):
    def __init__(self, session_factory, scopefunc=None):
        
        self.session_factory = session_factory
        if scopefunc:
            self.registry = ScopedRegistry(session_factory, scopefunc)
        else:
            self.registry = ThreadLocalRegistry(session_factory)
```
```
__init__中，session_factory是创建session的工厂函数，而sessionmaker就是一工厂函数(其实是定义了__call__的
函数)而scopefunc就是能产生某个作用域的函数，如果不提供将使用ThreadLocalRegistry
```
```python
class ThreadLocalRegistry(ScopedRegistry):
    def __init__(self, createfunc):
        self.createfunc = createfunc
        self.registry = threading.local()
 
    def __call__(self):
        try:
            return self.registry.value
        except AttributeError:
            val = self.registry.v
```
```
从上面__call__可以看出，每次都会创建新的session，并发在线程本地变量中，你可能会好奇__call__是在哪里调用的？
```
```python
def instrument(name):
    def do(self, *args, **kwargs):
        return getattr(self.registry(), name)(*args, **kwargs)
    return do
 
for meth in Session.public_methods:
    setattr(scoped_session, meth, instrument(meth))
```
```
正如我们所看到的，当我们调用session.query将会调用 getattr(self.registry(), 'query')，self.registry()就是
调用__call__的时机，但是在flask_sqlalchemy中并没有使用ThreadLocalRegistry，创建scoped_session过程如下
```
```python
# Which stack should we use?  _app_ctx_stack is new in 0.9
connection_stack = _app_ctx_stack or _request_ctx_stack
 
    def __init__(self, app=None,
                 use_native_unicode=True,
                 session_options=None):
        session_options.setdefault(
            'scopefunc', connection_stack.__ident_func__
        )
        self.session = self.create_scoped_session(session_options)
 
    def create_scoped_session(self, options=None):
        """Helper factory method that creates a scoped session."""
        if options is None:
            options = {}
        scopefunc=options.pop('scopefunc', None)
        return orm.scoped_session(
            partial(_SignallingSession, self, **options), scopefunc=scopefunc
        )
```

我们看到scopefunc被设置为connection_stack.__ident_func__，而connection_stack就是flask中app上下文，
如果你看过前一篇文章你就知道__ident_func__其实就是在多线程中就是thrading.get_ident，也就是线程id
我们看看ScopedRegistry是如何通过_操作的

```python
class ScopedRegistry(object):
    def __init__(self, createfunc, scopefunc):
        self.createfunc = createfunc
        self.scopefunc = scopefunc
        self.registry = {}
 
 
    def __call__(self):
        key = self.scopefunc()
        try:
            return self.registry[key]
        except KeyError:
            return self.registry.setdefault(key, self.createfunc())
```
```
代码也很简单，其实也就是根据线程id创建对应的session对象，到这里我们基本已经了解了flask_sqlalchemy的
魔法了，和flask cookie,g有异曲同工之妙，这里有两个小问题？
1.flask_sqlalchemy能否使用ThreadLocalRegistry？
    大部分情况都是可以的，但如果wsgi对多并发使用的是greenlet的模式就不适用了
2.上面create_scoped_session中partial是干嘛的？
    前面我们说过scoped_session的session_factory是可调用对象，但_SignallingSession类并没有定义__call__，所以通过partial支持

到这里你就知道为什么每次请求结束要self.session.remove()，不然为导致存放session的字段太大

这里说一下对db.relationship lazy的理解，看如下代码
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
 
 
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
假设role是已经获取的一个Role的实例
lazy:dynamic => role.users不会返回User的列表， 返回的是sqlalchemy.orm.dynamic.AppenderBaseQuery对象
                当执行role.users.all()是才会真正执行sql，这样的好处就是可以继续过滤

lazy:select => role.users直接返回User实例的列表，也就是直接执行sql

注意：db.session.commit只有在对象有变化时才会真的执行update

```

#### 参考
https://stackoverflow.com/questions/39480914/why-db-session-remove-must-be-called 问题引出
http://www.cnblogs.com/ctztake/p/8277372.html  说的比较简单
https://blog.csdn.net/yueguanghaidao/article/details/40016235  大佬的足迹
http://docs.sqlalchemy.org/en/latest/orm/contextual.html#using-thread-local-scope-with-web-applications 文档