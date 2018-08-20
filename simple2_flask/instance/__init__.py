# -*- coding:utf-8 -*-

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis

from .config import config

db = SQLAlchemy()
redis_store = FlaskRedis()


# app工厂
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    redis_store.init_app(app)

    @app.before_request
    def before_request():
        print("app.before_request")
        pass

    @app.teardown_request
    def handle_teardown_request(exception):
        print("app.teardown_request")
        db.session.remove()

    @app.errorhandler(401)
    def user_not_auth(error):
        return jsonify(error="not find this user", code=401)

    @app.errorhandler(404)
    def user_not_find(error):
        return jsonify(error="not find", code=404)

    @app.errorhandler(500)
    def server_internal_err(error):
        return jsonify(error="server internal error", code=500)

    # 注册蓝图
    from .views.simple_page import simple_page
    from .views.simple_view import simple_view

    app.register_blueprint(simple_page, url_prefix='/pages')
    app.register_blueprint(simple_view)
    print("all the app info:", vars(app))
    return app
