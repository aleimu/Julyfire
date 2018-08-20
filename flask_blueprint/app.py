# -*- coding:utf-8 -*-
__author__ = "lgj"
__date__ = "2018-8-14"

import os
from flask import Flask
from ablueprint import ab
from bblueprint import bb
from cbuleprint import cb

app = Flask(__name__, static_folder='static', static_url_path='/app/', template_folder='template')


@app.before_request
def before_request():
    print("*****app.before_request*****")


@app.teardown_request
def teardown_request(err):
    print("*****app.teardown_request*****")


def register_blueprint():
    app.register_blueprint(ab, url_prefix='/a')
    app.register_blueprint(bb, url_prefix='/b')
    app.register_blueprint(cb, url_prefix='/c')


register_blueprint()
app.secret_key = os.urandom(24)
print(vars(app))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2000, threaded=True, debug=True)  # 本地测试

"""
curl "http://127.0.0.1:2000/b/"

*****app.before_request*****
*****bb.before_request*****
*****app.teardown_request*****
*****bb.teardown_request*****

1、可以看出先执行了全局app的before_request然后才会执行bb蓝图中的自有before_request。
2、虽然下面的结构看着复杂，其实本质还是python的基础类型的组合
3、每个蓝图中可以定义自己的配置,细节还是需要看blueprint.py中的每个函数的注解
"""

"""
 {
	'subdomain_matching': False,
	'error_handler_spec': {},
	'_before_request_lock': < thread.lock object at 0x000000000261CD50 > ,
	'before_request_funcs': {
		'cb': [ < function before_request at 0x0000000002F0A048 > ],
		'ab': [ < function before_request at 0x0000000002F0A7B8 > ],
		'bb': [ < function before_request at 0x0000000002F0A4A8 > ],
		None: [ < function before_request at 0x0000000002F18208 > ]
	},
	'teardown_appcontext_funcs': [],
	'shell_context_processors': [],
	'after_request_funcs': {},
	'cli': < flask.cli.AppGroup object at 0x0000000002F11588 > ,
	'_blueprint_order': [ < flask.blueprints.Blueprint object at 0x0000000002F11278 > , < flask.blueprints.Blueprint object at 0x0000000002F112B0 > , < flask.blueprints.Blueprint object at 0x0000000002F11320 > ],
	'before_first_request_funcs': [],
	'view_functions': {
		'cb.users': < function users at 0x0000000002F18278 > ,
		'bb.users': < function users at 0x0000000002F0A208 > ,
		'static': < bound method Flask.send_static_file of < Flask 'app' >> ,
		'bb.static': < bound method Blueprint.send_static_file of < flask.blueprints.Blueprint object at 0x0000000002F112B0 >> ,
		'ab.static': < bound method Blueprint.send_static_file of < flask.blueprints.Blueprint object at 0x0000000002F11278 >> ,
		'ab.users': < function users at 0x0000000002F0A518 >
	},
	'instance_path': 'C:\\Users\\lenovo\\Desktop\\\xb5\xe3\xb5\xce\xbb\xfd\xc0\xdb\\Julyfire\\flask_blueprint\\instance',
	'teardown_request_funcs': {
		'cb': [ < function teardown_request at 0x0000000002F180B8 > ],
		'ab': [ < function teardown_request at 0x0000000002F0A6D8 > ],
		'bb': [ < function teardown_request at 0x0000000002F0A3C8 > ],
		None: [ < function teardown_request at 0x0000000002F18358 > ]
	},
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
		'SECRET_KEY': '\xe9\x8c\xa5N\xb7<\xd43r\xa5\xb5\xa3\x92$\xbd\xdf\xbb!h%\xb7F:\x89',
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
	'_static_url_path': '/app/',
	'template_context_processors': {
		None: [ < function _default_template_ctx_processor at 0x0000000002EF3BA8 > ]
	},
	'template_folder': 'template',
	'blueprints': {
		'cb': < flask.blueprints.Blueprint object at 0x0000000002F11320 > ,
		'ab': < flask.blueprints.Blueprint object at 0x0000000002F11278 > ,
		'bb': < flask.blueprints.Blueprint object at 0x0000000002F112B0 >
	},
	'url_map': Map([ < 
        Rule '/a/' (HEAD, OPTIONS, GET) - > ab.users > , <
        Rule '/b/' (HEAD, OPTIONS, GET) - > bb.users > , <
        Rule '/c/' (HEAD, OPTIONS, GET) - > cb.users > , <
        Rule '/a/ab//<filename>' (HEAD, OPTIONS, GET) - > ab.static > , <
        Rule '/b/bb//<filename>' (HEAD, OPTIONS, GET) - > bb.static > , <
        Rule '/app//<filename>' (HEAD, OPTIONS, GET) - > static >
	]),
	'name': 'app',
	'_got_first_request': False,
	'import_name': '__main__',
	'root_path': 'C:\\Users\\lenovo\\Desktop\\\xb5\xe3\xb5\xce\xbb\xfd\xc0\xdb\\Julyfire\\flask_blueprint',
	'_static_folder': 'static',
	'extensions': {},
	'url_default_functions': {},
	'url_build_error_handlers': []
}

"""
