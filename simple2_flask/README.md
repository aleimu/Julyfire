#### start server
```
chmod 660 simple_flask.sh
./simple_flask.sh
```

#### nginx config for uwsgi_config.ini
uwsgi --ini uwsgi_config.ini --daemonize /var/log/simple2flask.log
```
server {
    listen 5003 default_server;
    server_name localhost;
    location /static/ {
        root /data/;
        expires 30d;
    }
    location / {
        include uwsgi_params;
        uwsgi_pass unix:/tmp/simpleflask.sock; # 必须和uwsgi_config.ini 中的socket配置一致
        # 并且需要权限
    }
}
```

#### nginx config for uwsgi_config_other.ini

uwsgi --ini uwsgi_config_other.ini
```
server {
    listen 5004 default_server;
    server_name localhost;
    location /static/ {
        root /data/;
        expires 30d;
    }
    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:5000; # 必须和uwsgi_config_other.ini 中的socket配置一致
    }
}

```
#### SERVER_NAME 的坑
首先将hosts中配置 172.16.2.193 test.yy.com

再在config中将 SERVER_NAME = 'test.yy.com:3000'

再将manager.py:30行的manager.run()改为app.run()来进行试验

```shell
# curl http://test.yy.com:3000/pages/hello
Simple_page Say Hello World!

# curl http://127.0.0.1:3000/pages/hello
curl: (7) Failed to connect to 127.0.0.1 port 3000: Connection refused


# curl http://0.0.0.0:3000/pages/hello
curl: (7) Failed to connect to 0.0.0.0 port 3000: Address not available


# curl http://172.16.2.193:3000/pages/hello
{
  "code": 404,
  "error": "not find"
}
```

