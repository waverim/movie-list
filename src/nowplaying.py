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
            cursor.execute("insert into nowplaying values (int(item['id']), item['title'], float(item['score']), item['actors'])")
            conn.commit()
        except:
            conn.rollback()

    conn.close()