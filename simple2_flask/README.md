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

