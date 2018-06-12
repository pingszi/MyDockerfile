#!/bin/bash
set -e
 
#查看mysq状态
echo `service mysql status`
 
# 启动mysql
echo '1.启动mysql....'
service mysql start
sleep 3
echo `service mysql status`
 
# 导入数据
echo '2.开始导入数据....'
mysql < /mysql/aiqa.sql
echo '3.导入数据完毕....'
sleep 3
echo `service mysql status`

# 重设置密码
echo '4.开始修改密码....'
mysql < /mysql/privileges.sql
echo '5.修改密码完毕....'
 
echo 'mysql容器启动成功.....'
 
tail -f /dev/null
