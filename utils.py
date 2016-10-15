# coding=utf-8
import json
import tornado.web


class Result(object):
    def __init__(self):
        self.res = {"status" : 0, "data": None}
    def setData(self, data):
        self.res["data"] = data
        self.res["status"] = 1
    def getRes(self):
        return self.res