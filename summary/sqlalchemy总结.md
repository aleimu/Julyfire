#### mysql-5.7安装
https://blog.csdn.net/since_1904/article/details/70233403
#### flask-sqlalchemy教程
http://www.pythondoc.com/flask-sqlalchemy/
#### sqlalchemy文档
https://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html
#### 中文翻译版
https://www.jianshu.com/p/8d085e2f2657
#### sqlalchemy查询使用 
https://www.cnblogs.com/jingqi/p/8059673.html
#### MySQL外键与外键关系说明(简单易懂)
https://www.cnblogs.com/programmer-tlh/p/5782451.html

relationship和ForeignKey这个两个属性决定了表之间关系的属性,ForeignKey是mysql的本身的属性,relationship是orm的属性,relationship存在的用途感觉是为了方便类表的控制,可以像控制类的属性一样改变
具体参考:
http://docs.sqlalchemy.org/en/latest/orm/backref.html#relationships-backref
http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html
##### relationship是为了简化联合查询join等，创建的两个表之间的虚拟关系，这种关系与标的结构时无关的。他与外键十分相似，确实，他必须在外键的基础上才允许使用，使两个表之间产生管理，类似于合成一张表，可以直接取出关联的表，进行获取数据，而不需要join操作
https://www.cnblogs.com/ssyfj/p/8568013.html

---
```python
from sqlalchemy import create_engine # 创建一个和mysql数据库之间的连接引擎对象
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship, backref # 引入需要的模块
from sqlalchemy.ext.declarative import declarative_base # 创建基础类
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound

BaseModel = declarative_base()

engine = create_engine("mysql+pymysql://root:lgj123@localhost/myschool2", encoding="utf8", echo=True)


# 创建用户类型
class User(BaseModel):
    # 定义和指定数据库表之间的关联
    __tablename__ = 'user'
    # 创建字段类型
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(50))
    #addresses = relationship("Address", order_by="Address.id", backref="user")

    def __repr__(self):
        return '< User-->id:%s,name:%s,fullname:%s,password:%s >' % (self.id,self.name,self.fullname,self.password)


#建立联系（外键）
class Address(BaseModel):
    __tablename__ = 'addresses'
    id= Column(Integer, primary_key=True)
    email_address = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", backref=backref('addresses',order_by=id))
    def __repr__(self):
        return"< Address -->id:%s,email_address:%s,user_id:%s,user:%s>" % (self.id,self.email_address,self.user_id,self.user)

BaseModel.metadata.create_all(engine)# 创建表


from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


# ed_user1 = User(name='ed1', fullname='Ed Jones', password='edspassword')
# ed_user2 = User(name='ed2', fullname='Ed Jones', password='edspassword')
# ed_user3 = User(name='ed3', fullname='Ed Jones', password='edspassword')
# session.add(ed_user1)
# session.add(ed_user2)
# session.add(ed_user3)     # 这三条就算未commit到数据库中，但还是能被下面的查询语句查到，这里需要注意!
#
# session.commit()
print("-------------1")
for instance in session.query(User).order_by(User.id):
    print (instance.name,instance.fullname,instance.password)
print("-------------2")
for name, fullname in session.query(User.name,User.fullname):
    print (name, fullname)
print("-------------3")


query = session.query(User).filter(User.name.like('%ed%')).order_by(User.id)
user_all = query.all()
print("-------------4")
print("user_all:",user_all)
print("first:",query.first())
try:
    user1 = query.one()
    print ("user1:",user1)
except Exception as e:
    print("e:",e)
print("-------------5")
try:
    user2 = query.filter(User.id == 20).one()
    print ("user2:",user2)
except Exception as e:
    print("e:",e)
print("-------------6")
from sqlalchemy import text
for user in session.query(User).filter(text("id<25")).order_by(text("id")).all():
    print("user:",user)
print("-------------7")
user_text=session.query(User).filter(text("id<:value and name=:name")).params(value=50, name='ed3').order_by(User.id).one()
print("user_text:",user_text)
print("-------------8")
print("count:",session.query(User).filter(User.name.like('%ed%')).count())
print("-------------9")

# jack = User(name='jack', fullname='Jack Bean', password='gjffdd')
# print ("jack.addresses:",jack.addresses)
# jack.addresses = [Address(email_address='jack@google.com'),Address(email_address='j25@yahoo.com')]
# session.add(jack)
# session.commit()
print("-------------10")
for u,a in session.query(User, Address).filter(User.id==Address.user_id).filter(Address.email_address=='jack@google.com').all():
    print ("user:",u)
    print ("address:",a)
print("-------------11")
for u,a in session.query(User, Address).join(Address).filter(Address.email_address=='jack@google.com').all():
    print("user:", u)
    print("address:", a)
print("-------------12")
ad1=Address(email_address='123@qq.com',user_id=1)
#ad1.user=1
ad2=Address(email_address='123@qq.com',user_id=1)
#ad2.user=1

session.add(ad1)
session.add(ad2)
session.commit()


print("-------------13")
```
---
#### 返回列表(List)和单项(Scalar)
```python
很多Query的方法执行了SQL命令并返回了取出的数据库结果。

all()返回一个列表:
>>> query = session.query(User).filter(User.name.like('%ed')).order_by(User.id)
SQL>>> query.all()
[<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>,
      <User(name='fred', fullname='Fred Flinstone', password='blah')>]
      
first()返回至多一个结果，而且以单项形式，而不是只有一个元素的tuple形式返回这个结果.
>>> query.first()
<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>

one()返回且仅返回一个查询结果。当结果的数量不足一个或者多于一个时会报错。
>>> user = query.one()
Traceback (most recent call last):
...
MultipleResultsFound: Multiple rows were found for one()
没有查找到结果时：

>>> user = query.filter(User.id == 99).one()
Traceback (most recent call last):
...
NoResultFound: No row was found for one()

one_or_none()：从名称可以看出，当结果数量为0时返回None， 多于1个时报错

scalar()和one()类似，但是返回单项而不是tuple


```
---
#### 使用关键字变量过滤查询结果，filter 和 filter_by都适用，下面列出几个常用的操作：
```python
query.filter(User.name =='ed') #equals
query.filter(User.name !='ed') #not equals
query.filter(User.name.like('%ed%')) #LIKE
uery.filter(User.name.in_(['ed','wendy', 'jack'])) #IN
query.filter(User.name.in_(session.query(User.name).filter(User.name.like('%ed%'))#IN
query.filter(~User.name.in_(['ed','wendy', 'jack']))#not IN
query.filter(User.name ==None)#is None
query.filter(User.name !=None)#not None

from sqlalchemy import and_
query.filter(and_(User.name =='ed',User.fullname =='Ed Jones')) # and
query.filter(User.name =='ed',User.fullname =='Ed Jones') # and
query.filter(User.name =='ed').filter(User.fullname =='Ed Jones')# and

from sqlalchemy import or_
query.filter(or_(User.name =='ed', User.name =='wendy')) #or
query.filter(User.name.match('wendy')) #match
```
---
#### 使用字符串SQL

