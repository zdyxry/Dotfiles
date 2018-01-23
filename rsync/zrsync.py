#!/usr/bin/env python
# -*- coding:UTF-8 -*-

# this script path is /var/zrsync/


import sys
import time
import logging
import os
import sys
import pexpect
import string
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from watchdog.events import LoggingEventHandler
import yaml


#read config file
f = open('/etc/zrsync/config.yml','r')
config = yaml.load(f.read())


# backup host parameters
remoteHost = config['host']
remoteLogin = config['user']
remotePasswd = config['passwd']
remoteDir = config['remotedir']

# monitor local path
localDir = config['localdir']

log_file = '/var/log/zrsynclog'

def pexpectRun(cmd):
    ssh = pexpect.spawn(cmd,[],86400,logfile=sys.stdout)
    try:
        while True:
            i = ssh.expect(['password', 'continue connecting (yes/no)?'])
            if i == 0:
                ssh.sendline(remotePasswd)
                break
            elif i == 1:
                ssh.sendline('yes')
    except pexpect.EOF:
        ssh.close()
    else:
        ssh.expect(pexpect.EOF)
        ssh.close()
             
    print "Done"


def rsyncFile(file):
    localFile = os.path.join(localDir,file.replace(' ','\ '))
    remoteFile = os.path.join(remoteDir,file.replace(' ','\ '))
    cmd = 'rsync -avz -s %s %s@%s:%s' % (localFile,remoteLogin,remoteHost,remoteFile)
    print cmd
    pexpectRun(cmd)

    

def deleteFile():
    cmd = 'rsync -avz --delete %s %s@%s:%s' % (localDir,remoteLogin,remoteHost,remoteDir)
    print cmd
    pexpectRun(cmd)

def modifiedFile():
    cmd = 'rsync -avz %s %s@%s:%s' % (localDir,remoteLogin,remoteHost,remoteDir)
    print cmd
    pexpectRun(cmd)


class DwPatternMatchingEventHandler(PatternMatchingEventHandler,LoggingEventHandler):
    def on_created(self,event):
        logging.info("Created file: %s",event.src_path)
        name = event.src_path.split(localDir)
        watchname = name[-1].decode('utf8')
        rsyncFile(watchname)
    def on_deleted(self,event):
        logging.info("Deleted file: %s",event.src_path)
        deleteFile()
    def on_modified(self,event):
        logging.info("Modified file: %s",event.src_path)
        modifiedFile()
    def on_moved(self,event):
        logging.info("Moved file: %s",event.src_path)
        deleteFile()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    event_handler = DwPatternMatchingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, localDir, recursive=True)
    observer.start()
    try:
        logging.info("Observer start")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shuting down watcher")
        observer.stop()
    observer.join()
