# ! /usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
from . import db
import datetime


class User(db.Model):
    # 用户表
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    hash = db.Column('hash', db.String(256), nullable=False)  # 密码
    username = db.Column('username', db.String(32), index=True, unique=True)  # 用户名
    fullname = db.Column('fullname', db.String(32))  # 全名
    email = db.Column('email', db.String(64))  # 邮箱
    telephone = db.Column('telephone', db.String(11))  # 座机号码
    user_type = db.Column('user_type', db.Integer, default=2)  # 用户类型
    active = db.Column('active', db.Integer, default=0)  # 激活状态(0：未激活；1：已激活)
    create_time = db.Column('create_time', db.TIMESTAMP, default=datetime.datetime.now())  # 创建时间
    update_time = db.Column('update_time', db.TIMESTAMP)  # 更新时间

    def __init__(self, username, password, email, telephone, fullname, active, user_type):
        self.username = username
        m2 = hashlib.md5()
        m2.update(password)
        self.hash = m2.hexdigest()
        self.email = email
        self.telephone = telephone
        self.fullname = fullname
        self.active = active
        self.user_type = user_type

    def to_dict(self):
        dict = {}
        dict.update(self.__dict__)
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']
        return dict
