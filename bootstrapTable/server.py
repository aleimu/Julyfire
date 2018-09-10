# -*- coding:utf-8 -*-

import hashlib
import datetime
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1:3306/test?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = True

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'SECRET_KEY'

db = SQLAlchemy(app)
CORS(app)


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    hash = db.Column('hash', db.String(256), nullable=False)
    email = db.Column('email', db.String(64))
    mobile = db.Column('mobile', db.String(11))
    telephone = db.Column('telephone', db.String(11))
    role_type = db.Column('role_type', db.Integer, nullable=False)
    active = db.Column('active', db.Integer, default=0)
    create_time = db.Column('create_time', db.TIMESTAMP, default=datetime.datetime.now())
    username = db.Column('username', db.String(32), index=True, unique=True)
    fullname = db.Column('fullname', db.String(32))
    photo_url = db.Column('photo_url', db.TEXT)
    zh_name = db.Column('zh_name', db.String(32))
    source = db.Column(db.Integer)

    def __init__(self, username, password, email, mobile, telephone, role_type, fullname,
                 active, user_no, registration_id, fk_location_code, delete_flag):
        self.username = username
        m2 = hashlib.md5()
        m2.update(password)
        self.hash = m2.hexdigest()
        self.email = email
        self.mobile = mobile
        self.telephone = telephone
        self.role_type = role_type
        self.fullname = fullname
        self.active = active
        self.create_time = datetime.datetime.now()
        self.zh_name = fullname
        self.user_no = user_no
        self.registration_id = registration_id
        self.fk_location_code = fk_location_code
        self.source = 1
        self.delete_flag = delete_flag

    def to_dict(self):
        dict = {}
        dict.update(self.__dict__)
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']
        dict["ID"] = dict["id"]
        dict["Name"] = dict["username"]
        dict["ParentName"] = dict["fullname"]
        dict["Desc"] = dict["telephone"]
        dict["Email"] = dict["email"]
        dict["Level"] = dict["active"]
        return dict

@app.route('/get')
def users():
    print('/user request data: %s' % (request.values.items()))
    # http://127.0.0.1:3001/get?limit=10&offset=0&departmentname=&statu=&_=1536126471657
    offset = int(request.values.get('offset', 0))
    limit = int(request.values.get('limit', 10))
    role_type = request.values.get('role_type', 0)
    print("input offset, limit, role_type:", offset, limit, role_type)
    print("output offset, limit, role_type:", offset / 10 + 1, limit, role_type)
    err, set = get_users(offset / 10 + 1, limit, role_type)
    # print("set:",set)
    if not err:
        return jsonify(set)
    else:
        return jsonify(err, None, {})


@app.route('/add')
def modify_user():
    print('/users/id/ request data: %s' % (request.values.items()))
    id = request.values.get("id")
    email = request.values.get("email")
    fk_location_code = request.values.get("fk_location_code")
    fullname = request.values.get("fullname")
    mobile = request.values.get("mobile")
    telephone = request.values.get("telephone")
    user_no = request.values.get("user_no")
    username = request.values.get("username")
    password = request.values.get("password")
    zh_name = request.values.get("zh_name")
    role_type = request.values.get("role_type")
    delete_flag = request.values.get("delete_flag")
    if int(role_type) == 0:
        telephone = username
        mobile = username
    comt_type = request.values.get("comt_type")
    err, result = modify_user(id, email, fk_location_code, fullname, mobile, telephone, user_no, username,
                              password, zh_name, role_type, comt_type, delete_flag)
    if result:
        return jsonify(result)
    else:
        return jsonify(err, None, {})


def get_users(page, per_page, role_type):
    if not role_type:
        # users = User.query.filter().slice(int(page),int(per_page))
        # print("users--->:", users)
        users = User.query.filter().paginate(int(page), int(per_page), True)
        # print("users--->:",users)
        count = User.query.filter().count()
        users_list = []
        print("get_users1:", users.items)
        for item in users.items:
            user = item.to_dict()
            # print(user)
            user['create_time'] = datetime.datetime.strftime(user['create_time'], "%Y-%m-%d %H:%M:%S")
            users_list.append(user)
        # set = {"count": count, "users": users_list}
        set = {"total": count, "rows": users_list}
        db.session.remove()
        return None, set
    if int(role_type) == 0:
        users = User.query.filter_by(role_type=role_type).paginate(int(page), int(per_page), False)
        count = User.query.filter_by(role_type=role_type).count()
        users_list = []
        for item in users.items:
            user = item.to_dict()
            user['create_time'] = datetime.datetime.strftime(user['create_time'], '%y-%m-%d %h:%m')
            users_list.append(user)
        set = {"count": count, "users": users_list}
        db.session.remove()
        return None, set
    if int(role_type) != 0:
        statment = "role_type = 1 or role_type = 2"
        users = User.query.filter(statment).paginate(int(page), int(per_page), False)
        count = User.query.filter(statment).count()
        users_list = []
        for item in users.items:
            user = item.to_dict()
            user['create_time'] = datetime.datetime.strftime(user['create_time'], '%y-%m-%d %h:%m')
            users_list.append(user)
        set = {"count": count, "users": users_list}
        db.session.remove()
        return None, set


def delete_user(id):
    userobj = User.query.filter_by(id=id).first()
    if not userobj:
        return 'NO_USER', None
    User.query.filter_by(id=id).update(
        {User.delete_flag: 1})
    db.session.commit()
    return None, True


if __name__ == "__main__":
    print(vars(app))
    app.run(host='0.0.0.0', port=3001, threaded=True, debug=True)
    # localhost:63342
