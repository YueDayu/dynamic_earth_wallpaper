#!/bin/bash
script_path=$(readlink -f "$0")
bashpath=$(dirname "${script_path}")
python_client="python"
generate_path=$bashpath/generate

origin_img=$generate_path/origin.jpg
process_img=$generate_path/process.jpg
bg_img=$bashpath/data/bg.jpg

mkdir -p $generate_path

wget "http://img.nsmc.org.cn/CLOUDIMAGE/FY4A/MTCC/FY4A_DISK.JPG" -O $origin_img

$python_client $bashpath/process.py $origin_img $process_img $bg_img

PID=$(pgrep gnome-session)
export DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$PID/environ|cut -d= -f2-)

/usr/bin/gsettings set org.gnome.desktop.background picture-uri "file:///$process_img"
/usr/bin/gsettings set org.gnome.desktop.background picture-options scaled
