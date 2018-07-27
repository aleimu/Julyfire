# -*- coding: utf-8 -*-
from flask01 import Flask, g, session, request, current_app,render_template,Response,Request

app = Flask(__name__)
app.secret_key="secret_key"

@app.before_request
def before():
    print("before_request")
    if request.path == "/hello2":
        print("request.path",request.path)

@app.after_request
def after(response):
    if request.path == "/hello":
        print("request.path",request.path)
    print("after_request:",response)
    return response


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/hello1')
def hello1():
    print("hello1 start!")
    print("hello1 end!")
    return "hello1"


def hello2():
    print("hello2 start!")
    print("hello2 end!")
    return "hello2"

# todo: 有点问题
app.add_url_rule(rule='/hello2', endpoint='/')
app.view_functions['/hello2'] = hello2


@app.route('/hello3/<username>')
def hello3(username):
    print("hello3 start!")
    response = app.make_response(rv="set flask session by cookie")
    session['username'] = "this is session!"
    print("session_save:", app.save_session(session,response))  # 通过make_response构造返回,再把session加到cookie中
    # Cookie:session="ggJv7/AbUuQVuDyk3Is1fPGtw0A=?username=Uyd0aGlzIGlzIHNlc3Npb24hJwpwMAou"
    return response


@app.route('/hello4/<int:post_id>')
def hello4(post_id):
    print("hello4 start!")
    print("g:",g,g.__dict__)
    print("session:", session,session.__dict__)
    print("current_app:", current_app,current_app.__dict__)
    print("Request:", Request,Request.__dict__)
    print("Response:", Response,Response.__dict__)
    print("hello4 end!")
    return "hello4 %s" % post_id


@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=3000,debug=True,threaded=True)