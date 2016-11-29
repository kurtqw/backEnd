# coding=utf-8
import random
import time
import tornado.ioloop
from newsHandler import NewsHandler, JokeHanlder
from chat import Waiter
from chat import MatchHandler, ChatHandler, NameHandler, OtherNameHandler
import tornado.web
import tornado.httpserver
import tornado.options
import json
import tornado.httpclient
import tornado.websocket
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4
from queue import Queue
from utils import Result

global chattingList

class Application(tornado.web.Application):
    def __init__(self):
        self.waiter = Waiter()
        self.readNames()
        handlers = [
            (r"/", MatchHandler),
            (r"/chat", ChatHandler),
            (r"/name", NameHandler),
            (r"/othername", OtherNameHandler),
            (r"/news", NewsHandler),
            (r"/joke", JokeHanlder)
        ]
        super(Application, self).__init__(handlers)

    def readNames(self):
        self.maleNames = []
        with open("./nameList/maleNameList") as male:
            line = male.readline()
            while line:
                self.maleNames.append(line.strip("\n"))
                line = male.readline()
        self.femaleNames = []
        with open("./nameList/femaleNameList") as female:
            line = female.readline()
            while line:
                self.femaleNames.append(line.strip("\n"))
                line = female.readline()
        self.allNames = self.maleNames + self.femaleNames


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
