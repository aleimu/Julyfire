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

### sqlalchemy查询使用
#### 1.带条件查询

查询是最常用的，对于各种查询我们必须要十分清楚，首先是带条件的查询

```python
#带条件查询
rows = session.query(User).filter_by(username='jingqi').all()
print(rows)
rows1 = session.query(User).filter(User.username=='jingqi').all()
print(rows1)
rows2 = session.query(User.username).filter(User.username=='jingqi').all()
print(rows2)
rows3 = session.query(User.username).filter(User.username=='jingqi')
print(rows3)
```
**`filter_by`和`filter`都是过滤条件，只是用法有区别`filter_by`里面不能用`!= `还有`> <` 等等，所有`filter`用得更多,`filter_by`只能用`=`。**

前两个查询的是`User`,所以返回结果也是一个对象，但是`rows2`查询的是属性值，所以返回的是属性值。

`rows3`可以看到`SQLAlchemy `转成的`SQL`语句，`SQLAlchemy`最后都是会转成`SQL`语句，通过这个方法可以查看原生`SQL`,甚至有些时候我们需要把`SQLAlchemy`转成的`SQL`交给DBA审查，合适的才能使用。

查询要知道查询结果的返回怎样的数据
```python
print( session.query(User).filter(User.username=='jingqi').all() )
print( session.query(User).filter(User.username=='jingqi').first())
print( session.query(User).filter(User.username=='jingqi').one())#结果为一个时正常，多了就报错
print( session.query(User).get(2))#通过id查询
```
上面三条记录，第一个查出所有符合条件的记录，第二个查出所有符合记录的第一条记录，第三个返回一个对象，如果结果有多条就会报错，第四个通过主键获取记录

---
#### 2.限制返回的结果数量

```python
#限制查询返回结果
print( session.query(User).filter(User.username!='jingqi').limit(2).all())
print( session.query(User).filter(User.username!='jingqi').offset(2).all())
print( session.query(User).filter(User.username!='jingqi').slice(2,3).all())
#可以排序之后再进行限制
from sqlalchemy import desc
print( session.query(User).filter(User.username!='budong').order_by(User.username).all())
print( session.query(User).filter(User.username!='budong').order_by(desc(User.username)).slice(1,3).all())

```
第一个是限制返回条数，从第一条开始；第二个是从第三条开始返回查询结果；第三个是切片返回记录。

**`order_by`默认是顺序，`desc`是降序。**

---

#### 3.带条件查询

```python
#不等于
print( session.query(User).filter(User.username!='jingqi').all() )
#模糊匹配 like
print( session.query(User).filter(User.username.like('jingqi')).all() )
print( session.query(User).filter(User.username.notlike('jingqi')).all() )
#成员属于  in_
print( session.query(User).filter(User.username.in_(['jingqi','jingqi1'])).all() )
#成员不属于  notin_
print( session.query(User).filter(User.username.notin_(['jingqi','jingqi2'])).all() )
#空判断
print( session.query(User).filter(User.username==None).all() )
print( session.query(User).filter(User.username.is_(None)).all() )
print( session.query(User).filter(User.username.isnot(None)).all() )
#多条件
print( session.query(User).filter(User.username.isnot(None),User.password=='qwe123').all() )
#选择条件
from sqlalchemy import or_,and_,all_,any_
print( session.query(User).filter(or_(User.username=='jingqi',User.password=='qwe123')).all() )
print( session.query(User).filter(and_(User.username=='jingqi2',User.password=='111')).all() )

以上是各种带条件的查询，大家知道怎么使用，但是需要注意的是，所以的模糊匹配是十分耗费时间的，能不用就尽量不要用。
```
---
#### 4.聚合函数的使用

``` python
from sqlalchemy import func,extract
print( session.query(User.password,func.count(User.id)).group_by(User.password).all() )
print( session.query(User.password,func.count(User.id)).group_by(User.password).having(func.count(User.id)>1).all() )
print( session.query(User.password,func.sum(User.id)).group_by(User.password).all() )
print( session.query(User.password,func.max(User.id)).group_by(User.password).all() )
print( session.query(User.password,func.min(User.id)).group_by(User.password).all() )
#使用extract提取时间中的分钟或者天来分组
print( session.query(extract('minute', User.creatime).label('minute'),func.count('*').label('count')).group_by('minute').all() )
print( session.query(extract('day', User.creatime).label('day'),func.count('*').label('count')).group_by('day').all() )
```
这里只是告诉大家的用法，其中`group_by`是分组，如果要使用聚合函数，就必须导入`func`,`label`是取别名的意思 。

---
#### 5.表关系查询

对于有表关系的，也有些不同的查询，首先我们来建立一个有外键关系的表

