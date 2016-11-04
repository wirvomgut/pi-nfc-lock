#!/bin/bash

# check if supervisor is installed
if [ $(dpkg-query -W -f='${Status}' supervisor 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
  apt-get install supervisor;
fi

#undo changes
git reset --hard HEAD
git pull -u origin master

#copy supervisor file
cp supervisor-wvg-lock.conf /etc/supervisor/conf.d/wvg-lock.conf

#update supervisor
service supervisor restart
supervisorctl reread
supervisorctl update
