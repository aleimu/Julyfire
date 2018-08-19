# 配置数据库类型及路径
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:lgj123@localhost:3306/simple?charset=utf8'
# 数据改变后自动提交
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
# 数据变化的自动警告关闭
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 显示数据库操作的原sql
SQLALCHEMY_ECHO = True
