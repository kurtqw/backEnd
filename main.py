# coding=utf-8
import tornado.ioloop
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


chattingList = {}

class Chat(object):
    def __init__(self,id1,id2):
        self.id1 = id1
        self.id2 = id2
        self.isClose = False #是否有人退出
    def register(self,id,handler):
        if id == self.id1:
            self.handler1 = handler
        elif id == self.id2:
            self.handler2 = handler
        else:
            print("Error")
    def recMessage(self, data):
        if data.get('id') == self.id1:
            self.handler2.write_message(data.get('text'))
        elif data.get('id') == self.id2:
            self.handler1.write_message(data.get('text'))
        else:
            print("Error")

    def notifyClose(self, id):
        '''
        当一方退出后，告知另一方并断开另一方的连接
        TODO : 保存聊天记录
        :param id:主动断开的一方的ID
        :return:
        '''
        if chattingList[id].id1 == id:
            chattingList[id].handler2.write_message("对方已断开")
            chattingList[id].handler2.close()
        else:
            chattingList[id].handler1.write_message("对方已断开")
            chattingList[id].handler1.close()



class Waiter(object):
    '''
    TODO : 保存聊天记录
    '''
    waiting = Queue()
    callbacks = Queue()
    def match(self,id,callback):
        '''

        :param id:
        :param callback:
        :return:
        '''
        self.waiting.put(id)
        self.callbacks.put(callback)
        if  self.waiting.qsize() > 1:
            self.notify()
    def notify(self):
        id1 = self.waiting.get()
        id2 = self.waiting.get()
        print(id1,id2)
        callback1 = self.callbacks.get()
        callback2 = self.callbacks.get()
        callback1(id1)
        callback2(id2)
        chat = Chat(id1,id2)
        chattingList[id1] = chat
        chattingList[id2] = chat



class MainHandler(tornado.web.RequestHandler):
    idSet = set()
    @tornado.web.asynchronous
    def get(self):
        id = str(uuid4())
        while id in self.idSet:
            id = str(uuid4())
        self.idSet.add(id)
        self.application.waiter.match(id,self.returnId)
    def set_default_headers(self):
        #跨域
        self.set_header('Access-Control-Allow-Origin', "null")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Allow-Credentials',"true")

    def returnId(self, id):
        self.write(json.dumps({'status':0,'id':id}))#
        self.finish()



class ChatHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.id = self.get_argument("id",-1)
        chattingList[self.id].register(self.id,self)

    def on_message(self, data):
        chattingList[self.id].recMessage(json.loads(data))

    def on_close(self):
        if not chattingList[self.id].isClose:
            print("一方退出")
            chattingList[self.id].isClose = True
            chattingList[self.id].notifyClose(self.id)
        else:
            print("另一方也退出")
    def check_origin(self, origin):
        return True


class Application(tornado.web.Application):
    def __init__(self):
        self.waiter = Waiter()
        handlers = [
            (r"/",MainHandler),
            (r"/chat",ChatHandler)
        ]
        super(Application,self).__init__(handlers)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
