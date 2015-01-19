import urllib2
import json
from bs4 import BeautifulSoup

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
