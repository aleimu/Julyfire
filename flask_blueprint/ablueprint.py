# -*- coding:utf-8 -*-
__author__ = "lgj"
__date__ = "2018-8-14"

from flask import Blueprint, abort, jsonify, redirect, url_for

ab = Blueprint('ab', __name__, static_folder='static1', static_url_path='/ab/', template_folder='template1')


@ab.before_request
def before_request():
    print("*****ab.before_request*****")


@ab.teardown_request
def teardown_request(err):
    print("*****ab.teardown_request*****")


@ab.route('/')
def users():
    print("ab-dict:$s", vars(ab))
    return "ab"


@ab.route('/add')
def add():
    print ("this is ab.add")
    return redirect(url_for('cb.add'))
