#!/bin/bash

wget "http://img.nsmc.org.cn/CLOUDIMAGE/FY4A/MTCC/FY4A_DISK.JPG" -O /home/sensetime/code/wallpaper/data/origin.jpg

/usr/bin/python /home/sensetime/code/wallpaper/process.py /home/sensetime/code/wallpaper/data/origin.jpg /home/sensetime/code/wallpaper/data/process.jpg

PID=$(pgrep gnome-session)
export DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$PID/environ|cut -d= -f2-)

/usr/bin/gsettings set org.gnome.desktop.background picture-uri "file:///home/sensetime/code/wallpaper/data/process.jpg"
/usr/bin/gsettings set org.gnome.desktop.background picture-options spanned
