import re
import requests
from urllib.request import quote
from selenium import webdriver
from Spider.table import JokeTable
import configparser
import pymysql


class NeteaseNewsSpider(object):
    def __init__(self):
        parser = configparser.ConfigParser()
        parser.read('mysql.ini')
        parser.read('mysql.ini')
        host = parser['CONFIG']['HOST']
        username = parser['CONFIG']['USERNAME']
        password = parser['CONFIG']['PASSWORD']
        db = parser['CONFIG']['DB']
        self.conn = pymysql.connect(host, username, password, db, charset='utf8')
        self.cur = self.conn.cursor()
        self.driver = webdriver.PhantomJS()
        self.table = JokeTable(self.conn, 'qiushibaike', 1, False)

    def parse(self):
        url = 'http://www.qiushibaike.com/text/page/%d/?s=4934451'
        i = 1
        while i < 36:
            joke_url = url % i
            self.driver.get(joke_url)
            print(joke_url)
            joke_items = self.driver.find_elements_by_xpath("//*[@id]/a[1]/div/span")
            for item in joke_items:
                self.table.insert(item.text)
            i += 1

    def __del__(self):
        self.conn.commit()
        self.driver.close()


if __name__ == '__main__':
    spider = NeteaseNewsSpider()
    spider.parse()
