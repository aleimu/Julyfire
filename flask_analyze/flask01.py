# -*- coding: utf-8 -*-
"""
签注说明:
    - date: 2018-7
    - author: lgj
    - 说明:
        - 删除部分无关紧要的原注释,不影响理解
        - 部分源码注释,作了精简翻译.
        - 打断点真的很重要
flask: 微型web框架.
    - 核心依赖:
        - Werkzeug :
            - 功能实现: request, response,url路由管理
            - 导入接口: 部分未实现接口, 直接导入用
        - jinja2 :
            - 功能实现:模板渲染
            - 导入接口: 模板

    - 核心功能模块:
        - Request()    # 未实现,借用自 Werkzeug
        - Response()   # 未实现,借用自 Werkzeug
        - Flask()      # 核心功能类
        - url          # 封装了werkzeug.routing import Map, Rule 基于 Werkzeug 的路由模块
        - render_template # 封装了jinja2
    - 点评:
        - 对比 bottle.py框架, flask第一版的代码并不多, 但是有几个关键模块,没有自己实现.
        - 而 bottle.py 的 web框架核心组件, 除了依赖python自带的简单wsgiref.simple_server.make_server外基本都是自己实现的,未依赖任何其他第三方模块.
        - 可以查看template模板、bottle.add_route路由管理、bottle.match_url路由匹配的实现
    - 延伸:
    werkzeug.serving.WSGIRequestHandler#run_wsgi
    werkzeug.serving.make_server
    werkzeug.serving.BaseWSGIServer
    werkzeug.local.Local
    werkzeug.local.LocalStack
    werkzeug.local.LocalProxy

"""


from __future__ import with_statement
import os
import sys

from threading import local     # 作为flask对外接口使用

from jinja2 import (            # flask 部分模块实现,依赖 jinja2
    Environment,
    PackageLoader,
    FileSystemLoader
)


# 说明:
#   - flask 部分模块实现,严重依赖 werkzeug 参考资料 http://werkzeug-docs-cn.readthedocs.io/zh_CN/latest/tutorial.html#id1
#   - werkzeug 最新版本,模块组织结构发生改变.部分失效导入注释后已换成最新可用的
#
from werkzeug.wrappers import Request as RequestBase, Response as ResponseBase    # 关键依赖
from werkzeug.local import LocalStack, LocalProxy     # 文件末尾, _request_ctx_stack, current_app 中依赖
from werkzeug.wsgi import SharedDataMiddleware        # Flask() 模块 中引用
from werkzeug.utils import cached_property
# from werkzeug import create_environ    # 已失效,此处注销,更换如下
from werkzeug.test import create_environ
from werkzeug.routing import Map, Rule  # Flask 的 URL 规则基于 Werkzeug 的路由模块
from werkzeug.exceptions import HTTPException, InternalServerError
from werkzeug.contrib.securecookie import SecureCookie
# from werkzeug  import abort, redirect   # werkzeug 依赖: 本文件未使用,但导入以用作对外接口，已失效，更换如下
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from jinja2 import Markup, escape         # jinja2 的依赖: 本文件未使用,但导入以用作 对外接口


try:
    import pkg_resources,pkg_resources.resource_stream
except (ImportError, AttributeError):
    pkg_resources = None


################################################################################
#                             代码主体部分
# 说明:
#   - 主要模块:
#       - Request()     # 未独立实现, 依赖 werkzeug
#       - Response()    # 未独立实现, 依赖 werkzeug
#       - Flask()       # web 框架核心模块
#
#   - 对外接口函数:
#       - url_for()
#       - flash()
#       - get_flashed_messages
#       - render_template()
#       - render_template_string()
#
#   - 全局上下文对象:    [ 特别注意理解: 为何是上下文的?]
#       - _request_ctx_stack
#       - current_app
#       - request
#       - session
#       - g
#
#   - 辅助模块:
#       - _RequestGlobals()
#       - _RequestContext()
################################################################################

