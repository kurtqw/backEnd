# coding=utf-8
import time
import json
import random
from uuid import uuid4
from queue import Queue
from utils import Result

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.httpclient
import tornado.websocket
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options


chattingList = {}


class Person(object):
    def __init__(self, id, sex, nameIndex, callback, application):
        '''
        :param id:
        :param sex: 0:male,1:female
        :param callback:
        :param nameIndex the index of nameList in nameList list
        '''
        self.id = id
        self.sex = sex
        self.nameIndex = nameIndex
        self.returnId = callback  # 返回ID给前端的函数
        if sex == '0':
            self.name = application.maleNames[int(nameIndex)]
        else:
            self.name = application.femaleNames[int(nameIndex)]


class Message(object):
    def __init__(self, sender, data):
        #发送该消息的人
        self.sender = sender
        self.type = data.get('type')
        self.content = data.get('text')
        self.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def response(self):
        res = Result()
        data = dict()
        data["sender"] = self.sender
        data["type"] = self.type
        data["content"] = self.content
        data["time"] = self.time

        res.setData(data)
        return res.getRes()


class Chat(object):
    def __init__(self, person1, person2):
        self.person1 = person1
        self.person2 = person2
        self.isClose = False  # 是否有人退出
        self.messageRecord = []

    def register(self, id, handler):
        if id == self.person1.id:
            self.handler1 = handler
        elif id == self.person2.id:
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
        if data.get('id') == self.person1.id:
            message = Message(self.person1.name, data)
            self.messageRecord.append(message)
            self.handler2.write_message(message.response())
        elif data.get('id') == self.person2.id:
            message = Message(self.person2.name, data)
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
        if chattingList[id].person1.id == id:
            chattingList[id].handler2.write_message("对方已断开")
            chattingList[id].handler2.close()
        else:
            chattingList[id].handler1.write_message("对方已断开")
            chattingList[id].handler1.close()


class Waiter(object):
    '''
    '''
    malesWaiting = Queue()
    femalesWaiting = Queue()

    def match(self, person):

        if person.sex == '0': #male
            self.malesWaiting.put(person)
            if self.femalesWaiting.qsize() > 0:
                self.notify(2)
            elif self.malesWaiting.qsize() > 1:
                self.notify(0)
        else:
            self.femalesWaiting.put(person)
            if self.malesWaiting.qsize() > 0:
                self.notify(2)
            elif self.femalesWaiting.qsize() > 1:
                self.notify(1)

    def notify(self, matchType):
        '''
        :param matchType: 0(both male)  1(both female) 2(opposite)
        :return:
        '''
        if matchType == 0:
            person1 = self.malesWaiting.get()
            person2 = self.malesWaiting.get()
        elif matchType == 1:
            person1 = self.femalesWaiting.get()
            person2 = self.femalesWaiting.get()
        else:
            person1 = self.femalesWaiting.get()
            person2 = self.malesWaiting.get()
        person1.returnId(person2.id)
        person2.returnId(person1.id)
        chat = Chat(person1, person2)
        chattingList[person1.id] = chat
        chattingList[person2.id] = chat
        print(person1.id, person2.id)


class MatchHandler(tornado.web.RequestHandler):


    @tornado.web.asynchronous
    def get(self):
        id = str(uuid4())
        while id in self.application.idSet:
            id = str(uuid4())
        self.application.idSet.add(id)
        sex = self.get_argument('sex')
        nameIndex = self.get_argument("nameIndex")
        person = Person(id, sex, nameIndex, self.returnId, self.application)
        self.application.waiter.match(person)

    def set_default_headers(self):
        # 跨域
        self.set_header('Access-Control-Allow-Origin', "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        #self.set_header('Access-Control-Allow-Credentials', "true")

    def returnId(self, id):
        self.write(json.dumps({'status': 1, 'id': id}))  #
        self.finish()


class ChatHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.id = self.get_argument("id")
        chattingList[self.id].register(self.id, self)

    def on_message(self, data):
        chattingList[self.id].recMessage(json.loads(data))

    def on_close(self):

        if self.id in chattingList.keys() and not chattingList[self.id].isClose:
            print("一方退出")
            chattingList[self.id].isClose = True
            chattingList[self.id].notifyClose(self.id)
            if chattingList[self.id].person1.id == self.id:
                anotherId = chattingList[self.id].person2.id
            else:
                anotherId = chattingList[self.id].person1.id
            self.application.idSet.remove(self.id)
            self.application.idSet.remove(anotherId)
            chattingList.pop(self.id)
            chattingList.pop(anotherId)

        else:
            print("另一方也退出")

    def check_origin(self, origin):
        return True

class OtherNameHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        # 跨域
        self.set_header('Access-Control-Allow-Origin', "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        #self.set_header('Access-Control-Allow-Credentials', "true")
    def get(self):
        id = self.get_argument("id")
        res = Result()
        if id in chattingList.keys():
            if id == chattingList[id].person1.id:
                self.write(json.dumps({'other':chattingList[id].person1.name,'mine':chattingList[id].person2.name,'status':1}))
            else:
                self.write(json.dumps({'other':chattingList[id].person2.name,'mine':chattingList[id].person1.name,'status':1}))

class NameHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        # 跨域
        self.set_header('Access-Control-Allow-Origin', "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        #self.set_header('Access-Control-Allow-Credentials', "true")
    def get(self):
        res = Result()
        names = {}
        sex = self.get_argument("sex")
        if sex == "0":
            # male
            for i in range(8):  # 一次返回8个名字
                index = random.randint(0, len(self.application.maleNames) - 1)
                while index in names.keys():
                    index = random.randint(0, len(self.application.maleNames) - 1)
                names[index] = self.application.maleNames[index]

        elif sex == "1":
            # female
            for i in range(8):  # 一次返回8个名字
                index = random.randint(0, len(self.application.femaleNames) - 1)
                while index in names.keys():
                    index = random.randint(0, len(self.application.femaleNames) - 1)
                names[index] = self.application.femaleNames[index]
        res.setData(names)
        self.write(res.getRes())






