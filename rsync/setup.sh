#!/usr/bin/env bash

CONFIG_PATH="/etc/zrsync"
SCRIPT_PATH="/var/zrsync"
if [ ! -d $CONFIG_PATH ] ; then
    mkdir $CONFIG_PATH
    cp ./config.yml $CONFIG_PATH
fi

if [ ! -d $SCRIPT_PATH ] ; then
    mkdir $SCRIPT_PATH
    cp ./zrsync.py $SCRIPT_PATH
fi

cp ./zrsync.service /usr/lib/systemd/system
systemctl enable zrsync
systemctl start zrsync 
