# 呵呵
{
新人最重要的品质应该就是“好学”
中坚最重要的品质应该是“努力”
“忠心”, 就算是稳定团队也是一种巨大的财富。高层骨干的变动对公司来说是伤筋动骨的。

新人(1-2年)
中坚(2-5年)
骨干(>5年)
}


# 项目优化mongo步骤
{

1. 列出原始日志表与统计表；
2. 列出每个表的查询条件；
3. 列出每个表的索引；
4. 列出查询慢的语句；

优化建议:

如果nscanned(扫描的记录数)远大于nreturned(返回结果的记录数)的话, 那么需要使用索引。
如果 reslen 返回字节非常大, 那么考虑只获取所需的字段。
执行 update 操作时同样检查一下 nscanned, 并使用索引减少文档扫描数量。
使用 db.eval() 在服务端执行某些统计操作。
减少返回文档数量, 使用 skip & limit 分页。

对于创建索引的建议是; 如果很少读, 那么尽量不要添加索引, 因为索引越多, 写操作会越慢。如果读量很大, 那么创建索引还是比较划算的。

也可以通过客户端db.setProfilingLevel(级别) 命令来实时配置。可以通过db.getProfilingLevel()命令来获取当前的Profile级别。



level有三种级别

0 – 不开启
1 – 记录慢命令 (默认为>100ms)
2 – 记录所有命令

参数为1的时候, 默认的慢命令是大于100ms, 当然也可以进行设置
db.setProfilingLevel( level , slowms ) 
db.setProfilingLevel( 1 , 120 );

Mongodb Profile 记录是直接存在系统db里的, 记录位置 system.profile , 我们只要查询这个Collection的记录就可以获取到我们的 Profile 记录了。
执行查询, 然后执行profile
> db.users.find({"name":"wolfy"+66666})
{ "_id" : ObjectId("5752486fc74b6bdc94876d95"), "name" : "wolfy66666", "age" : 13471 }
> db.system.profile.find()

通过执行db.system.profile.find({millis:{$gt:500}})能够返回查询时间在500毫秒以上的查询命令。

这里值的含义是

ts; 命令执行时间
info; 命令的内容
query; 代表查询
order.order;  代表查询的库与集合
reslen; 返回的结果集大小, byte数
nscanned; 扫描记录数量
nquery; 后面是查询条件
nreturned; 返回记录数及用时
millis; 所花时间

如果发现时间比较长, 那么就需要作优化。
比如nscanned数很大, 或者接近记录总数, 那么可能没有用到索引查询。
reslen很大, 有可能返回没必要的字段。
nreturned很大, 那么有可能查询的时候没有加限制。
mongo可以通过db.serverStatus()查看mongod的运行状态

}

# mysql常用
{

# 查看表结构
desc et_pages;
# 查看建表语句
show create table et_pages;
# 查看数据库缓存配置
show variables like 'have_query_cache';
show status like '%qcache_cache%';

1 查看系统支持的存储引擎
show engines;

2 查看表使用的存储引擎
两种方法; 
a、show table status from db_name where name='table_name';
b、show create table table_name;

3 修改表引擎方法
alter table table_name engine=innodb;


}

