# -*- coding:utf-8 -*-

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

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
