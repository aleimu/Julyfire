
```shell
语法规则： location [=|~|~*|^~] /uri/ { … }

= 开头表示精确匹配
^~ 开头表示uri以某个常规字符串开头，理解为匹配 url路径即可。nginx不对url做编码，因此请求为/static/20%/aa，可以被规则^~ /static/ /aa匹配到（注意是空格）。
~ 开头表示区分大小写的正则匹配
~* 开头表示不区分大小写的正则匹配
!~和!~*分别为区分大小写不匹配及不区分大小写不匹配 的正则
/ 通用匹配，任何请求都会匹配到。

如果多个location匹配均匹配，按照如下的优先级来确定：
(location =) > (location 完整路径) > (location ^~ 路径) > (location ~,~* 正则顺序) > (location 部分起始路径) > (/)
```
##### 参考
- https://www.cnblogs.com/Chiler/p/8027167.html
- https://www.cnblogs.com/jackylee92/p/6836948.html
- http://outofmemory.cn/code-snippet/742/nginx-location-configuration-xiangxi-explain


```shell
# 前端资源代码截取 --错误样例
my_dev.domain.com:5009/templates/index.html
http://my_dev.domain.com:5009/templates/login.html

<a  href="#" name="../static/assets/content/userManager/driver_view.html">

http://my_dev.domain.com:5009/static/assets/content/userManager/driver_view.html

<script src="static/assets/js/data/driverview.js?rev=@@hash"></script>

http://my_dev.domain.com:5009/templates/static/assets/js/data/driverview.js?rev=@@hash&_=1533613750298  # 404       ---> 为什么会把templates加入路径？



# 前端资源代码截取  --正确样例
my_dev.domain.com:5009/templates/index.html

<a  href="#" name="../static/assets/content/car/car_view.html">

http://my_dev.domain.com:5009/static/assets/content/car/car_view.html       # 这级目录的问题

<script src="../static/assets/js/data/carview.js?rev=@@hash"></script>          # 这级路径的问题

http://my_dev.domain.com:5009/static/assets/js/data/carview.js?rev=@@hash&_=1533616165247   # 200

# Nginx配置

server {
	listen 5009 default_server;
	server_name localhost;

    location ^~ /templates/ {
		root /root/new_test_01/servers/sub_operation/backend_oper/instance/;
		index login.html;
	}
    location /v1 {
        include uwsgi_params;
        uwsgi_pass unix:/root/new_test_01/servers/sub_operation/log_test_01/log_test_01.sock;
	}
    location / {
        include uwsgi_params;
        uwsgi_pass unix:/root/new_test_01/servers/sub_operation/backend_oper/op_test_01.sock;
	}
    location ^~ /static_v1/ {
        root /root/new_test_01/servers/web_front/oper_web/;
        index login.html index.html;
        }
}


# Nginx日志

lgj@iZ282hpfj1mZ:/root/new_test_01/servers/sub_operation/backend_oper$ tailf /var/log/nginx/access.log
36.24.247.94 - - [07/Aug/2018:12:29:24 +0800] "GET /templates/static/assets/js/data/driverview.js?rev=@@hash&_=1533616150781 HTTP/1.1" 404 206 "http://my_dev.domain.com:5009/templates/index.html" "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
36.24.247.94 - - [07/Aug/2018:12:29:27 +0800] "GET /templates/index.html HTTP/1.1" 304 0 "http://my_dev.domain.com:5009/templates/login.html" "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
36.24.247.94 - - [07/Aug/2018:12:29:27 +0800] "GET /static/assets/js/data/carview.js?rev=@@hash&_=1533616165245 HTTP/1.1" 200 2847 "http://my_dev.domain.com:5009/templates/index.html" "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
36.24.247.94 - - [07/Aug/2018:12:29:27 +0800] "GET /static/assets/js/data/carview.js?rev=@@hash&_=1533616165246 HTTP/1.1" 200 2847 "http://my_dev.domain.com:5009/templates/index.html" "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"



# app 配置
app = Flask(__name__, static_folder='', static_url_path='',template_folder='templates')

前端请求js、html文件时经过app了吗？还是直接通过Nginx获得的？要是没进过app，那这里的配置是无效的，也就是说前后端分离的话，这里的配置也就没意思了吧。
查看flask的日志，也没有发现有请求静态资源的记录。

       
server {
    listen 80;
    server_name your.domain.name;
    location / {
        # 把跟路径下的请求转发给前端工具链（如gulp）打开的开发服务器
        # 如果是产品环境，则使用root等指令配置为静态文件服务器
        proxy_pass http://localhost:5000/;
    }
    
    location ~ .*\.(gif|jpg|jpeg|png|bmp|swf|js|css|ico|woff)$
        {
           root d:/nginx-1.13.6/resources;
           access_log  on;
        }

    location /api/ {
        # 把 /api 路径下的请求转发给真正的后端服务器
        proxy_pass http://localhost:8080/service/;
        # 把host头传过去，后端服务程序将收到your.domain.name, 否则收到的是localhost:8080
        proxy_set_header Host $http_host;
        # 把cookie中的path部分从/api替换成/service
        proxy_cookie_path /api /service;
        # 把cookie的path部分从localhost:8080替换成your.domain.name
        proxy_cookie_domain localhost:8080 your.domain.name         
    }

}

nginx -s reload
```

