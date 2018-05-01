#!/usr/bin/env python
#coding:utf-8
"""
 ---- Program:
 ---- Description:
 ---- Author: Ed
 ---- Date: 2018-04-30 16:10:27
 ---- Last modified: 2018-04-30 20:31:00
"""

import mylibrary

def insert(homepage, cur, pid):
    print('I am parsing the page {}! pid'.format(homepage), pid)
    cur.execute('select projectname, latest from project where homepage = %s', homepage)
    projectname, latest = cur.fetchone()


    if homepage == 'http://ww1.readheroacademia.com':
        parser = mylibrary.Parser1(homepage, projectname, latest)
    elif 'http://www.goodmanga.net' in homepage:
        parser = mylibrary.Parser0(homepage, projectname, latest)
    elif 'manganelo.com' in homepage:
        parser = mylibrary.Parser2(homepage, projectname, latest)

    chapterurls = parser.GetChapterUrls()

#      print(len(parser.completedchapters))
    #  print(len(chapterurls))

    insertlist = []
    for eachchapterurl in chapterurls:
        insertlist.extend(parser.CreateInsertlist(eachchapterurl))
        # skill : how to merge two dicts in together
        # skill : how to us os.path.splitext() Note that it turns a tuple
        # skill : how to use dict comprehension to create dict object

    pictureurls = [each[0] for each in insertlist]
    nonduplicated = mylibrary.duplicatedpicture(pictureurls, cur)
    insertlist = [each for each in insertlist
                  if each[0] in nonduplicated]
    sql = 'insert into picture(pictureurl, picturename, chaptername, PROJECTNAME) values(%s,%s,%s,%s)'
    cur.executemany(sql, insertlist)
    print('{} entries has been inserted into TABLE picture'.format(len(insertlist)))

def main(homepages, pid=0):
    print('Hi, this is insert.py')
    cur = mylibrary.login()
    for eachpage in homepages:
        insert(eachpage, cur, pid)
    cur.close()

if __name__ == '__main__':
    # homepage = [ 'http://www.goodmanga.net/9825/boku-no-hero-academia' ]
    # homepage = ['http://ww1.readheroacademia.com']
    homepage = ['http://www.goodmanga.net/18949/goblin-slayer-side-story-year-one']
    homepage = ['http://manganelo.com/manga/platina_end']
    main(homepage)

