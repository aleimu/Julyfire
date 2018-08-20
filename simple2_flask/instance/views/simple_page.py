# -*- coding:utf-8 -*-

from flask import Blueprint, render_template, abort, request, jsonify
from jinja2 import TemplateNotFound
from sqlalchemy import text

from ..models import User
from ..models import db

simple_page = Blueprint('simple_page', __name__, template_folder='templates')


@simple_page.before_request
def before_request():
    if request.path == '/token':
        token = request.values.get('token')
        if not token:
            return jsonify(error="no token", code=500)


@simple_page.teardown_request
def handle_teardown_request(exception):
    db.session.remove()


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
    # username, password, email, telephone, fullname, active, user_type
    user1 = User(username='张一', password='1234561', email='zhang1@qq.com', telephone='1315501789', fullname=True,
                 active=0, user_type=10)
    user2 = User(username='张二', password='1234562', email='zhang2@qq.com', telephone='1315501789', fullname=True,
                 active=1, user_type=11)
    user3 = User(username='张三', password='1234563', email='zhang3@qq.com', telephone='1315501789', fullname=True,
                 active=1, user_type=12)
    user4 = User(username='张四', password='1234564', email='zhang4@qq.com', telephone='1315501789', fullname=True,
                 active=0, user_type=13)
    db.session.add_all([user1, user2, user3, user4])
    db.session.commit()
    return '插入成功'


# 修改数据
@simple_page.route('/update/<uid>')
def update(uid):
    user = User.query.get(uid)
    if user:
        user.password = '1234561'
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


# 利用text语句进行查询
@simple_page.route('/textsql')
def textsql():
    all_user = db.session.query(User).filter(text("id<224")).order_by(text("id")).all()
    print(all_user)
    return all_user
