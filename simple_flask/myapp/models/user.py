from . import db


# 创建数据模型
class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column('mail_box', db.String(120), unique=True, nullable=False)
    gender = db.Column(db.Boolean(), default=None, nullable=False)

    def __str__(self):
        return 'User{name=%s,email=%s,password=%s,}' % (self.name, self.email, self.password,)