# Python:Celery 分布式异步消息任务队列
{

Celery的架构由三部分组成, 消息中间件（message broker）, 任务执行单元（worker）和任务执行结果存储（task result store）组成。
https://www.cnblogs.com/forward-wang/p/5970806.html
https://www.cnblogs.com/lianzhilei/p/7133295.html
http://python.jobbole.com/87086/?utm_source=blog.jobbole.com&utm_medium=relatedPosts
http://dormousehole.readthedocs.io/en/latest/patterns/celery.html#id2

# -*- coding:utf-8 -*-
# celery_test.py

from celery import Celery
import time

# 任意  中间件  数据存储
app = Celery('cly', broker='redis://:12345@192.168.40.190:12345/0',backend='redis://:12345@192.168.40.190:12345')
@app.task
def add(x,y):
    time.sleep(3)
    print("running...",x,y)
    return x+y

#代码做了几件事; 
创建了一个 Celery 实例 app, 名称为 my_task；
指定broker消息中间件用 redis
指定backend存储用 redis
创建了一个 Celery 任务 add, 当函数被 @app.task 装饰后, 就成为可被 Celery 调度的任务

# shell
cat redis_server_test.cnf 
daemonize yes
port 12345
requirepass 12345

redis-server  redis_server_test.cnf 
redis-cli -p 12345 -a 12345
celery -A celery_test worker --loglevel=info

>>> from celery_test import add
>>> add.delay(1,2)

>>> result = add.delay(2, 6)
>>> result.ready()   # 使用 ready() 判断任务是否执行完毕
False
>>> result.ready()
False
>>> result.ready()
True
>>> result.get()     # 使用 get() 获取任务结果
8

BROKER_URL = 'redis://localhost:6379/0'
URL的格式为; 
redis://:password@hostname:port/db_number
URL Scheme 后的所有字段都是可选的, 并且默认为 localhost 的 6379 端口, 使用数据库 0。我的配置是; 
redis://:password@ubuntu:6379/5



为了测试Celery能否工作编写 celery_test.py并运行,再在当前目录下运行如下命令:
celery -A celery_test worker --loglevel=info
查询文档, 了解到该命令中-A参数表示的是Celery APP的名称, 这个实例中指的就是tasks.py,后面的tasks就是APP的名称, 
worker是一个执行任务角色, 后面的loglevel=info记录日志类型默认是info,这个命令启动了一个worker,用来执行程序中add这个加法任务（task）。



style="background-color: #FFEFD5"

}

# 系统性能优化
{
1、大量读多少量写是主从还是缓存？数据量少的话，尽量使用缓存
2、依赖非常多的外部RPC服务时--换成异步调用/3、
3、配置线程池
4、DB查询性能优化
5、系统中陈旧的框架
}


使用Charles设置代理，将一个远程服务器地址代理到本地服务进行调试
使用Postman模拟当时生产环境的请求（从Charles中 copy header、query 之类的数据）


# 前端
{
jquery：使用选择器（$）选取DOM对象，对其进行赋值、取值、事件绑定等操作，其实和原生的HTML的区别只在于可以更方便的选取和操作DOM对象，而数据和界面是在一起的。
vue：通过Vue对象将数据和View完全分离开来了。对数据进行操作不再需要引用相应的DOM对象，可以说数据和View是分离的，他们通过Vue对象这个vm实现相互的绑定。这就是传说中的MVVM。
与jq不同 mvvm框架基本不操作dom节点， 双向绑定使 dom节点跟变量绑定后， 通过修改变量的值控制dom节点的各类属性。所以其实现思路为： 视图层使用一变量控制dom节点显示与否，点击按钮则改变该变量。

vue适用的场景：复杂数据操作的后台页面，表单填写页面
jquery适用的场景：比如说一些html5的动画页面，一些需要js来操作页面样式的页面
然而二者也是可以结合起来一起使用的，vue侧重数据绑定，jquery侧重样式操作，动画效果等，则会更加高效率的完成业务需求

vue使用者的思路转变：界面不是被你的事件改变的，事件只需要改变数据，界面是数据的实时反馈。




/*
    $(window).bind('beforeunload',function(){
        a1=$("#post_public_button").attr();
        alert(a1)
        a2=$("#put_keyword_button").attr();
        alert(a1)
        return '真的确定离开当前页面吗?';
      }
    );
    
    window.onbeforeunload=function(e){
      var e=window.event||e;
      e.returnValue=("确定离开当前页面吗？");
    }
*/
    #带条件的判断是否提示退出
    window.onbeforeunload = function() 
    { 
        var public_id_list = document.getElementById("public_id_list").value
        var textareaid = document.getElementById("textareaid").value
        if(textareaid != "" || public_id_list != ""){ 
            return "您确定要退出页面吗？"; 
        }
    } 

#前端跳转总结
我们可以利用http的重定向来跳转

window.location.replace("http://www.jb51.net");
使用href来跳转
window.location.href = "http://www.jb51.net";
使用jQuery的属性替换方法
$(location).attr('href', 'http://www.jb51.net');
$(window).attr('location','http://www.jb51.net');
$(location).prop('href', 'http://www.jb51.net')


$.all('*',function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    res.header("Access-Control-Allow-Methods","PUT,POST,GET,DELETE,OPTIONS");
    next();
});
//在客户端对ajax进行设定
$.ajaxSettings.crossDomain = true;

