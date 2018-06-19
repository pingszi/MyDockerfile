#!/bin/bash
set -e
 
# 启动mysql
echo '启动mysql....'
service mysql start
sleep 2
echo `service mysql status`
 
echo 'mysql启动成功.....'
 
tail -f /dev/null