#!/usr/bin/env python
#coding:utf-8
"""
 ---- Program:
 ---- Description:
 ---- Author: Ed
 ---- Date: 2018-04-29 23:15:25
 ---- Last modified: 2018-05-01 20:14:14
"""

import mylibrary
import os
import download
import insert

if __name__ == '__main__':
    os.chdir(mylibrary.HOME)
    cur = mylibrary.login()
    cur.execute('select homepage from project')
    homepages = [each[0] for each in cur.fetchall()]
    # skill: multiprocessing会出现不明原因的错误，出现什么copy,openssl之类的warning,可以尝试修改multiprocessing运行的函数名
    mylibrary.multirunning(insert.main, homepages)

    cur.execute('select pictureurl, picturename, chaptername, projectname from picture where ifdownload = 0')
    downloadlist = cur.fetchall()
    cur.close()
    mylibrary.multirunning(download.main, downloadlist)


