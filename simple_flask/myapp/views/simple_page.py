# -*- coding:utf-8 -*-

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from myapp.models.user import User
from myapp.models.other import Post, Category
from ..models import db

simple_page = Blueprint('simple_page', __name__, template_folder='templates')


@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)


@simple_page.route('/hello')
def hello_world():
    return 'Simple_page Say Hello World!'


# 往数据库插入数据
@simple_page.route('/insert/')
def insert():
    user1 = User(name='张三', password='123456', email='zhangsan@qq.com', gender=True)
    user2 = User(name='李四', password='123456', email='lisi@qq.com', gender=True)
    user3 = User(name='王五', password='123456', email='wangwu@qq.com', gender=True)
    user4 = User(name='莫愁', password='123456', email='mochou@qq.com', gender=False)
    user5 = User(name='凤姐', password='123456', email='fengjie@qq.com', gender=False)
    db.session.add_all([user1, user2, user3, user4, user5])
    db.session.commit()
    return '插入成功'


# 修改数据
@simple_page.route('/update/<uid>')
def update(uid):
    user = User.query.get(uid)
    if user:
        user.password = '654321'
        db.session.add(user)
        return '修改成功'
    else:
        return '查无此人'


# 查询数据
@simple_page.route('/find/')
def find():
    ulist = User.query.all()
    ret = ';'.join([str(i) for i in ulist])
    return ret


# 条件查询
@simple_page.route('/xfind/')
def xfind():
    # 查找id大于3的数据
    # user=User.query.filter(User.id>3).all()
    # 查找男性
    user = User.query.filter(User.gender == True).all()
    ret = ';'.join([str(k) for k in user])
    return ret


# 利用sql语句进行查询
@simple_page.route('/dosql/')
def dosql():
    ret = db.session.execute("select gender,count(id) from t_user GROUP by gender").fetchall()
    return str(ret)