```python
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class UserDetails(Base):
    __tablename__ = 'user_details'
    id = Column(Integer,primary_key=True,autoincrement=True)
    id_card = Column(Integer,nullable=False,unique=True)
    lost_login = Column(DateTime)
    login_num = Column(Integer,default=0)
    user_id = Column(Integer,ForeignKey('user.id'))

    userdetail_for_foreignkey = relationship('User',backref='details',uselist=False,cascade='all')

    def __repr__(self):
        return '<UserDetails(id=%s,id_card=%s,lost_login=%s,login_num=%s,user_id=%s)>'%(
            self.id,
            self.id_card,
            self.login_login,
            self.login_num,
            self.user_id
        )
```
这里要注意`relationship`默认是一对多的关系，使用`uselist=False`则表示一对一的关系，`cascade` 是自动关系处理，就和MySQL中的`ON DELETE`类似，但是有区别，参数选项如下：

`cascade` 所有的可选字符串项是:
- *all* , 所有操作都会自动处理到关联对象上.
- *save-update* , 关联对象自动添加到会话.
- *delete* , 关联对象自动从会话中删除.
- *delete-orphan* , 属性中去掉关联对象, 则会话中会自动删除关联对象.
- *merge* , `session.merge()` 时会处理关联对象.
- *refresh-expire* , `session.expire()` 时会处理关联对象.
- *expunge* , `session.expunge()` 时会处理关联对象.

有如上的表关系之后，查询可以十分方便

```python

#表关系查询
row = session.query(UserDetails).all()
print(row,dir(row[0]))
row = session.query(User).filter(User.id==1).first()
print(row,dir(row))
print(row.details)
print(row.details[0].lost_login)
```

**`relationship`会在`User`表里面添加一个属性，通过这个属性就可以查询对应的`user_details`表中的所有字段。省去了很多的代码。**

---
#### 6.多表查询

多表查询也是必须要掌握的知识点。以下是常见的几种表关联方式，需要熟练掌握。

```python
#多表查询
print( session.query(UserDetails,User).all() )  #这个是 cross join
print( session.query(UserDetails,User).filter(User.id==UserDetails.id).all() )  #这是也是cross join 但是加上了where条件

print( session.query(User.username,UserDetails.lost_login).join(UserDetails,UserDetails.id==User.id).all() )  #这个是inner join

print( session.query(User.username,UserDetails.lost_login).outerjoin(UserDetails,UserDetails.id==User.id).all() )  #这个才是左连接，sqlalchemy没有右连接

q1 = session.query(User.id)
q2 = session.query(UserDetails.id)
print(q1.union(q2).all())  #这个是union关联
```
#### 7.子表查询
```python
from sqlalchemy import all_,any_
sql_0 = session.query(UserDetails.lost_login).subquery()  #这是声明一个子表
print( session.query(User).filter((User.creatime > all_(sql_0)) ).all()  )
print( session.query(User).filter((User.creatime > any_(sql_0)) ).all()  )
```
注意`any_`和`all_`的区别，`all_`要求的是所有都满足，`any_`只需要有满足的就行。

---
#### 8.原生SQL的查询以及其他使用
再次强调，使用`ORM`或者原生`SQL`没有绝对那个好一点，怎么方便怎么使用。

```python
#第一步写好原生的sql，如果需要传递参数，可以使用字符串拼接的方式
sql_1 = """
    select * from `user`
"""
#第二步执行，得到返回的结果
row = session.execute(sql_1)
print(row,dir(row))
#第三步，自己控制得到数据的方式
print( row.fetchone() )
print( row.fetchmany() )
print( row.fetchall() )
#也可以循环获得
for i in row:
    print('===',i)
```

#### 9.分页查询

flask_sqlalchemy.BaseQuery#paginate 中提供了封装好的paginate分页函数，若只是使用SQLAlchemy则没有这个方法，可以通过属性绑定到SQLAlchemy上，参考: https://blog.csdn.net/guoqianqian5812/article/details/78860572

```python
session.query.filter(statment).order_by(session.create_time.desc()).paginate(int(page), int(per_page), False)

```



# sqlalchemy 查询的时候排除掉数据库字段为 null的

方法1： session.query(user).filter_by(user.brand_id.isnot(None))
方法2： from sqlalchemy import not_
        session.query(user).filter_by(not_(employ.user==None))
        sqlalchemy 查询数据库字段为 null的数据
方法1：
        session.query(user).filter_by(user.brand_id.is(None))
        
# 更新多条
res = db_session.query(User).filter(User.id <= 20).update({"name":"NBDragon"})
print(res) # 6 res就是我们当前这句更新语句所更新的行数
db_session.commit()


