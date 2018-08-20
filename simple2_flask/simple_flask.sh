#!/bin/bash


status(){
   echo -e "\033[41;30m =========status====== \033[0m"
   ps -ef |grep uwsgi_config.ini|grep -v grep
   
}

start() {
    echo -e "\033[41;30m ==========start====== \033[0m"
    uwsgi --ini uwsgi_config.ini --daemonize /var/log/simple2flask.log
    sleep 1
    chmod 666 /tmp/simpleflask.sock
}

stop() {
    echo -e "\033[41;30m ==========stop======= \033[0m"
    ps -ef |grep uwsgi_config.ini|grep -v grep|awk '{ if ( $3 == "1" ) print $2 }'|xargs kill -9
}

restart() {
    stop;
    sleep 1;
    start;
    status;
}

case "$1" in
    'start')
        start
        ;;
    'stop')
        stop
        ;;
    'status')
        status
        ;;
    'restart')
        restart
        ;;
    *)
    echo "usage: $0 {start|stop|restart|status}"
    exit 1
        ;;
    esac