字符串能使Query更加灵活，通过text()构造指定字符串的使用，这种方法可以用在很多方法中，像filter()和order_by()。
```python
from sqlalchemy import text
for user in session.query(User).filter(text("id<224")).order_by(text("id")).all()

绑定参数可以指定字符串，用params()方法指定数值。
session.query(User).filter(text("id<:value and name=:name")).params(value=224, name='fred').order_by(User.id).one()

如果要用一个完整的SQL语句，可以使用from_statement()。
session.query(User).from_statement(text("SELECT* FROM users where name=:name")).params(name='ed').all()
```
---
#### 通过text的存在可以灵活的构造查询请求，就像拼凑字符串一样简单，根据查询的条件不同拼凑出合适的字符串
```python
def table_search(page, per_page, name, status, trans_type, start_port, end_port):

    statement = "1=1"
    if name:
        statement += " and name like '%s%s%s' " % ('%', name, '%')
    if status:
        statement += " and status = '%s' " % status
    if trans_type:
        statement += " and trans_type = '%s' " % trans_type
    if start_port:
        statement += " and start_port_name like '%s%s%s' " % ('%', start_port, '%')
    if end_port:
        statement += " and end_port_name like '%s%s%s' " % ('%', end_port, '%')
    lines = mytable.query.filter(statement).order_by(mytable.update_at.desc(),
                                                     mytable.create_at.desc()).paginate(int(page), int(per_page), False)
    count = mytable.query.filter(statement).count()
    lines_list = []
    for item in lines.items:
        line = item.to_dict()
        if line['create_at']:
            line['create_at'] = datetime.datetime.strftime(line['create_at'], '%Y-%m-%d %H:%M')
        if line['update_at']:
            line['update_at'] = datetime.datetime.strftime(line['update_at'], '%Y-%m-%d %H:%M')
        lines_list.append(line)
    result = {"count": count, "lines": lines_list}
    db.session.remove()
    return None, result

```
---