class Request(RequestBase):       # 未独立实现, 依赖 werkzeug.Request
    def __init__(self, environ):
        RequestBase.__init__(self, environ)
        self.endpoint = None
        self.view_args = None
        print("Request environ:", environ)


class Response(ResponseBase):     # 未独立实现, 依赖 werkzeug.Response
    default_mimetype = 'text/html'


class _RequestGlobals(object):    # 预定义接口: _RequestContext() 中 引用
    pass


class _RequestContext(object):    # 请求上下文, 基本上保函了请求的所有信息，可在打印中查看
    def __init__(self, app, environ):
        self.app = app
        self.url_adapter = app.url_map.bind_to_environ(environ)
        self.request = app.request_class(environ)
        # 带上下文的 session 实现
        self.session = app.open_session(self.request)
        # 关键: 待上下文的 g 实现
        self.g = _RequestGlobals()    # 预定义接口
        self.flashes = None
        print("-----------------0")
        print(to_dict(self.app))
        print("-----------------1")
        print(to_dict(self.url_adapter))
        print("-----------------2")
        print(to_dict(self.request))
        print("-----------------3")
        # print(to_dict(self.session))
        print("-----------------4")
        print(to_dict(self.g))
        print("-----------------5")
        """
        -- -- -- -- -- -- -- -- - 0 {
            'error_handlers': {
                404: < function page_not_found at 0x0000000003425908 >
            },
            'package_name': '__main__',
            'root_path': 'D:\\gitlab_camel\\flask_dome',
            'jinja_env': < jinja2.environment.Environment object at 0x00000000032A7978 > ,
            'before_request_funcs': [ < function before at 0x0000000003425588 > ],
            'view_functions': {
                'index': < function index at 0x00000000034256D8 > ,
                'hello4': < function hello4 at 0x0000000003425898 > ,
                'hello3': < function hello3 at 0x0000000003425828 > ,
                '/hello2': < function hello2 at 0x0000000003425668 > ,
                'hello1': < function hello1 at 0x0000000003425748 >
            },
            'template_context_processors': [ < function _default_template_ctx_processor at 0x00000000031EBA58 > ],
            'debug': True,
            'url_map': Map([ < Rule '/hello1' (HEAD, GET) - > hello1 > , <
                Rule '/hello2' (HEAD, GET) - > />, <
                Rule '/' (HEAD, GET) - > index > , <
                Rule '/hello4/<post_id>' (HEAD, GET) - > hello4 > , <
                Rule '/static/<filename>' - > static > , <
                Rule '/hello3/<username>' (HEAD, GET) - > hello3 >
            ]),
            'wsgi_app': < werkzeug.wsgi.SharedDataMiddleware object at 0x000000000303A400 > ,
            'after_request_funcs': [ < function after at 0x00000000034255F8 > ]
        }
        -- -- -- -- -- -- -- -- - 1 {
            'map': Map([ < Rule '/hello1' (HEAD, GET) - > hello1 > , <
                Rule '/hello2' (HEAD, GET) - > />, <
                Rule '/' (HEAD, GET) - > index > , <
                Rule '/hello4/<post_id>' (HEAD, GET) - > hello4 > , <
                Rule '/static/<filename>' - > static > , <
                Rule '/hello3/<username>' (HEAD, GET) - > hello3 >
            ]),
            'server_name': u '127.0.0.1:3000',
            'url_scheme': u 'http',
            'query_args': u '',
            'script_name': u '/',
            'path_info': u '/',
            'default_method': u 'GET',
            'subdomain': u ''
        }
        -- -- -- -- -- -- -- -- - 2 {
            'view_args': None,
            'url': u 'http://127.0.0.1:3000/',
            'shallow': False,
            'environ': {
                'wsgi.multiprocess': False,
                'SERVER_SOFTWARE': 'Werkzeug/0.14.1',
                'SCRIPT_NAME': '',
                'REQUEST_METHOD': 'GET',
                'PATH_INFO': '/',
                'SERVER_PROTOCOL': 'HTTP/1.1',
                'QUERY_STRING': '',
                'werkzeug.server.shutdown': < function shutdown_server at 0x00000000034EACF8 > ,
                'HTTP_USER_AGENT': 'curl/7.61.0',
                'SERVER_NAME': '0.0.0.0',
                'REMOTE_PORT': 63034,
                'wsgi.url_scheme': 'http',
                'SERVER_PORT': '3000',
                'werkzeug.request': < Request 'http://127.0.0.1:3000/' [GET] > ,
                'wsgi.input': < socket._fileobject object at 0x0000000003430A20 > ,
                'HTTP_HOST': '127.0.0.1:3000',
                'wsgi.multithread': False,
                'HTTP_ACCEPT': '*/*',
                'wsgi.version': (1, 0),
                'wsgi.run_once': False,
                'wsgi.errors': < open file '<stderr>',
                mode 'w'
                at 0x0000000000572150 > ,
                'REMOTE_ADDR': '127.0.0.1'
            },
            'endpoint': None
        }
        -- -- -- -- -- -- -- -- - 3
        -- -- -- -- -- -- -- -- - 4 {}
        -- -- -- -- -- -- -- -- - 5
        """


    # 栈顶存放的是当前活跃的request，使用栈是为了获取当前的活跃request对象。
    def __enter__(self):    # 请求的上下文入栈
        _request_ctx_stack.push(self)
        print("get_ident of this request:",_request_ctx_stack.__ident_func__()) # 查看一下这个请求的上下文存储的key:vlaue 中key的值，也就是线程值或者协程，环境安装了greenlet时优先使用
        # ('get_ident of this request:', <greenlet.greenlet object at 0x7f1baafe9410>)  ('get_ident of this request:', 3740)

    def __exit__(self, exc_type, exc_value, tb):    # 请求的上下文出栈
        if tb is None or not self.app.debug:
            _request_ctx_stack.pop()


