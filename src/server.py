import tornado.ioloop
import tornado.web

import json
import nowplaying
import upcoming

class Index(tornado.web.RequestHandler):
    def get(self):
        self.write('<a href="/nowplaying">Nowplaying</a><br><a href="/upcoming">Upcoming</a>')


class Nowplaying(tornado.web.RequestHandler):
    def get(self):
        arr = nowplaying.get_nowplaying()
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(arr))


class Upcoming(tornado.web.RequestHandler):
    def get(self):
        arr = upcoming.get_upcoming()
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(arr))
        
        
application = tornado.web.Application([
    (r"/", Index),
    (r"/nowplaying", Nowplaying),
    (r"/upcoming", Upcoming),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
