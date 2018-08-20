# -*- coding:utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    # DB Config
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1:3306/test?charset=utf8'
    REDIS_URL = "redis://:@localhost:6379/1"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    TOKEN_EXPIRE = 3600 * 2
    DEBUG = True
    # 调度系统密钥
    SECURITY_KEY = 'df6ebcb8-93c4-11e7-a2ab-9801a7aef71d'

    # Upload Config
    # =============
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    UPLOAD_FOLDER = '../upload/'
    FRONT_URL = '../carrier-web/'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'pdf'])


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'mysql://camel:camel@10.129.222.49:3306/camel?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = "redis://:@localhost:6379/5"
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'dev': Config,
    'test': TestingConfig,
    'pro': ProductionConfig,
}