def url_for(endpoint, **values):    # 实现依赖: werkzeug.LocalStack 模块
    return _request_ctx_stack.top.url_adapter.build(endpoint, values)


def flash(message):     # 向页面 输出 一条 消息
    # session : 文件末尾定义的 全局上下文对象
    session['_flashes'] = (session.get('_flashes', [])) + [message]


def get_flashed_messages():
    flashes = _request_ctx_stack.top.flashes
    if flashes is None:
        _request_ctx_stack.top.flashes = flashes = \
            session.pop('_flashes', [])
    return flashes


def render_template(template_name, **context):    # 渲染模板页面: 通过查找 templates 目录
    # current_app : 文件结尾定义的 全局上下文对象
    # 依赖 jinja2
    print("context:",context)
    current_app.update_template_context(context)
    print ("current_app:",to_dict(current_app))
    return current_app.jinja_env.get_template(template_name).render(context)


def render_template_string(source, **context):   # 渲染模板页面: 通过传入的模板字符串
    # 同上
    current_app.update_template_context(context)
    return current_app.jinja_env.from_string(source).render(context)


def _default_template_ctx_processor():    # 默认的模板上下文 处理机
    reqctx = _request_ctx_stack.top     # 文件末尾定义的 全局上下文对象

    return dict(
        request=reqctx.request,
        session=reqctx.session,
        g=reqctx.g
    )


def _get_package_path(name):     # 获取 模块包 路径, Flask() 中 引用
    """Returns the path to a package or cwd if that cannot be found."""
    try:
        return os.path.abspath(os.path.dirname(sys.modules[name].__file__))
    except (KeyError, AttributeError):
        return os.getcwd()

# 自定义方便查询属性
def to_dict(instence):
    return instence.__dict__

