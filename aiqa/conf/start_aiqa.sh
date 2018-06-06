#!/bin/bash
nginx
uwsgi --ini /opt/project/product/script/uwsgi.ini
/opt/project/redis-4.0.9/src/redis-server /opt/project/redis-4.0.9/redis.conf
