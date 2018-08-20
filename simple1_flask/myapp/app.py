# -*- coding:utf-8 -*-

from flask import Flask
from myapp.models import db
# 重点关注py2与py3的import区别，相对路径与绝对路径
# python2缺省为相对路径导入，python3缺省为绝对路径导入,python2缺省会搜索上一级目录、上上级目录
# from .views.simple_page import simple_page  #py2 from .views.simple_page import simple_page
#                                              # ValueError: Attempted relative import in non-package
# from views.simple_page import simple_page  #py2 from ..models import db
#                                             # ValueError: Attempted relative import beyond toplevel package



from myapp.views.simple_page import simple_page  # py2 ok!
from myapp.views.simple_view import simple_view  # py3 ok!

print ("__name__", __name__)
app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(simple_page, url_prefix='/pages')
app.register_blueprint(simple_view, url_prefix='/views')

db.init_app(app)


@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()


if __name__ == '__main__':
    print(vars(app))
    app.run()