JSON.stringify() 方法用于将一个json值转为字符串；
JSON.parse() 方法用于将json字符串转化成对象；
}

# tronado结束访问的两种情况
{

为什么 Tornado 在调用 self.finish() 以后不终止 RequestHandler 中相关处理函数的运行？
self.finish()代表回应生成的终结，并不代表着请求处理逻辑的终结。假设你有一个block的逻辑是和回应无关的，那么放在self.finish()的后面可以显著的缩短响应时间。所以，如果你确定自己的逻辑需要立即返回，可以在self.finish()后立刻return。Tornado在将这个自由留给了你自己。另外一个理由是，在call stack里让顶端的函数去弹出一个非顶端的函数，这个逻辑有点奇怪。唯一能够提供退出的机制就是异常了。但是在正常逻辑里面使用异常去实现一个功能，也是很怪的逻辑
同理还有self.render/self.write 
我们在所有这种response语句前加return 例如 return self.redirect('/')
作者：安江泽
链接：https://www.zhihu.com/question/19787492/answer/12971863
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


# http://demo.pythoner.com/itt2zh/ch5.html
记住当你使用@tornado.web.asynchonous装饰器时，Tornado永远不会自己关闭连接。你必须在你的RequestHandler对象中调用finish方法来显式地告诉Tornado关闭连接。（否则，请求将可能挂起，浏览器可能不会显示我们已经发送给客户端的数据。）在前面的异步示例中，我们在on_response函数的write后面调用了finish方法

tornado.web.asynchronous
其中 tornado.web.asynchronous 装饰器很简单，就是设置 self._auto_finish = False，这样当 AsyncHandler.get() 执行完之后，connection socket 不会被 close，需要主动调用 self.finish()。在保持连接不关闭的情况下，把控制权让出去，等数据就绪之后再切回来，使异步实现成为可能。 下面是 asynchronous 简化后的代码：

# 代码二：
def asynchronous(method):
   @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.application._wsgi:
            raise Exception("@asynchronous is not supported for WSGI apps")
        self._auto_finish = False
        return method(self, *args, **kwargs)
    return wrapper

作者：OMSobliga
链接：https://www.jianshu.com/p/8769093242f3
來源：简书
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。
}

# mongodb redhat安装参考
{
https://www.cnblogs.com/kevingrace/p/7565215.html

1）在/etc/yum.repos.d 创建一个mongodb-org.repo 源文件
[root@qd-vpc-dev-op01 ~]$ cd /etc/yum.repos.d/
[root@qd-vpc-dev-op01 yum.repos.d]$ touch mongodb-org.repo
[root@qd-vpc-dev-op01 yum.repos.d]$ cat mongodb-org.repo
[mongodb-org]
name=MongoDB Repository
baseurl=http://mirrors.aliyun.com/mongodb/yum/redhat/6/mongodb-org/3.2/x86_64/
gpgcheck=0
enabled=1
 
2）更新yum源
[root@qd-vpc-dev-op01 yum.repos.d]$ yum update
 
3) 安装MongoDB
[root@qd-vpc-dev-op01 yum.repos.d]$ yum install -y mongodb-org
 
