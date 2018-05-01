#!/usr/bin/env python
#coding:utf-8
"""
 ---- Program:
 ---- Description:
 ---- Author: Ed
 ---- Date: 2018-04-29 23:14:39
 ---- Last modified: 2018-05-01 20:36:31
"""

import multiprocessing
import os
import requests
import re
from bs4 import BeautifulSoup
import pymysql

HOME = 'c:/users/edwardelric/desktop/comics'

def login():
    # Login in mysql
    config = {'user':'wang','db':'manga','autocommit':'True', 'host': '10.43.37.104', 'charset':'utf8mb4'}
    #  config = {'user':'wang','db':'manga','autocommit':'True', 'host': '172.30.136.1', 'charset':'utf8mb4'}
    connection = pymysql.connect(**config)
    cur = connection.cursor()
    return cur

class Parser():
# skill: how to use CLASS

    def __init__(self, homepage, projectname, latest):
        self.homepage = homepage
        self.latest = - latest
        self.projectname = projectname

        cur = login()
        cur.execute('select chaptername from chapter where lacknum = 0 and projectname = %s', self.projectname)
        self.completedchapters = [each[0] for each in cur.fetchall()]
        cur.execute('select pictureurl from picture where ifdownload = 1 and projectname = %s', self.projectname)
        self.completedpictures =[each[0] for each in cur.fetchall()]
        cur.close()

##################################################

#  class Parser1(Parser):
    #  def GetChapterUrls(self):
    #  def GetPictureUrls(self, chapterurl):
    #  def CreateInsertlist(self, chapterurl):

class Parser1(Parser):

    def GetChapterUrls(self):
        '''
        Get new chapters urls
        '''
        flag, response = myrequests(self.homepage)
        if flag == -1:
            soup = BeautifulSoup(response.text, 'lxml')
            chapterurls = [eachurl.get('href') for eachurl in soup.find_all('a')]
            chapterurls = [eachurl.strip() for eachurl in chapterurls if 'chapter' in eachurl]
        else:
            print('Network is not avaliable')

        chapternames = [re.search(r'academia-chapter-(\d{0,3})', eachurl).group(1)
                        for eachurl in chapterurls]
        chapters = dict(zip(chapternames, chapterurls))

        newchapterurls = [chapters[eachname] for eachname
                          in set(chapternames) - set(self.completedchapters)]
        return newchapterurls

    def GetPictureUrls(self, chapterurl):
        flag, response = myrequests(chapterurl)
        if flag == -1:
            soup = BeautifulSoup(response.text, 'lxml')
            pictureurls = [eachurl.get('src') for eachurl in soup.find_all('img')]
            pictureurls = [eachurl.strip() for eachurl in pictureurls if 'blogspot' in eachurl]
        else:
            print('Network is not avaliable')
        return list(set(pictureurls) - set(self.completedpictures))

    def CreateInsertlist(self, chapterurl):
        chaptername = re.search(r'academia-chapter-(\d{0,3})', chapterurl).group(1)
        insertlist = ([
        (eachpictureurl, ''.join([str(i+1),
        os.path.splitext(eachpictureurl)[-1]]), chaptername, self.projectname)
            for i, eachpictureurl in enumerate(self.GetPictureUrls(chapterurl))
        ])
        return insertlist

