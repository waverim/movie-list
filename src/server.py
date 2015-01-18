import tornado.ioloop
import tornado.web

import json
import nowplaying
import upcoming

class Index(tornado.web.RequestHandler):
    def get(self):
        arr = nowplaying.get_nowplaying()

        self.write('<h2>Now Playing</h2>')
        for i in arr:
            data = json.loads(i)
            self.write('<p><a href="http://movie.douban.com/subject/' + data["id"] + '/">')
            self.write(' ' + data["title"] + ' </a></p>')
            self.write('<p style="text-indent: 2em;">Score: ' + data["score"]+ '</p>')
            self.write('<p style="text-indent: 2em;">Actors: ' + data["actors"]+ '</p>')

        up = upcoming.get_upcoming()

        self.write('<h2>Upcoming</h2>')
        for i in up:
            data = json.loads(i)
            self.write('<p><a href="http://movie.douban.com/subject/' + data["id"] + '/">')
            self.write(' ' + data["title"] + ' </a></p>')
            self.write('<p style="text-indent: 2em;">Coming date: ' + data["date"]+ '</p>')

application = tornado.web.Application([
    (r"/", Index),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
