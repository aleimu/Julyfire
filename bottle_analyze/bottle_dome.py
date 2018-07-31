# -*- coding: utf-8 -*-
from bottle import route, run, request, response, send_file, abort,template
import time

@route('/')
def hello_world():
    return 'Hello World!'


@route('/index.html')
def index():
    time.sleep(60)
    return '<a href="/hello/lgj">to_lgj</a>'


@route('/hello/:name')
def hello_name(name):
    return 'Hello %s!' % name

@route('/hello')
def hello_name2():
    send_file(filename='index.html', root='./')

#@route("/login", method='PUT')
#def login_submit():
#    return template("login.html")  #template can not is file


@route("/login", method='PUT')
def login_submit():
    name = request.POST['name']
    pwd = request.POST['pwd']
    if name and pwd:
        return template('<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">' + \
                       '<html><head><title>HELLO {{name}}: {{pwd}}</title>' + \
                       '</head><body><h1>HELLO {{name}}: {{pwd}}</h1>' + \
                       '<p>Sorry, the requested URL {{pwd}} caused an pwd.</p>',
                       name=name,
                       pwd=pwd
                       )
@route('/login1', method='POST')
def login_submit1():
    name = request.POST['name']
    if name :
        return 'Hello %s!' % name

@route('/login2', method='POST')
def login_submit2():
    name = request.POST['name']
    pwd = request.POST['pwd']
    if name and pwd:
        return 'Hello %s!,your passwd %s' % (name,pwd)

@route('/static/:filename#.*#')
def static_file(filename):
    send_file(filename, root='/path/to/static/files/')


run(host='localhost', port=8080)

#test by httpie in cmd
#http GET http://127.0.0.1:8080/
#http -f POST http://127.0.0.1:8080/login2 name=dwadada pwd=dwadad
#http -f PUT http://127.0.0.1:8080/login name="dwadada", pwd="dwadad"