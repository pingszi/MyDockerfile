#!/bin/bash
set -e
 
# 启动mysql
echo '1.启动mysql....'
service mysql start
 
# 导入数据
echo '2.开始导入数据....'
mysql < /mysql/aiqa.sql
echo '3.导入数据完毕....'

# 重设置密码
echo '4.开始修改密码....'
mysql < /mysql/privileges.sql
echo '5.修改密码完毕....'
