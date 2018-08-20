# -*- coding:utf-8 -*-
__author__ = "lgj"
__date__ = "2018-8-14"

from flask import Blueprint, abort, jsonify, request

bb = Blueprint('bb', __name__, static_folder='static2', static_url_path='/bb/', template_folder='template2')


@bb.before_request
def before_request():
    print("*****bb.before_request*****")


@bb.teardown_request
def teardown_request(err):
    print("*****bb.teardown_request*****")


@bb.route('/')
def users():
    print(vars(bb))
    return "bb"


"""
{
	'url_prefix': None,
	'name': 'bb',
	'root_path': 'C:\\Users\\lenovo\\Desktop\\\xb5\xe3\xb5\xce\xbb\xfd\xc0\xdb\\Julyfire\\flask_blueprint',
	'_static_folder': 'static2',
	'deferred_functions': [ < function < lambda > at 0x0000000002F25358 > , < function < lambda > at 0x0000000002F252E8 > , < function < lambda > at 0x0000000002F250B8 > ],
	'template_folder': 'template2',
	'subdomain': None,
	'import_name': 'bblueprint',
	'url_values_defaults': {},
	'_got_registered_once': True,
	'_static_url_path': '/bb/'
}

"""
