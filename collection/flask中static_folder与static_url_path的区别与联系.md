```python

# -*- coding:utf-8 -*-

from flask import Flask, url_for

app1 = Flask(__name__, static_folder='mystatic', static_url_path='/myurl', template_folder='mytemplate')
app2 = Flask(__name__)
app3 = Flask(__name__, static_url_path='')


@app1.route('/')
def hello_world():
    return 'Hello World!'


@app1.route("/css")
def static_css():
    return url_for('static', filename='style.css')


@app1.route("/js")
def static_js():
    return url_for('static', filename='login.js')


# @app.route("/ss")
# def static():
#     return "hello ss!"
# AssertionError: View function mapping is overwriting an existing endpoint function: static
# 不允许重复定义内部约束方法static



if __name__ == '__main__':
    print("1--------------------")
    print(app1.__dict__)
    print app1.view_functions['static'].__dict__
    print("2--------------------")
    print app2.__dict__
    print("3--------------------")
    print app3.__dict__
    # app1.run()
    # app2.run(port=5001)
    # app3.run(port=5002)
```


#### 目录结构
```

flask_simply_dome
    -mystatic
        --login.js  -->"this is a test login.js"
    -static
        --login.js  -->"this is app3 or app2 login.js"
    asimply_app.py
```
```shell
# curl "http://127.0.0.1:5000/css"
/myurl/style.css
# curl "http://127.0.0.1:5000/js"
/myurl/login.js
# curl "http://127.0.0.1:5000/myurl/login.js"
"this is a test login.js"

# curl "http://127.0.0.1:5001/static/login.js"
"this is app3 or app2 login.js"

# curl "http://127.0.0.1:5002/login.js"
"this is app3 or app2 login.js"
```
#### 对比各app的属性
```
1--------------------
{
	'subdomain_matching': False,
	'error_handler_spec': {},
	'_before_request_lock': < thread.lock object at 0x0000000002619D50 > ,
	'before_request_funcs': {},
	'teardown_appcontext_funcs': [],
	'shell_context_processors': [],
	'after_request_funcs': {},
	'cli': < flask.cli.AppGroup object at 0x0000000002EF0278 > ,
	'_blueprint_order': [],
	'before_first_request_funcs': [],
	'view_functions': {
		'static_css': < function static_css at 0x0000000002EF87B8 > ,
		'static_js': < function static_js at 0x0000000002EF8828 > ,
		'hello_world': < function hello_world at 0x0000000002EF8748 > ,
		'static': < bound method Flask.send_static_file of < Flask 'asimply_app' >>
	},
	'instance_path': 'D:\\myself\\flask_simply_dome\\instance',
	'teardown_request_funcs': {},
	'url_value_preprocessors': {},
	'config': < Config {
		'JSON_AS_ASCII': True,
		'USE_X_SENDFILE': False,
		'SESSION_COOKIE_SECURE': False,
		'SESSION_COOKIE_PATH': None,
		'SESSION_COOKIE_DOMAIN': None,
		'SESSION_COOKIE_NAME': 'session',
		'MAX_COOKIE_SIZE': 4093,
		'SESSION_COOKIE_SAMESITE': None,
		'PROPAGATE_EXCEPTIONS': None,
		'ENV': 'production',
		'DEBUG': False,
		'SECRET_KEY': None,
		'EXPLAIN_TEMPLATE_LOADING': False,
		'MAX_CONTENT_LENGTH': None,
		'APPLICATION_ROOT': '/',
		'SERVER_NAME': None,
		'PREFERRED_URL_SCHEME': 'http',
		'JSONIFY_PRETTYPRINT_REGULAR': False,
		'TESTING': False,
		'PERMANENT_SESSION_LIFETIME': datetime.timedelta(31),
		'TEMPLATES_AUTO_RELOAD': None,
		'TRAP_BAD_REQUEST_ERRORS': None,
		'JSON_SORT_KEYS': True,
		'JSONIFY_MIMETYPE': 'application/json',
		'SESSION_COOKIE_HTTPONLY': True,
		'SEND_FILE_MAX_AGE_DEFAULT': datetime.timedelta(0, 43200),
		'PRESERVE_CONTEXT_ON_EXCEPTION': None,
		'SESSION_REFRESH_EACH_REQUEST': True,
		'TRAP_HTTP_EXCEPTIONS': False
	} > ,
	'_static_url_path': '/myurl',
	'template_context_processors': {
		None: [ < function _default_template_ctx_processor at 0x0000000002ED9BA8 > ]
	},
	'template_folder': 'mytemplate',
	'blueprints': {},
	'url_map': Map([ < Rule '/css' (HEAD, OPTIONS, GET) - > static_css > , <
		Rule '/js' (HEAD, OPTIONS, GET) - > static_js > , <
		Rule '/' (HEAD, OPTIONS, GET) - > hello_world > , <
		Rule '/myurl/<filename>' (HEAD, OPTIONS, GET) - > static >
	]),
	'name': 'asimply_app',
	'_got_first_request': False,
	'import_name': '__main__',
	'root_path': 'D:\\myself\\flask_simply_dome',
	'_static_folder': 'mystatic',
	'extensions': {},
	'url_default_functions': {},
	'url_build_error_handlers': []
}
{}
1--------------------
{
	'subdomain_matching': False,
	'error_handler_spec': {},
	'_before_request_lock': < thread.lock object at 0x0000000002619D70 > ,
	'before_request_funcs': {},
	'teardown_appcontext_funcs': [],
	'shell_context_processors': [],
	'after_request_funcs': {},
	'cli': < flask.cli.AppGroup object at 0x0000000002EF03C8 > ,
	'_blueprint_order': [],
	'before_first_request_funcs': [],
	'view_functions': {
		'static': < bound method Flask.send_static_file of < Flask 'asimply_app' >>
	},
	'instance_path': 'D:\\myself\\flask_simply_dome\\instance',
	'teardown_request_funcs': {},
	'url_value_preprocessors': {},
	'config':同上,
	'_static_url_path': None,
	'template_context_processors': {
		None: [ < function _default_template_ctx_processor at 0x0000000002ED9BA8 > ]
	},
	'template_folder': 'templates',
	'blueprints': {},
	'url_map': Map([ < Rule '/static/<filename>' (HEAD, OPTIONS, GET) - > static > ]),
	'name': 'asimply_app',
	'_got_first_request': False,
	'import_name': '__main__',
	'root_path': 'D:\\myself\\flask_simply_dome',
	'_static_folder': 'static',
	'extensions': {},
	'url_default_functions': {},
	'url_build_error_handlers': []
}
2--------------------

{
	'subdomain_matching': False,
	'error_handler_spec': {},
	'_before_request_lock': < thread.lock object at 0x00000000026A3DB0 > ,
	'before_request_funcs': {},
	'teardown_appcontext_funcs': [],
	'shell_context_processors': [],
	'after_request_funcs': {},
	'cli': < flask.cli.AppGroup object at 0x0000000002FFB5F8 > ,
	'_blueprint_order': [],
	'before_first_request_funcs': [],
	'view_functions': {
		'static': < bound method Flask.send_static_file of < Flask 'asimply_app' >>
	},
	'instance_path': 'D:\\myself\\flask_simply_dome\\instance',
	'teardown_request_funcs': {},
	'url_value_preprocessors': {},
	'config': 同上,
	'_static_url_path': '',
	'template_context_processors': {
		None: [ < function _default_template_ctx_processor at 0x0000000002FDEBA8 > ]
	},
	'template_folder': 'templates',
	'blueprints': {},
	'url_map': Map([ < Rule '/<filename>' (HEAD, OPTIONS, GET) - > static > ]),
	'name': 'asimply_app',
	'_got_first_request': False,
	'import_name': '__main__',
	'root_path': 'D:\\myself\\flask_simply_dome',
	'_static_folder': 'static',
	'extensions': {},
	'url_default_functions': {},
	'url_build_error_handlers': []
}
3----------------------

"""
```
#### 结论
```shell
static_url_path主要用于改变url的path的，静态文件放在static下面，所以正常情况url是static/filename ，但是可以通过static_url_path来改变这个url
static_folder主要是用来改变url的目录的，默认是static，可以通过这个变量来改变静态文件目录。
对于配置这两个参数，首先要确定前端请求js、html文件时经过app了吗？还是直接通过Nginx获得的？要是没进过app，那这里的配置是无效的，也就是说前后端分离的话，这里的配置也就没意义了。
查看flask的日志，也没有发现有请求静态资源的记录。
```
