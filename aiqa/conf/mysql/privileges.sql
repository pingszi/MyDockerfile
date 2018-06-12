use mysql;
select host, user from user;

update user set host = '%' where user = 'root' and host = '127.0.0.1';
grant all privileges on *.* to 'root'@'%' identified by '123456' with grant option;
flush privileges;