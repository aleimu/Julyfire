# Flask User Management

[![Build Status](https://travis-ci.org/mjhea0/flask-basic-registration.svg?branch=master)](https://travis-ci.org/mjhea0/flask-basic-registration)

Starter app for managing users - login/logout and registration.
本项目主要是在 https://github.com/mjhea0/flask-basic-registration

的基础上增加了email的确认、密码修改、密码忘记重置三个功能，优化了目录结构适合大型项目。

主要是自己的学习过程，若用于生产推荐使用更好的模块: Flask-User、Flask-Security

## QuickStart

### Set Environment Variables

```sh
$ export APP_SETTINGS="project.config.DevelopmentConfig"
```

or

```sh
$ export APP_SETTINGS="project.config.ProductionConfig"
```

### Update Settings in Production

1. `SECRET_KEY`
1. `SQLALCHEMY_DATABASE_URI`

### Create DB

```sh
$ python manage.py create_db
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py create_admin
```

### Run

```sh
$ python manage.py runserver
```

### Testing

Without coverage:

```sh
$ python manage.py test
```

With coverage:

```sh
$ python manage.py cov
```

把邮箱地址编码成令牌,并且令牌也包含一个时间戳，该时间戳是让我们设置一个令牌在什么时间内有效的时间限制。

Bcrypt 算法强烈地被推荐的原因之一就是”未来的适应性“。这就意味着随着时间的推移，当计算能力变得越来越便宜的时候，我们可以把它变得越来越困难地被暴力方式来破解，这种暴力方式就是上百万次的猜测密码。我们使用越多的”循环“来散列密码，将会花费越多的时间来猜测。如果我们在存储密码之前使用算法散列密码 20 次的话，攻击者必须散列每一个它们的猜测 20 次。

请记住如果我们散列密码超过 20 次的话，我们的应用程序需要花费很长的一段时间来返回响应，具体要取决于什么时候处理完成。这就意味着当选择使用的”循环数“的时候，我们必须平衡安全和可用性。我们可以在给定时间内计算完成的”循环“取决于提供我们应用程序的计算资源。在 0.25 到 0.5 秒之间的时间内散列密码是一个很好的体验。我们应该尝试使用的”循环“至少为 12。

```python
from flask.ext.bcrypt import generate_password_hash

# Change the number of rounds (second argument) until it takes between
# 0.25 and 0.5 seconds to run.
generate_password_hash('password1', 12)
```

#### 参考
- http://python.jobbole.com/81410/
- http://www.pythondoc.com/exploreflask/users.html
- https://github.com/mjhea0/flask-basic-registration
- http://www.pythondoc.com/flask-mega-tutorial/