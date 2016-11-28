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
        url = 'http://www.qiushibaike.com/'
        self.driver.get(url)
        i = 1
        while i < 35:
            i += 1
            joke_items = self.driver.find_elements_by_xpath("//*[@id]/a[1]/div/span")
            for item in joke_items:
                self.table.insert(item.text)
            try:
                self.driver.find_element_by_xpath('//*[@id="content-left"]/ul/li[8]/a/span').click()
            except Exception as e:
                self.driver.save_screenshot('fuck.png')

    def __del__(self):
        self.conn.commit()
        self.driver.close()


if __name__ == '__main__':
    spider = NeteaseNewsSpider()
    spider.parse()
