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
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='anna', \
                           port=3306, charset='utf8')
    cursor = conn.cursor()
    cursor.execute("use test")
    
    arr = get_nowplaying()

    current_id_list = [int(item['id']) for item in arr]

    cursor.execute("select movie_id from movie where movie_type='1'")
    old_id_list = [i[0] for i in cursor.fetchall()]

    should_delete_id_list = list(set(old_id_list) - set(current_id_list))

    print should_delete_id_list
    
    for item in should_delete_id_list:
        try:
            cursor.execute("delete from movie where movie_id = %d" % (item))
            conn.commit()
        except:
            conn.rollback()

    for item in arr:
        try:
            cursor.execute("insert ignore into movie values ('%d', '%d', '%s')" % (int(item['id']), 1, item['title']))
            conn.commit()
        except:
            conn.rollback()

    conn.close()

update_database()    
