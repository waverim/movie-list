import urllib2
import json
import re
from bs4 import BeautifulSoup

import gevent
import gevent.monkey

def get_upcoming():
    response = urllib2.urlopen('http://movie.douban.com/later/wuhan/')
    html_string = response.read()

    soup = BeautifulSoup(html_string)
    upcoming = soup.find_all(attrs={"class": "intro"})
    
    id_list = [re.findall(r'[\d]+', item.a['href'])[0] for item in upcoming]
    
    detail_list = [gevent.spawn(get_movie_detail, item) for item in id_list]
    gevent.joinall(detail_list)

    for index, item in enumerate(detail_list):
        detail_list[index] = item.value
    #result = [i.value for i in detail_list]
    return result

def get_movie_detail(movie_id):
    movie_string = urllib2.urlopen('http://api.douban.com/v2/movie/subject/' + movie_id).read()
    movie_json = json.loads(movie_string)
    return movie_json