###################################################################
#                       核心功能接口
###################################################################
class Flask(object):
    """
        from flask import Flask
        app = Flask(__name__)
    """
    request_class = Request      # 请求类
    response_class = Response    # 响应类
    static_path = '/static'      # 静态资源路径
    secret_key = None            # 密钥配置
    session_cookie_name = 'session'      # 安全cookie
    # 模板参数
    jinja_options = dict(
        autoescape=True,
        extensions=['jinja2.ext.autoescape', 'jinja2.ext.with_']
    )

    def __init__(self, package_name):
        print("Flask __init__ start!")
        self.debug = False     # 调试模式开关
        # 注意:
        #   - 这个参数,不是随便乱给的
        #   - 要跟实际的 项目工程目录名对应,否则无法找到对应的工程
        self.package_name = package_name
        # 注意:
        #   - 调用前面定义的 全局私有方法
        #   - 依赖前面的传入参数, 通过该参数, 获取 项目工程源码根目录.
        self.root_path = _get_package_path(self.package_name)    # 获取项目根目录
        self.view_functions = {}         # 视图函数集
        self.error_handlers = {}           # 出错处理
        self.before_request_funcs = []     # 预处理
        self.after_request_funcs = []      # 结束清理
        self.template_context_processors = [_default_template_ctx_processor]

        # todo: 待深入
        self.url_map = Map()    # 关键依赖: werkzeug.routing.Map
        if self.static_path is not None:    # 处理静态资源
            #
            # todo: 待深入 关键依赖: werkzeug.routing.Rule
            self.url_map.add(Rule(self.static_path + '/<filename>',
                                  build_only=True, endpoint='static'))

            if pkg_resources is not None:
                target = (self.package_name, 'static')
            else:
                target = os.path.join(self.root_path, 'static')

            #
            # todo: 待深入, 关键依赖: werkzeug.SharedDataMiddleware
            self.wsgi_app = SharedDataMiddleware(self.wsgi_app, {
                self.static_path: target
            })
        # todo: 待深入, jinja2 模板配置
        self.jinja_env = Environment(loader=self.create_jinja_loader(), **self.jinja_options)
        self.jinja_env.globals.update(
            url_for=url_for,
            get_flashed_messages=get_flashed_messages
        )
        print("Flask __init__ end!")

    # 加载 templates 目录文件
    def create_jinja_loader(self):
        if pkg_resources is None:
            # 加载 模板目录 文件
            return FileSystemLoader(os.path.join(self.root_path, 'templates'))
        return PackageLoader(self.package_name)

    def update_template_context(self, context):
        reqctx = _request_ctx_stack.top
        print("reqctx:",to_dict(reqctx))
        print("template_context_processors:", self.template_context_processors)
        for func in self.template_context_processors:
            print("func:",func())
            context.update(func())

    # 对外运行接口: 借用werkzeug.run_simple 实现
    def run(self, host='localhost', port=5000, **options):
        # from werkzeug import run_simple
        from werkzeug.serving import run_simple # 关键依赖: 核心运行模块
        if 'debug' in options:
            self.debug = options.pop('debug')
        options.setdefault('use_reloader', self.debug)
        options.setdefault('use_debugger', self.debug)
        return run_simple(host, port, self, **options)    # 依赖 werkzeug->werkzeug.serving.make_server->werkzeug.serving.BaseWSGIServer，
        # 主要就是建立socket监听，绑定server、app，其中内容丰富还需深入

    def test_client(self):
        # from werkzeug import Client        # todo: 待深入, 关键依赖 已失效 更换如下
        from werkzeug.test import Client
        return Client(self, self.response_class, use_cookies=True)

    def open_resource(self, resource):
        """Opens a resource from the application's resource folder.  To see
        how this works, consider the following folder structure::
            /myapplication.py
            /schemal.sql
            /static
                /style.css
            /template
                /layout.html
                /index.html
        If you want to open the `schema.sql` file you would do the
        following::
            with app.open_resource('schema.sql') as f:
                contents = f.read()
                do_something_with(contents)
        """
        if pkg_resources is None:
            return open(os.path.join(self.root_path, resource), 'rb')
        return pkg_resources.resource_stream(self.package_name, resource)

    # 关键接口: 创建 or 打开一个 会话(session)
    #   - 实现方式: 使用 cookie 实现
    #   - 默认把全部session数据, 存入一个 cookie 中.
    #   - 对比 flask-0.4 版本, 部分重构
    def open_session(self, request):
        key = self.secret_key
        if key is not None:
            return SecureCookie.load_cookie(request, self.session_cookie_name,
                                            secret_key=key)

    # 关键接口: 更新session-->所以说flask的session是依赖cookie的，Flask中的session是存在浏览器中
    def save_session(self, session, response):
        if session is not None:
            session.save_cookie(response, self.session_cookie_name)

    # 添加路由规则, route() 装饰器的实现,依赖
    def add_url_rule(self, rule, endpoint, **options):
        """
        Basically this example::
            @app.route('/')
            def index():
                pass
        Is equivalent to the following::
            def index():
                pass
            app.add_url_rule('index', '/')
            app.view_functions['index'] = index
        """
        options['endpoint'] = endpoint
        options.setdefault('methods', ('GET',))

        # 路由规则添加
        self.url_map.add(Rule(rule, **options))

    # 路由装饰器定义:
    def route(self, rule, **options):
        """A decorator that is used to register a view function for a
        given URL rule.  Example::

            @app.route('/')
            def index():
                return 'Hello World'
        The following converters are possible:

        =========== ===========================================
        `int`       accepts integers
        `float`     like `int` but for floating point values
        `path`      like the default but also accepts slashes
        =========== ===========================================

        Here some examples::

            @app.route('/')
            def index():
                pass

            @app.route('/<username>')
            def show_user(username):
                pass

            @app.route('/post/<int:post_id>')
            def show_post(post_id):
                pass
        """
        def decorator(f):
            self.add_url_rule(rule, f.__name__, **options)    # 添加路由规则
            self.view_functions[f.__name__] = f               # 更新 视图函数集合, 前面定义,{}
            return f
        return decorator

    # 错误处理装饰器定义:
    def errorhandler(self, code):
        """
            @app.errorhandler(404)
            def page_not_found():
                return 'This page does not exist', 404

            def page_not_found():
                return 'This page does not exist', 404
            app.error_handlers[404] = page_not_found
        """
        def decorator(f):
            self.error_handlers[code] = f     # 前述定义{}
            return f
        return decorator

    # 请求前,预处理:
    #   - 注册预处理函数
    def before_request(self, f):
        """Registers a function to run before each request."""
        self.before_request_funcs.append(f)
        return f

    # 请求结束, 清理工作:
    #   - 注册清理函数
    def after_request(self, f):
        """Register a function to be run after each request."""
        self.after_request_funcs.append(f)
        return f

    # 模板上下文处理函数
    def context_processor(self, f):
        """Registers a template context processor function."""
        self.template_context_processors.append(f)
        return f

    # 请求匹配:
    def match_request(self):
        rv = _request_ctx_stack.top.url_adapter.match()
        request.endpoint, request.view_args = rv
        return rv

    # 处理请求:
    #   - 处理 路由URL 和 对应的 视图函数
    def dispatch_request(self):
        try:
            endpoint, values = self.match_request()    # 请求匹配
            return self.view_functions[endpoint](**values)  # 视图处理集中的函数如下，以url为key，以对应的函数为value，返回的就是对应url下逻辑的处理结果

            # 'view_functions': {
            #     'index': < function index at 0x00000000034256D8 > ,
            #     'hello4': < function hello4 at 0x0000000003425898 > ,
            #     'hello3': < function hello3 at 0x0000000003425828 > ,
            #     '/hello2': < function hello2 at 0x0000000003425668 > ,
            #     'hello1': < function hello1 at 0x0000000003425748 >
            # },

        except HTTPException, e:
            handler = self.error_handlers.get(e.code)
            if handler is None:
                return e
            return handler(e)
        except Exception, e:
            handler = self.error_handlers.get(500)
            if self.debug or handler is None:
                raise
            return handler(e)

    # 返回响应
    def make_response(self, rv):
        if isinstance(rv, self.response_class): # 适配自定义的response
            return rv
        if isinstance(rv, basestring):
            return self.response_class(rv)
        if isinstance(rv, tuple):
            return self.response_class(*rv)
        return self.response_class.force_type(rv, request.environ)

    # 请求前, 执行预处理工作中:
    def preprocess_request(self):
        for func in self.before_request_funcs:
            rv = func()    # 执行预处理函数
            if rv is not None:
                return rv

    # 在返回响应前, 作 清理工作, 与上配对
    def process_response(self, response):
        session = _request_ctx_stack.top.session
        if session is not None:
            self.save_session(session, response)     # 保存 session

        for handler in self.after_request_funcs:     # 请求结束后, 清理工作
            response = handler(response)
        return response

    # flask的核心函数
    def wsgi_app(self, environ, start_response):
        """
            app.wsgi_app = MyMiddleware(app.wsgi_app)   中间层
        """
        with self.request_context(environ):     # 请求上下文
            rv = self.preprocess_request()      # 请求前, 预处理
            if rv is None:
                rv = self.dispatch_request()    # 匹配视图函数、处理请求
            response = self.make_response(rv)            # 返回响应
            response = self.process_response(response)   # 返回响应前, 作清理工作
            print("tag1:",response)
            return response(environ, start_response)

    # 请求上下文
    def request_context(self, environ):
        """
        Example usage:
            with app.request_context(environ):
                do_something_with(request)
        """
        return _RequestContext(self, environ)     # 请求上下文, 上述已定义该模块

    def test_request_context(self, *args, **kwargs):
        return self.request_context(create_environ(*args, **kwargs))

    def __call__(self, environ, start_response):  # 类实例app变成一个可调用对象, 但是这个environ是怎么来的呢？--> 打断点可以看出 werkzeug.serving.WSGIRequestHandler --> application_iter = app(environ, start_response)
        """适配wsgi规范
        SocketServer.BaseServer#serve_forever 监听端口
        r, w, e = _eintr_retry(select.select, [self], [], [],poll_interval)
        if self in r:
            self._handle_request_noblock()
        当有请求进来后触发处理当前请求的逻辑，这是调用__call__的第一步
        但其绑定是在run方法中的run_simple中
        """
        print("environ:",environ)
        print("start_response:",start_response)
        return self.wsgi_app(environ, start_response)


