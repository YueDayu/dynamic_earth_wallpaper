#!/bin/bash

bashpath="/home/sensetime/code/wallpaper"
python_client="/usr/bin/python"

wget "http://img.nsmc.org.cn/CLOUDIMAGE/FY4A/MTCC/FY4A_DISK.JPG" -O $bashpath/data/origin.jpg

$python_client $bashpath/process.py $bashpath/data/origin.jpg $bashpath/data/process.jpg

PID=$(pgrep gnome-session)
export DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$PID/environ|cut -d= -f2-)

/usr/bin/gsettings set org.gnome.desktop.background picture-uri "file:///$bashpath/data/process.jpg"
/usr/bin/gsettings set org.gnome.desktop.background picture-options spanned