class Parser0(Parser):

    def sort_urls(self, oldurls, reverse):
        temp = {}
        for each in oldurls:
            temp[float(each.split('/')[-1])] = each
        newurls = [temp[each] for each in sorted(temp.keys(),reverse = reverse)]
        return newurls

    def GetChapterUrls(self):
        '''
        :param latest: 返回最新的url的个数，latest = -1表示返回全部url, latest = 1表示返回最新一话的url
        :return urls: All chapter urls of the chapter
        '''
        # Get all pages
        flag, response = myrequests(self.homepage)
        soup = BeautifulSoup(response.text,'lxml')

        allpages = [each.get('href') for each in soup.find_all('button') if each.get('href') is not None]
        allpages = [each for each in allpages if re.search('page', each) is not None]
        allpages.append(self.homepage)

        chapterurls = []
        for eachpage in allpages:
            flag, response = myrequests(eachpage)
            soup = BeautifulSoup(response.text, 'lxml')
            for eachtag in soup.find_all('a'):
                chapterurl = eachtag.get('href')
                if re.search('chapter', chapterurl) is not None:
                    chapterurls.append(chapterurl)

        # skill: How th sort the elements of a list
        chapterurls = self.sort_urls(chapterurls, reverse = True)

        if self.latest < 0:
            chapterurls = chapterurls[self.latest:]
        elif self.latest > 0:
            chapterurls = chapterurls[:self.latest]

        chapternames = [eachurl.split('/')[-1].strip() for eachurl in chapterurls]
        chapters = dict(zip(chapternames, chapterurls))

        newchapterurls = [chapters[eachname] for eachname
                          in set(chapternames) - set(self.completedchapters)]
        return newchapterurls

    def GetPictureUrls(self, chapterurl):
        '''
        :param url: the url of a chapter
        :return maxpicture:the max picuture number of the chapter and the
        :return  picturedomain: the domain url of a picuture url, used to construct the urls of picture
        '''
        flag, response = myrequests(chapterurl)
        pattern = '<span>of (.*?)</span>'
        maxpicture = int(re.search(pattern,response.text).group(1))

        pattern = r'<img src="(http://www.goodmanga.net/images/manga.*?)/1.jpg"'
        picturedomain = re.search(pattern, response.text).group(1).replace(' ','')

        # skill: how to use map and format
        pictureurls = list(map((picturedomain + '/{}.jpg' ).format, range(1, maxpicture + 1)))
        return list(set(pictureurls) - set(self.completedpictures))

    def CreateInsertlist(self, chapterurl):
        chaptername = chapterurl.split('/')[-1]
        insertlist = ([
        (eachpictureurl, eachpictureurl.split('/')[-1], chaptername, self.projectname)
            for eachpictureurl in self. GetPictureUrls(chapterurl)
        ])
        return insertlist

class Parser2(Parser):

    def GetChapterUrls(self):
        flag, response = myrequests(self.homepage)
        soup = BeautifulSoup(response.text, 'lxml')
        urls = [each.a.get('href') for each in soup.find_all('div', class_ = 'row') if each.a is not None]
        # skill: reversed() sort(reverse = reverse)
        if self.latest >0:
            chapterurls = urls[:self.latest]
        elif self.latest<0:
            chapterurls = urls[self.latest:]
        else:
            chapterurls = urls
        return chapterurls


    def GetPictureUrls(self, chapterurl):
        flag, response = myrequests(chapterurl)
        soup = BeautifulSoup(response.text, 'lxml')
        pictureurls = [each.get('src') for each in soup.find_all('img', class_ = 'img_content')]
        return pictureurls

    def CreateInsertlist(self, chapterurl):
        chaptername = chapterurl.split('_')[-1]
        insertlist = ([
        (eachpictureurl, ''.join([str(i+1), os.path.splitext(eachpictureurl)[-1]]), chaptername, self.projectname)
            for i, eachpictureurl in enumerate(self. GetPictureUrls(chapterurl))
        ])
        return insertlist

##################################################

def multirunning(func, arg):
    '''
    Multiprocessing the script
    '''
    # Split downloadlist into groups for pooling
    groups = []
    for i in range(4):
        groups.append(arg[i::4])

    result = []
    pool = multiprocessing.Pool()
    for i in range(4):
        result.append(pool.apply_async(func,(groups[i], i+1), error_callback = print))
    pool.close()
    pool.join()

def myrequests(url, maxtry = 5):
    '''
    :parm: maxtry 连接的最大尝试次数
    :return flag = -1时，说明下载成功
    '''
    flag = 0
    while flag >= 0 and flag < maxtry:
        if flag != 0:
            print('Connection to {} fails! Trying to reconnection {} times'.format(url,flag + 1))
        try:
            response = requests.get(url, timeout=3)
        except Exception:
            flag += 1
        else:
            flag = -1
    if flag == -1:
        return flag, response
    else:
        print('Connection to %s fails'%url)
        return flag, None

def duplicatedpicture(pictureurls, cur):
    getnum = len(pictureurls)
    cur.execute('select pictureurl from picture')
    existed = [each[0] for each in cur.fetchall()]
    pictureurls = list(set(pictureurls) - set(existed))
    returnum = len(pictureurls)
    print('Hi, this is duplicatedpicture, I get {} return {}'.format(getnum, returnum))
    return pictureurls

if __name__ == '__main__':
    cur = login()
    cur.close()



