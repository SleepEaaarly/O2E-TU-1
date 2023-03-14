#!/bin/bash
DIR=/home/admin

time=`date -d "now" +%Y-%m-%d-%H-%M`
mv $DIR/django.log $DIR/django_log/django$time.log

PID=`ps -aux | grep manage.py | grep -v grep | awk '{print $2}'` 

if [ -n "$PID" ]; then
	echo $PID | xargs kill -9
fi
echo "running backend"
nohup python manage.py runserver 0.0.0.0:8000> $DIR/django.log 2>&1 & exit
