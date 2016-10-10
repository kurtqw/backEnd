# coding=utf-8
import random
import time
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
from utils import Result
from newsHandler import NewsHandler
chattingList = {}

class Message(object):
    def __init__(self,sender, data):
        self.sender = sender
        self.type = data.get('type')
        self.content = data.get('text')
        self.time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    def response(self):
        return self.time + "\n" + self.sender+"\t" + self.content


class Chat(object):
    def __init__(self, id1, id2, nameIndex1, nameIndex2):
        self.id1 = id1
        self.id2 = id2
        self.nameIndex1 = nameIndex1
        self.nameIndex2 = nameIndex2
        self.isClose = False #是否有人退出
        self.messageRecord = []
    def register(self,id,handler):
        if id == self.id1:
            self.handler1 = handler
        elif id == self.id2:
            self.handler2 = handler
        else:
            print("Error")
    def recMessage(self, data):
        '''
        收到一方的消息，将其发给另外一方
        TODO:存储记录
        :param data:
        :return:
        '''
        if data.get('id') == self.id1:
            message = Message(Application.femaleNames[int(self.nameIndex1)],data)
            self.messageRecord.append(message)
            self.handler2.write_message(message.response())
        elif data.get('id') == self.id2:
            message = Message(Application.maleNames[int(self.nameIndex2)],data)
            self.messageRecord.append(message)
            self.handler1.write_message(message.response())
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
           性别区分

    '''
    maleWaiting = Queue()
    maleCallbacks = Queue()
    maleNameIndex = Queue()
    femaleWaiting = Queue()
    femaleCallbacks = Queue()
    femaleNameIndex = Queue()
    def match(self, id, sex, nameIndex, callback):
        '''
        :param id:
        :param sex: 0:male,1:female
        :param callback:
        :param nameIndex the index of name in name list
        :return:
        '''
        if sex == '0':
            self.maleWaiting.put(id)
            self.maleCallbacks.put(callback)
            self.maleNameIndex.put(nameIndex)
            if  self.femaleWaiting.qsize() > 0:
                self.notify()
        else:
            self.femaleWaiting.put(id)
            self.femaleCallbacks.put(callback)
            self.femaleNameIndex.put(nameIndex)
            if self.maleWaiting.qsize() > 0:
                self.notify()
    def notify(self):
        id1 = self.femaleWaiting.get()
        id2 = self.maleWaiting.get()
        nameIndex1 = self.femaleNameIndex.get()
        nameIndex2 = self.maleNameIndex.get()
        print(id1,id2)
        callback1 = self.femaleCallbacks.get()
        callback2 = self.maleCallbacks.get()
        callback1(id1)
        callback2(id2)
        chat = Chat(id1, id2, nameIndex1, nameIndex2)
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
        sex = self.get_argument('sex')
        print(sex)
        nameIndex = self.get_argument("nameIndex")
        self.application.waiter.match(id, sex, nameIndex, self.returnId)
    def set_default_headers(self):
        #跨域
        self.set_header('Access-Control-Allow-Origin', "null")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Allow-Credentials',"true")

    def returnId(self, id):
        self.write(json.dumps({'status':1,'id':id}))#
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

class NameHandler(tornado.web.RequestHandler):
    def get(self):
        res = Result()
        names = {}
        sex = self.get_argument("sex")
        if sex == "0":#male
            for i in range(8):#一次返回8个名字
                index = random.randint(0, len(Application.maleNames)-1)
                while index in names.keys():
                    index = random.randint(0, len(Application.maleNames)-1)
                names[index] = Application.maleNames[index]

        else:
            for i in range(8):#一次返回8个名字
                index = random.randint(0, len(Application.femaleNames)-1)
                while index in names.keys():
                    index = random.randint(0, len(Application.femaleNames)-1)
                names[index] = Application.femaleNames[index]
        res.setData(names)
        self.write(res.getRes())

class Application(tornado.web.Application):
    def __init__(self):
        self.waiter = Waiter()
        self.readNames()
        handlers = [
            (r"/",MainHandler),
            (r"/chat",ChatHandler),
            (r"/name", NameHandler),
            (r"/news", NewsHandler)
        ]
        super(Application,self).__init__(handlers)
    def readNames(self):
        Application.maleNames = []
        with open("maleNameList") as male:
            line = male.readline()
            while line:
                Application.maleNames.append(line.strip("\n"))
                line = male.readline()
        Application.femaleNames = []
        with open("femaleNameList") as female:
            line = female.readline()
            while line:
                Application.femaleNames.append(line.strip("\n"))
                line = female.readline()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
