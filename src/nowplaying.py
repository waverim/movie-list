# -*- coding: utf-8 -*-  

import urllib2
import json
from bs4 import BeautifulSoup
import MySQLdb

def get_nowplaying():
    response = urllib2.urlopen('http://movie.douban.com/nowplaying/wuhan/')
    html_string = response.read()

    soup = BeautifulSoup(html_string)
    nowplaying =  soup.find_all(attrs={"data-category": "nowplaying"})

    arr = []
    for tag in nowplaying:
        obj = {}
        obj['id'] = tag['id']
        obj['title'] = tag['data-title']
        obj['score'] = tag['data-score']
        obj['actors'] = tag['data-actors']
        arr.append(obj)

    return arr

def update_database():
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='', \
                           port=3306, charset='utf8')
    cursor = conn.cursor()
    cursor.execute("use test")
    
    arr = get_nowplaying()
    
    for item in arr:
        try:
            m_id = int(item['id'])
            cursor.execute("insert into movie values ('%d', '%d')" % (m_id, 1))
            conn.commit()
        except:
            conn.rollback()

    conn.close()

update_database()    