在看项目中看到 session.query(User).filter("id<224")) 在字符串外并未构造成text("id<224")也是可以的，心存疑惑，需要验证一下。
已验证--->目前使用的Flask-1.0.2版本中是支持不加text的，但会在不加的时候报出warning，具体的代码实现如下：
```python
@_generative(_no_statement_condition, _no_limit_offset)
def filter(self, *criterion):
    """
    session.query(MyClass).filter(MyClass.name == 'some name')
    session.query(MyClass).\\
            filter(MyClass.name == 'some name', MyClass.id > 5)

    The criterion is any SQL expression object applicable to the
    WHERE clause of a select.   
String expressions are coerced into SQL expression constructs via the :func:`.text` construct.（字符串表达式通过：func：`。text`结构强制转换为SQL表达式构造。）
    """
    for criterion in list(criterion):
        criterion = expression._expression_literal_as_text(criterion)
        criterion = self._adapt_clause(criterion, True, True)
        if self._criterion is not None:
            self._criterion = self._criterion & criterion
        else:
            self._criterion = criterion
def _expression_literal_as_text(element):
    return _literal_as_text(element, warn=True)


def _literal_as_text(element, warn=False):
    if isinstance(element, Visitable):
        return element
    elif hasattr(element, '__clause_element__'):
        return element.__clause_element__()
    elif isinstance(element, util.string_types):
        if warn:
            util.warn_limited(
                "Textual SQL expression %(expr)r should be "
                "explicitly declared as text(%(expr)r)",
                {"expr": util.ellipses_string(element)})

        return TextClause(util.text_type(element))
    elif isinstance(element, (util.NoneType, bool)):
        return _const_expr(element)
    else:
        raise exc.ArgumentError(
            "SQL expression object or string expected, got object of type %r "
            "instead" % type(element)
        )
```
##### text 方法就是通过sqlalchemy.sql.elements.TextClause#_create_text构造的，这里殊途同归了。总结就是:不使用text(str)也是可以的，就是会报个warning。



---
### 2018-7-24号 遇到的问题--已解决
https://stackoverflow.com/questions/28047027/sqlalchemy-not-find-table-for-creating-foreign-key
https://segmentfault.com/q/1010000003983231/revision
https://segmentfault.com/q/1010000002361279
```python
sqlalchemy.exc.NoReferencedTableError: Foreign key associated with column 'Address.fk_province_code' could not find table 'Geo_Code' with which to generate a foreign key to target column 'ad_code'
sqlalchemy.exc.NoReferencedTableError：与列'Address.fk_province_code'关联的外键无法找到用于生成目标列'ad_code'的外键的表'Geo_Code'

```

```python
python manage.py db init
python manage.py db migrate
python mmanage.py shell
db.create_all()
```

##### 再执行上述命令前 要把所有可能报错的model中的表文件导入到 manage.py中，显式的告诉migrate时需要创建哪些表，隐式依赖的表不这样做就会报错。

```python
relationship是为了简化联合查询join等，创建的两个表之间的虚拟关系，这种关系与标的结构时无关的。他与外键十分相似，确实，他必须在外键的基础上才允许使用

不然会报错：

sqlalchemy.exc.NoForeignKeysError: Could not determine join condition between parent/child tables on relationship Father.son - there are no foreign keys linking these tables.  Ensure that referencing columns are associated with a ForeignKey or ForeignKeyConstraint, or specify a 'primaryjoin' expression

详细的relationship可以点击这里进行查看

relationship的使用：

使两个表之间产生管理，类似于合成一张表，可以直接取出关联的表，进行获取数据，而不需要join操作
```
---

```python

    #简单查询
    print(session.query(User).all())
    print(session.query(User.name, User.fullname).all())
    print(session.query(User, User.name).all())
    
    #带条件查询
    print(session.query(User).filter_by(name='user1').all())
    print(session.query(User).filter(User.name == "user").all())
    print(session.query(User).filter(User.name.like("user%")).all())
    
    #多条件查询
    print(session.query(User).filter(and_(User.name.like("user%"), User.fullname.like("first%"))).all())
    print(session.query(User).filter(or_(User.name.like("user%"), User.password != None)).all())
    
    #sql过滤
    print(session.query(User).filter("id>:id").params(id=1).all())
    
    #关联查询 
    print(session.query(User, Address).filter(User.id == Address.user_id).all())
    print(session.query(User).join(User.addresses).all())
    print(session.query(User).outerjoin(User.addresses).all())
    
    #聚合查询
    print(session.query(User.name, func.count('*').label("user_count")).group_by(User.name).all())
    print(session.query(User.name, func.sum(User.id).label("user_id_sum")).group_by(User.name).all())
    
    #子查询
    stmt = session.query(Address.user_id, func.count('*').label("address_count")).group_by(Address.user_id).subquery()
    print(session.query(User, stmt.c.address_count).outerjoin((stmt, User.id == stmt.c.user_id)).order_by(User.id).all())
    
    #exists
    print(session.query(User).filter(exists().where(Address.user_id == User.id)))
    print(session.query(User).filter(User.addresses.any()))
    
    #限制返回字段查询
    person = session.query(Person.name, Person.created_at,                     
             Person.updated_at).filter_by(name="zhongwei").order_by(            
             Person.created_at).first()
             
    #记录总数查询的几种姿势

    from sqlalchemy import func
     
    # count User records, without
    # using a subquery.
    session.query(func.count(User.id))
     
    # return count of user "id" grouped
    # by "name"
    session.query(func.count(User.id)).\
            group_by(User.name)
     
    from sqlalchemy import distinct
     
    # count distinct "name" values
    session.query(func.count(distinct(User.name)))
```    