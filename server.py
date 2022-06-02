import os
import time
from typing import Optional, Awaitable
from datetime import date


import tornado.ioloop
import tornado.web
from tornado import gen


@gen.coroutine
def async_sleep(timeout):
    """ Sleep without blocking the IOLoop. """
    yield gen.coroutine(tornado.ioloop.IOLoop.current().add_timeout)


class MainHandler(tornado.web.RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    @gen.coroutine
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        # clienttime = float(self.get_query_argument('lastmod'))
        name = self.get_query_argument('name')
        print(name)
        servertime, data = os.path.getmtime('file.txt'), {}
        # print(type(slm),type(clm))
        # while servertime <= clienttime:
        #     yield async_sleep(1)
        #     servertime = os.path.getmtime('file.txt')
        fl = open("file.txt", 'r')
        data['body'] = fl.read()
        # data["time"] = 4325
        data['lastmod'] = servertime
        fl.close()
        # data = {
        #     "Received": True,
        #     "name": "Noha",
        #     "test": "Mostafa"
        # }
        self.write(data)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()