4）启动MongoDB
[root@qd-vpc-dev-op01 yum.repos.d]$ service mongod start
[root@qd-vpc-dev-op01 yum.repos.d]$ chkconfig mongod on
 
5）配置远程访问
[root@qd-vpc-dev-op01 yum.repos.d]$cat /etc/mongod.conf|grep -v "#"|grep -v "^$"
systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log
storage:
  dbPath: /var/lib/mongo
  journal:
    enabled: true
processManagement:
net:
  port: 27017
 
[root@qd-vpc-dev-op01 yum.repos.d]$ service mongod restart
Restarting mongod (via systemctl):                         [  OK  ]
 
6）打开MongoDB
[root@qd-vpc-dev-op01 yum.repos.d]$ mongo 127.0.0.1:27017

}

# history
{
#显示时间戳
export HISTTIMEFORMAT='%F %T '
#搜索历史
Ctrl+R 


vi ~/.bash_profile
HISTSIZE=5000
HISTFILESIZE=5000

export HISTTIMEFORMAT='%F %T '
export HISTCONTROL=ignoredups
export HISTCONTROL=erasedups
export HISTCONTROL=ignorespace





export HISTCONTROL=ignoredups # 使用HISTCONTROL来消除命令历史中的连续重复条目 
export HISTCONTROL=erasedups # 使用HISTCONTROL在整个历史中去除重复命令 
export HISTCONTROL=ignorespace # 使用HISTCONTROL强制history忽略某条特定命令(这里是空格) 
export HISTIGNORE=“pwd:ls:” # 存储历史命令时忽略特殊命令，这里的话pwd,ls就不会存储了 
export HISTTIMEFORMAT='%F %T ' # 使用HISTTIMEFORMAT在历史中显示TIMESTAMP

# 单用户的登陆启动配置, ls加上了颜色
scrapyer@crawltest004:~$ cat /home/scrapyer/.bash_profile 
STSIZE=5000
HISTFILESIZE=5000
alias ls='ls --color=tty'
alias ll='ls -l'
export HISTTIMEFORMAT='%F %T '
export HISTCONTROL=ignoredups
export HISTCONTROL=erasedups
export HISTCONTROL=ignorespace 
}

