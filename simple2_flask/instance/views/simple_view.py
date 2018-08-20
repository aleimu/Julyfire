# -*- coding:utf-8 -*-

from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound

from ..tools.user_tools import check_user, mark_user

simple_view = Blueprint('simple_view', __name__, template_folder='templates')


@simple_view.route('/', defaults={'page': 'index'})
@simple_view.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)


@simple_view.route('/hello')
def hello_world():
    return 'Simple_view Say Hello World!'


@simple_view.route('/usercheck')
def usercheck():
    username = request.values.get("username", "")
    password = request.values.get("password", "")
    check_user(username, password)
    return 'Simple_view Say usercheck!'


@simple_view.route('/usermark')
def usermark():
    username = request.values.get("username", "")
    mark_user(username)
    return 'Simple_view Say usermark!'
