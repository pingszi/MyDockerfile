#!/bin/bash

nginx
/opt/java/redis/redis-4.0.9/src/redis-server /opt/java/redis/redis-4.0.9/redis.conf&
java -jar /opt/java/oms/EduS-app-0.0.1-SNAPSHOT.war&
java -jar /opt/java/oms/EduS-oms-0.0.1-SNAPSHOT.war