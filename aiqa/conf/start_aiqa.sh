#!/bin/bash
# 根据传入的MYSQL_IP环境变量修改项目的mysql地址
mysqlip=$MYSQL_IP
ipreg='[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'

if [ $mysqlip ]; then
   #sed -i 's/192.168.180.30/'${mysqlip}'/g' /opt/project/product/AIQA/AIQA/settings.py
   sed -i "s/^'HOST': '${ipreg}',$/'HOST': '${mysqlip}',/" /opt/project/product/AIQA/AIQA/settings.py	
fi

nginx
uwsgi --ini /opt/project/product/script/uwsgi.ini
/opt/project/redis-4.0.9/src/redis-server /opt/project/redis-4.0.9/redis.conf
