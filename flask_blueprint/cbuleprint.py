# -*- coding:utf-8 -*-
__author__ = "lgj"
__date__ = "2018-8-14"

from flask import Blueprint, abort, jsonify, request

cb = Blueprint('cb', __name__)


@cb.before_request
def before_request():
    print("*****cb.before_request*****")


@cb.teardown_request
def teardown_request(err):
    print("*****cb.teardown_request*****")


@cb.route('/')
def users():
    print("cb-dict:", vars(cb))
    return "cb"


@cb.route('/add')
def add():
    print ("this is cb.add")
    return "add"
