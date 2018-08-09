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