# 长连接
{
#ajax实现长连接

 <%@ page language="java" import="java.util.*" pageEncoding="UTF-8" isELIgnored="false" %>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
    <head>
        <meta http-equiv="pragma" content="no-cache">
        <meta http-equiv="cache-control" content="no-cache">
        <meta http-equiv="expires" content="0">
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <%@ include file="/tags/jquery-lib.jsp"%>
        
        <script type="text/javascript">
            $(function () {
            
                (function longPolling() {
                
                    $.ajax({
                        url: "${pageContext.request.contextPath}/communication/user/ajax.mvc",
                        data: {"timed": new Date().getTime()},
                        dataType: "text",
                        timeout: 5000,
                        error: function (XMLHttpRequest, textStatus, errorThrown) {
                            $("#state").append("[state: " + textStatus + ", error: " + errorThrown + " ]<br/>");
                            if (textStatus == "timeout") { // 请求超时
                                    longPolling(); // 递归调用
                                
                                // 其他错误，如网络错误等
                                } else { 
                                    longPolling();
                                }
                            },
                        success: function (data, textStatus) {
                            $("#state").append("[state: " + textStatus + ", data: { " + data + "} ]<br/>");
                            
                            if (textStatus == "success") { // 请求成功
                                longPolling();
                            }
                        }
                    });
                })();
                
            });
        </script>
    </head>
    
    <body>
    
websocket
Connection: Keep-alive，但不能说是长连接
TCP的keep alive是检查当前TCP连接是否活着；HTTP的Keep-alive是要让一个TCP连接活久点。它们是不同层次的概念。

#HTTP协议的头部字段总结:

1、 Accept: 告诉WEB服务器自己接受什么介质类型，*/* 表示任何类型，type/* 表示该类型下的所有子类型，type/sub-type。
2、 Accept-Charset:  浏览器申明自己接收的字符集 
Accept-Encoding:  浏览器申明自己接收的编码方法，通常指定压缩方法，是否支持压缩，支持什么压缩方法（gzip，deflate） 
Accept-Language: 浏览器申明自己接收的语言 
语言跟字符集的区别: 中文是语言，中文有多种字符集，比如big5，gb2312，gbk等等。
3、 Accept-Ranges: WEB服务器表明自己是否接受获取其某个实体的一部分（比如文件的一部分）的请求。bytes: 表示接受，none: 表示不接受。
4、 Age: 当代理服务器用自己缓存的实体去响应请求时，用该头部表明该实体从产生到现在经过多长时间了。
5、 Authorization: 当客户端接收到来自WEB服务器的 WWW-Authenticate 响应时，用该头部来回应自己的身份验证信息给WEB服务器。
6、 Cache-Control: 请求: no-cache（不要缓存的实体，要求现在从WEB服务器去取） 
max-age: （只接受 Age 值小于 max-age 值，并且没有过期的对象） 
max-stale: （可以接受过去的对象，但是过期时间必须小于 max-stale 值） 
min-fresh: （接受其新鲜生命期大于其当前 Age 跟 min-fresh 值之和的缓存对象） 
响应: public(可以用 Cached 内容回应任何用户) 
private（只能用缓存内容回应先前请求该内容的那个用户） 
no-cache（可以缓存，但是只有在跟WEB服务器验证了其有效后，才能返回给客户端） 
max-age: （本响应包含的对象的过期时间） 
ALL: no-store（不允许缓存）
7、 Connection: 请求: close（告诉WEB服务器或者代理服务器，在完成本次请求的响应后，断开连接，不要等待本次连接的后续请求了）。 
keepalive（告诉WEB服务器或者代理服务器，在完成本次请求的响应后，保持连接，等待本次连接的后续请求）。 
响应: close（连接已经关闭）。 
keepalive（连接保持着，在等待本次连接的后续请求）。 
Keep-Alive: 如果浏览器请求保持连接，则该头部表明希望 WEB 服务器保持连接多长时间（秒）。例如: Keep-Alive: 300
8、 Content-Encoding: WEB服务器表明自己使用了什么压缩方法（gzip，deflate）压缩响应中的对象。例如: Content-Encoding: gzip
9、Content-Language: WEB 服务器告诉浏览器自己响应的对象的语言。
10、Content-Length:  WEB 服务器告诉浏览器自己响应的对象的长度。例如: Content-Length: 26012
11、Content-Range:  WEB 服务器表明该响应包含的部分对象为整个对象的哪个部分。例如: Content-Range: bytes 21010-47021/47022
12、Content-Type:  WEB 服务器告诉浏览器自己响应的对象的类型。例如: Content-Type: application/xml
13、ETag: 就是一个对象（比如URL）的标志值，就一个对象而言，比如一个 html 文件，如果被修改了，其 Etag 也会别修改，所以ETag 的作用跟 Last-Modified 的作用差不多，主要供 WEB 服务器判断一个对象是否改变了。比如前一次请求某个 html 文件时，获得了其 ETag，当这次又请求这个文件时，浏览器就会把先前获得的 ETag 值发送给WEB 服务器，然后 WEB 服务器会把这个 ETag 跟该文件的当前 ETag 进行对比，然后就知道这个文件有没有改变了。
14、 Expired: WEB服务器表明该实体将在什么时候过期，对于过期了的对象，只有在跟WEB服务器验证了其有效性后，才能用来响应客户请求。是 HTTP/1.0 的头部。例如: Expires: Sat, 23 May 2009 10:02:12 GMT
15、 Host: 客户端指定自己想访问的WEB服务器的域名/IP 地址和端口号。例如: Host: rss.sina.com.cn
16、 If-Match: 如果对象的 ETag 没有改变，其实也就意味著对象没有改变，才执行请求的动作。
17、 If-None-Match: 如果对象的 ETag 改变了，其实也就意味著对象也改变了，才执行请求的动作。
18、 If-Modified-Since: 如果请求的对象在该头部指定的时间之后修改了，才执行请求的动作（比如返回对象），否则返回代码304，告诉浏览器该对象没有修改。例如: If-Modified-Since: Thu, 10 Apr 2008 09:14:42 GMT
19、 If-Unmodified-Since: 如果请求的对象在该头部指定的时间之后没修改过，才执行请求的动作（比如返回对象）。
20、 If-Range: 浏览器告诉 WEB 服务器，如果我请求的对象没有改变，就把我缺少的部分给我，如果对象改变了，就把整个对象给我。浏览器通过发送请求对象的 ETag 或者 自己所知道的最后修改时间给 WEB 服务器，让其判断对象是否改变了。总是跟 Range 头部一起使用。
21、 Last-Modified: WEB 服务器认为对象的最后修改时间，比如文件的最后修改时间，动态页面的最后产生时间等等。例如: Last-Modified: Tue, 06 May 2008 02:42:43 GMT
22、 Location: WEB 服务器告诉浏览器，试图访问的对象已经被移到别的位置了，到该头部指定的位置去取。例如: Location: http://i0.sinaimg.cn/dy/deco/2008/0528/sinahome_0803_ws_005_text_0.gif
23、 Pramga: 主要使用 Pramga: no-cache，相当于 Cache-Control:  no-cache。例如: Pragma: no-cache
24、 Proxy-Authenticate:  代理服务器响应浏览器，要求其提供代理身份验证信息。Proxy-Authorization: 浏览器响应代理服务器的身份验证请求，提供自己的身份信息。
25、 Range: 浏览器（比如 Flashget 多线程下载时）告诉 WEB 服务器自己想取对象的哪部分。例如: Range: bytes=1173546-
26、 Referer: 浏览器向 WEB 服务器表明自己是从哪个 网页/URL 获得/点击 当前请求中的网址/URL。例如: Referer: http://www.sina.com/
27、 Server: WEB 服务器表明自己是什么软件及版本等信息。例如: Server: Apache/2.0.61 (Unix)
28、 User-Agent: 浏览器表明自己的身份（是哪种浏览器）。例如: User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 Firefox/2、0、0、14
29、 Transfer-Encoding: WEB 服务器表明自己对本响应消息体（不是消息体里面的对象）作了怎样的编码，比如是否分块（chunked）。例如: Transfer-Encoding: chunked
30、 Vary: WEB服务器用该头部的内容告诉 Cache 服务器，在什么条件下才能用本响应所返回的对象响应后续的请求。假如源WEB服务器在接到第一个请求消息时，其响应消息的头部为: Content-Encoding: gzip; Vary: Content-Encoding那么 Cache 服务器会分析后续请求消息的头部，检查其 Accept-Encoding，是否跟先前响应的 Vary 头部值一致，即是否使用相同的内容编码方法，这样就可以防止 Cache 服务器用自己 Cache 里面压缩后的实体响应给不具备解压能力的浏览器。例如: Vary: Accept-Encoding
31、 Via:  列出从客户端到 OCS 或者相反方向的响应经过了哪些代理服务器，他们用什么协议（和版本）发送的请求。当客户端请求到达第一个代理服务器时，该服务器会在自己发出的请求里面添加 Via 头部，并填上自己的相关信息，当下一个代理服务器收到第一个代理服务器的请求时，会在自己发出的请求里面复制前一个代理服务器的请求的Via 头部，并把自己的相关信息加到后面，以此类推，当 OCS 收到最后一个代理服务器的请求时，检查 Via 头部，就知道该请求所经过的路由。例如: Via: 1.0 236.D0707195.sina.com.cn:80 (squid/2.6.STABLE13)


# HTTP 请求消息头部实例:  
Host: rss.sina.com.cn 
User-Agent: Mozilla/5、0 (Windows; U; Windows NT 5、1; zh-CN; rv:1、8、1、14) Gecko/20080404 Firefox/2、0、0、14 
Accept: text/xml,application/xml,application/xhtml+xml,text/html;q=0、9,text/plain;q=0、8,image/png,*/*;q=0、5 
Accept-Language: zh-cn,zh;q=0、5 
Accept-Encoding: gzip,deflate 
Accept-Charset: gb2312,utf-8;q=0、7,*;q=0、7 
Keep-Alive: 300 
Connection: keep-alive 
Cookie: userId=C5bYpXrimdmsiQmsBPnE1Vn8ZQmdWSm3WRlEB3vRwTnRtW &lt;-- Cookie 
If-Modified-Since: Sun, 01 Jun 2008 12:05:30 GMT 
Cache-Control: max-age=0 
HTTP 响应消息头部实例:  
Status: OK - 200 &lt;-- 响应状态码，表示 web 服务器处理的结果。 
Date: Sun, 01 Jun 2008 12:35:47 GMT 
Server: Apache/2、0、61 (Unix) 
Last-Modified: Sun, 01 Jun 2008 12:35:30 GMT 
Accept-Ranges: bytes 
Content-Length: 18616 
Cache-Control: max-age=120 
Expires: Sun, 01 Jun 2008 12:37:47 GMT 
Content-Type: application/xml 
Age: 2 
X-Cache: HIT from 236-41、D07071951、sina、com、cn &lt;-- 反向代理服务器使用的 HTTP 头部 
Via: 1.0 236-41.D07071951.sina.com.cn:80 (squid/2.6.STABLE13) 
Connection: close    
    
    
# tornado长连接断开的处理机制
使用tornado的异步http调用时候，在继续RequestHandler的子类中，可以重载on_connection_close方法。

此方法在对端连接关闭，或者在socket上读写错误的时候被调用，可以让服务器做一些清理。


参考博客
http://tornado-zh.readthedocs.io/zh/latest/websocket.html?highlight=WebSocketHandler    # tornado.websocket — 浏览器与服务器双向通信
http://www.cnblogs.com/shijingjing07/p/6558217.html # tornado长轮询
https://www.cnblogs.com/x54256/p/8253002.html       # 模拟tornado两个socket请求
http://www.cnblogs.com/huazi/archive/2012/11/25/2787290.html    # tornado的长轮询聊天室例子分析
https://www.cnblogs.com/Finley/p/5517769.html   # Tornado长轮询和WebSocket

}


