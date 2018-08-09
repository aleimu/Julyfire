**socket、socketio、flask-socketio、WebSocket的区别与联系**

- socket 是通信的基础，并不是一个协议，Socket是应用层与TCP/IP协议族通信的中间软件抽象层，它是一组接口。在设计模式中，Socket其实就是一个门面模式，它把复杂的TCP/IP协议族和UDP协议族隐藏在Socket接口后面，对用户来说，一组简单的接口就是全部，让Socket去组织数据，以符合指定的协议。
- WebSocket 是html5新增加的一种通信协议,可以类比于http协议。常见的应用方式如弹幕、web在线游戏。
- socketio 是基于socket连接后(并没有自己实现socket的链接而是复用了web框架或eventlet、gevent的socket)对网络输入输出流的处理，封装了send、emit、namespace、asyncio 、订阅等接口，同时扩展使用了redis、rabbitmq消息队列的方式与其他进程通信。
- flask-socketio 是socketio对flask的适配，封装了emit、send和关于room的操作。
select的链接、发送等底层操作还是在flask中做的，socketio对其做了抽象。使用threading模式时并没有自己实现socket的链接而是复用了web框架的socket，也可以指定使用gevent和eventlet中的select多路复用已提高性能。

**总结**

HTTP、WebSocket 等应用层协议，都是基于 TCP 协议来传输数据的。我们可以把这些高级协议理解成对 TCP 的封装。
既然大家都使用 TCP 协议，那么大家的连接和断开，都要遵循 TCP 协议中的三次握手和四次挥手，只是在连接之后发送的内容不同，或者是断开的时间不同。
对于 WebSocket 来说，它必须依赖 HTTP 协议进行一次握手 ，握手成功后，数据就直接从 TCP 通道传输，与 HTTP 无关了。


                    
- 网络协议全景
- http://www.colasoft.com.cn/download/protocols_map.php

![image](https://blog.zengrong.net/uploads/2014/12/TCP-IP.gif)

##### 在源码flask_socketio.SocketIO#run方法中可以看出 select 多路复用的几种选择。
```python
    if self.server.eio.async_mode == 'threading':
        from werkzeug._internal import _log
        _log('warning', 'WebSocket transport not available. Install '
                        'eventlet or gevent and gevent-websocket for '
                        'improved performance.')
        app.run(host=host, port=port, threaded=True,
                use_reloader=use_reloader, **kwargs)
        # 这里的 app 就是 app = Flask(__name__)
    elif self.server.eio.async_mode == 'eventlet':
        def run_server():
            import eventlet
            import eventlet.wsgi
            import eventlet.green
            addresses = eventlet.green.socket.getaddrinfo(host, port)
            if not addresses:
                raise RuntimeError('Could not resolve host to a valid address')
            eventlet_socket = eventlet.listen(addresses[0][4], addresses[0][0])

            # If provided an SSL argument, use an SSL socket
            ssl_args = ['keyfile', 'certfile', 'server_side', 'cert_reqs',
                        'ssl_version', 'ca_certs',
                        'do_handshake_on_connect', 'suppress_ragged_eofs',
                        'ciphers']
            ssl_params = {k: kwargs[k] for k in kwargs if k in ssl_args}
            if len(ssl_params) > 0:
                for k in ssl_params:
                    kwargs.pop(k)
                ssl_params['server_side'] = True  # Listening requires true
                eventlet_socket = eventlet.wrap_ssl(eventlet_socket,
                                                    **ssl_params)

            eventlet.wsgi.server(eventlet_socket, app,
                                 log_output=log_output, **kwargs)

        if use_reloader:
            run_with_reloader(run_server, extra_files=extra_files)
        else:
            run_server()
    elif self.server.eio.async_mode == 'gevent':
        from gevent import pywsgi
        try:
            from geventwebsocket.handler import WebSocketHandler
            websocket = True
        except ImportError:
            websocket = False
```

##### 参考博客
https://www.cnblogs.com/minsons/p/8251780.html

http://python-socketio.readthedocs.io/en/latest/