###################################################################
#                     全局上下文变量定义(context locals)
# 说明:
#   - 此处全局的 g, session, 需要深入理解
#   - 需要深入去看 werkzeug.LocalStack() 的实现 Local-->LocalStack-->LocalProxy 这三个的关系参考下面的链接
#   https://www.jianshu.com/p/3f38b777a621，https://blog.csdn.net/barrysj/article/details/51519254
#   python中有threading local处理方式，在多线程环境中将变量按照线程id区分，由于协程在Python web中广泛使用，所以threading local不再满足需要
#   local中优先使用greenlet协程，其次是线程id。localstack相当于在本协程（线程）中将数据以stack的形式存储(通过封装local来实现)。
#   LocalProxy就是local的代理。重载了很多运算符，方便变量值得动态更新和获取，
#
###################################################################

_request_ctx_stack = LocalStack()    # 依赖 werkzeug.LocalStack 模块-->`Local`堆栈
current_app = LocalProxy(lambda: _request_ctx_stack.top.app)
request = LocalProxy(lambda: _request_ctx_stack.top.request)

#   - g: 请求上下文 栈对象
#   - session: 请求上下文 栈对象
session = LocalProxy(lambda: _request_ctx_stack.top.session)    # flash()函数中引用
g = LocalProxy(lambda: _request_ctx_stack.top.g)