# jira 语法
{

h1. 标题一
h2. 标题二
h3. 标题三
h4. 标题四
h5. 标题五
h6. 标题六

# 有序列表一
# 有序列表二
## 有序列表缩进一次
### 有序列表缩进二次
## 有序列表缩进一次
# 有序列表三

* 无序列表一
* 无序列表二
** 无序列表缩进一次
*** 无序列表缩进二次
** 无序列表缩进一次
* 无序列表三


{code:java}
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello world!");
    }
}
{code}


*黑体*
_斜体_
-删除线-
+下划线+
下标 ~sub~
上标 ^sup^

!http://upload-images.jianshu.io/upload_images/245520-8d44d5e7c54148da.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240!


}




# 未整理
{
mongod --dbpath D:\mongodb\mongodbdata
mongo --port 27017 -u name -p password --authenticationDatabase admin

account_id=$.trim(account_id)   #jquery 去除字符串两边的空格

function tourl(thiss){
    window.open($(thiss).attr('href'),'_blank');
}

# 为网页某处增加组件
$(document).ready(function(){        
    var obj1 = document.getElementById("hehe1");  
    obj1.insertAdjacentHTML("afterBegin",'发文数 :  <input id="txt1" size="4" style="size:4;float:right;margin : 0px 10px 0px 0px;">'); 
    }

}