```shell
########### 每个指令必须有分号结束。#################
#user administrator administrators;  #配置用户或者组，默认为nobody nobody。
#worker_processes 2;  #允许生成的进程数，默认为1
#pid /nginx/pid/nginx.pid;   #指定nginx进程运行文件存放地址
error_log log/error.log debug;  #制定日志路径，级别。这个设置可以放入全局块，http块，server块，级别以此为：debug|info|notice|warn|error|crit|alert|emerg
events {
    accept_mutex on;   #设置网路连接序列化，防止惊群现象发生，默认为on
    multi_accept on;  #设置一个进程是否同时接受多个网络连接，默认为off
    #use epoll;      #事件驱动模型，select|poll|kqueue|epoll|resig|/dev/poll|eventport
    worker_connections  1024;    #最大连接数，默认为512
}
http {
    include       mime.types;   #文件扩展名与文件类型映射表
    default_type  application/octet-stream; #默认文件类型，默认为text/plain
    #access_log off; #取消服务日志    
    log_format myFormat '$remote_addr–$remote_user [$time_local] $request $status $body_bytes_sent $http_referer $http_user_agent $http_x_forwarded_for'; #自定义格式
    access_log log/access.log myFormat;  #combined为日志格式的默认值
    sendfile on;   #允许sendfile方式传输文件，默认为off，可以在http块，server块，location块。
    sendfile_max_chunk 100k;  #每个进程每次调用传输数量不能大于设定的值，默认为0，即不设上限。
    keepalive_timeout 65;  #连接超时时间，默认为75s，可以在http，server，location块。

    upstream mysvr {   
      server 127.0.0.1:7878;
      server 192.168.10.121:3333 backup;  #热备
    }
    error_page 404 https://www.baidu.com; #错误页
    server {
        keepalive_requests 120; #单连接请求上限次数。
        listen       4545;   #监听端口
        server_name  127.0.0.1;   #监听地址       
        location  ~*^.+$ {       #请求的url过滤，正则匹配，~为区分大小写，~*为不区分大小写。
           #root path;  #根目录
           #index vv.txt;  #设置默认页
           proxy_pass  http://mysvr;  #请求转向mysvr 定义的服务器列表
           deny 127.0.0.1;  #拒绝的ip
           allow 172.18.5.54; #允许的ip           
        } 
    }
}


文件及目录匹配，其中：
* -f和!-f用来判断是否存在文件
* -d和!-d用来判断是否存在目录
* -e和!-e用来判断是否存在文件或目录
* -x和!-x用来判断文件是否可执行

样例 ： 判断访问的图片是否存在，不存在跳转到另外的域名

   location ~* ^.+.(jpg|jpeg|gif|css|png|js|ico|thumb) {
       root    /data/wwwroot/bbs.xxx.com;
       expires 10d;
       if (!-e $request_filename) {
           rewrite ^/data/attachment/forum/(.*)$ http://img.xxx.com/forum/$1 permanent;
       }
        if (!-e $request_filename) {
           rewrite ^/item/([0-9a-z]+)/([0-9a-z]+)/(.*).html$ http://b.cutv.com/item/$1$2$3 permanent;
       }
   }

```

#### nginx配置 -- 让匹配路径不作为文件目录的一部分
```

参考 https://blog.csdn.net/u011510825/article/details/50531864

nginx指定文件路径有两种方式root和alias，ot与alias主要区别在于nginx如何解释location后面的uri，这会使两者分别以不同的方式将请求映射到服务器文件上。

[root]
语法：root path
默认值：root html
配置段：http、server、location、if

[alias]
语法：alias path
配置段：location

root实例：
location ^~ /t/ {
     root /www/root/html/;
}
如果一个请求的URI是/t/a.html时，web服务器将会返回服务器上的/www/root/html/t/a.html的文件。
alias实例：

location ^~ /t/ {

 alias /www/root/html/new_t/;
}
如果一个请求的URI是/t/a.html时，web服务器将会返回服务器上的/www/root/html/new_t/a.html的文件。注意这里是new_t，因为alias会把location后面配置的路径丢弃掉，把当前匹配到的目录指向到指定的目录。
注意：

1. 使用alias时，目录名后面一定要加"/"。
3. alias在使用正则匹配时，必须捕捉要匹配的内容并在指定的内容处使用。
4. alias只能位于location块中。（root可以不放在location中）

```
