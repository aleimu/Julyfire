#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import datetime

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from instance.models import User
from instance import db, create_app

app = create_app('dev')

app.secret_key = os.urandom(24)
app.permanent_session_lifetime = datetime.timedelta(seconds=24 * 60 * 60)

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, User=User, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
