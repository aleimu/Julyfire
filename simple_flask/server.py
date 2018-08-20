# -*- coding:utf-8 -*-

from myapp.app import app, db

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager as manager

manager = manager(app)
migrate = Migrate(app, db)


# 创建python manage.py createdb命令，创建数据库
@manager.command
def createdb():
    db.create_all()
    return '创建数据库成功'


# 创建python manage.py dropdb命令，删除数据库
@manager.command
def dropdb():
    db.drop_all()
    return '删除数据库成功'


manager.add_command('db', MigrateCommand)

print(vars(app))
if __name__ == '__main__':
    manager.run()
