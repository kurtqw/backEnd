# coding=utf-8
import time
import json
import random
from uuid import uuid4

from utils import Result
from chat import Message

import tornado.httpclient
import tornado.websocket
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

GROUP_CHAT_RECORD_SIZE = 20


class GroupChatHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.topic = self.get_argument("topic")
        if self.topic not in ["体育", "电影", "音乐", "游戏", "唱K", "泡馆"]:
            #若不在设定主题内 则断开连接
            self.close()
        if self.topic not in self.application.groupChats.keys():
            self.application.groupChats[self.topic] = GroupChat(self.topic)

        # id
        self.id = str(uuid4())
        while self.id in self.application.groupIdSet:
            self.id = str(uuid4())
        self.application.groupIdSet.add(self.id)

        #昵称
        index = random.randint(0, len(self.application.allNames) - 1)
        while self.application.allnames[index]  in self.application.groupChats[self.topic].names:
            index = random.randint(0, len(self.application.allNames) - 1)
        self.name = self.application.allnames[index]
        self.application.groupChats[self.topic].names.add(self.name)

        #在GroupChat的people dict 中保存与id对应的write_message
        self.application.groupChats[self.topic].people[self.id] = self.write_message

        #返回用户的ID， 名字
        self.write_message(json.dumps({'status': 1, 'id': self.id, 'name': self.name}))

        #将该话题下原先的近20条记录发给用户
        for record in self.application[self.topic].records:
            self.write_message(record)

    def on_message(self, data):
        message = Message(sender=self.name, data=data)

        #将消息发送给每个在群组里的人
        for key in self.application.groupChats[self.topic].people.keys():
            if key != self.id:
                self.application.groupChats[self.topic].people[key](message.response())

        #将消息存入消息记录
        if len(self.application.groupChats[self.topic].records) > GROUP_CHAT_RECORD_SIZE:
            self.application.groupChats[self.topic].records.pop()
        self.application.groupChats[self.topic].records.insert(0, message.response())


    def on_close(self):
        #将自己从people中删去
        self.application.groupChats[self.topic].people.pop(self.id)
        self.application.groupChats[self.topic].names.remove(self.name)


class GroupChat(object):
    def __init__(self, topic):
        self.topic = topic

        #{ {"res":{"sender":"xxx","type":"xxx","content":"","time":"2016-10-16  13:45:20"},"status":1},\
        #  ..}
        self.records = []


        self.names = set()

        #{id1 : write_message1, id2 : write_message2...}
        self.people = {}


