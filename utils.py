# coding=utf-8
import json
import tornado.web


class Result(object):
    def __init__(self):
        self.res = {"status" : 0, "res": None}
    def setData(self, data):
        self.res["res"] = data
        self.res["status"] = 1
    def getRes(self):
        return self.res
