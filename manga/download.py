#!/usr/bin/env python
#coding:utf-8

"""
 ---- Program:
 ---- Description:
 ---- Author: Ed
 ---- Date: 2018-04-30 17:19:11
 ---- Last modified: 2018-05-01 13:34:26
"""

import mylibrary
import os

def create_folder(downloadlist):
    folder = [
        (each_chapter, each_project) for
        eachurl, each_picture, each_chapter, each_project in downloadlist
              ]
    folder = list(set(folder))

    existed_project = [each.upper() for each in os.listdir()]
    for each_chapter, each_project in folder:
        if each_project.upper() not in existed_project:
            os.mkdir(each_project)
        # skill: how to use os.path.join

        chapter_folder = os.path.join(each_project, each_chapter)

        existed_chapters = [
            os.path.join(each_project, existed_chapter) for
                existed_chapter in os.listdir(each_project)
                            ]

        if chapter_folder not in existed_chapters:
            os.mkdir(chapter_folder)
            print('chapter {0} of {1} has been created!'.format(each_chapter, each_project))

def download(downloadlist, cur):
    for eachurl,each_picture, each_chapter, each_project in downloadlist:
        flag, response = mylibrary.myrequests(eachurl)
        if flag == -1:
            with open('/'.join([each_project, each_chapter.strip(), each_picture]), 'wb') as jpg:
                jpg.write(response.content)
            cur.execute('update picture set ifdownload = 1 where pictureurl = %s', eachurl)
            print('{0} of chapter {1} of project {2} is downloaded successfully!'\
                  .format(each_picture, each_chapter, each_project))
        else:
            print('{0} of chapter {1} of project {2} fails to be downloaded!'\
                  .format(each_picture, each_chapter, each_project))


def main(downloadlist, pid = 0):
    global cur
    print('Hi, I am downloadlack.py, pid : ', pid)
    print('{} items will be downloaded'.format(len(downloadlist)))
    os.chdir(mylibrary.HOME)
    create_folder(downloadlist)
    download(downloadlist, cur)

cur = mylibrary.login()

if __name__ == '__main__':
    cur.execute('select pictureurl, picturename, chaptername, projectname from picture where ifdownload = 0')
    # downloadlist  = [('http://www.goodmanga.net/images/manga/goblin-slayer/8/18.jpg','18.jpg','8','Goblin Slayer'),('http://www.goodmanga.net/images/manga/goblin-slayer/8/21.jpg','21.jpg','8','Goblin Slayer'),('http://www.goodmanga.net/images/manga/goblin-slayer/8/25.jpg','25.jpg','8','Goblin Slayer'),('http://www.goodmanga.net/images/manga/goblin-slayer/8/29.jpg','29.jpg','8','Goblin Slayer'),('http://www.goodmanga.net/images/manga/goblin-slayer/8/32.jpg','32.jpg','8','Goblin Slayer')]
    downloadlist = cur.fetchall()
    main(downloadlist)
    cur.close()
