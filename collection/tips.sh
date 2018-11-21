# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

# 生成一个SQLORM基类，创建表必须继承他，别问我啥意思就是这么规定的
Base = declarative_base()
# 链接数据库采用pymysq模块做映射，后面参数是最大连接数5
engine = create_engine('mysql+pymysql://root:lgj123@127.0.0.1:3306/test?charset=utf8', max_overflow=5)
Session = sessionmaker(bind=engine)
session = Session()

# mysql 数据库并不需要真的建立外键，使用下面的方式也是可以模拟外键的效果的！

class users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(32))
    password = Column(String(32))
    children = relationship("login", backref="users")

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return "<users(%s,%s,%s)>" % (self.id, self.email, self.password)


class login(Base):
    __tablename__ = 'login'

    id = Column(Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey('users.id'))
    confirmed = Column(Integer)

    def __init__(self, confirmed):
        self.confirmed = confirmed

    def __repr__(self):
        return "<login(%s,%s,%s)>" % (self.id, self.users_id, self.confirmed)


u1 = users('a1', "a2")
c1 = login('b1')
c2 = login('b2')
u1.children = [c1, c2]
session.add(u1)
session.commit()



# https://www.cnblogs.com/huchong/p/8797516.html#_lab2_0_0

# https://www.jianshu.com/p/9771b0a3e589
