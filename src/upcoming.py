import urllib2
import json
import re
from bs4 import BeautifulSoup

def get_upcoming():
    response = urllib2.urlopen('http://movie.douban.com/later/wuhan/')
    html_string = response.read()

    soup = BeautifulSoup(html_string)
    upcoming =  soup.find_all(attrs={"class": "intro"})
    
    arr = []
    for tag in upcoming:
        obj = {}
        obj['id'] = re.findall(r'[\d]+', tag.a['href'])[0]
        obj['date'] = tag.li.string

        movie_string = urllib2.urlopen('http://api.douban.com/v2/movie/subject/' + obj['id']).read()
        
        movie_json = json.loads(movie_string)

        obj['title'] = movie_json['title']
        
        arr.append(json.dumps(obj))

    return arr