# -*- coding:utf-8 -*-
import os
import time
from ..models import db
from ..models import User

from sqlalchemy import or_, and_


def check_user(username, password):
    print("check_user(username,password)")
    print(db.session.query(User).filter(or_(User.username == 'jingqi', User.password == 'qwe123')).all())
    print(db.session.query(User).filter(and_(User.username == 'jingqi2', User.password == '111')).all())
    user = User.query.filter(and_(User.username == username, User.password == password)).one()
    if user:
        return True
    else:
        return False


def mark_user(username):
    print("mark_user(username)")
    user = User.query.filter(User.username == username).one()
    if user:
        return True
    else:
        return False
