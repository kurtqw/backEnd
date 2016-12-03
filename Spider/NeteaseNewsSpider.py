import re
import requests
from urllib.request import quote
from selenium import webdriver
from table import NewsTable
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
        self.table = NewsTable(self.conn, 'Netease', 1, False)

    def parse(self):
        url = 'http://news.163.com/latest/'
        self.driver.get(url)
        i = 1
        while i < 18:
            i += 1
            news_items = self.driver.find_elements_by_xpath(
                "//div[@id='instantPanel']/div[@class='cnt']/ul[@class='list_txt']/li/a[2]")
            for item in news_items:
                url = item.get_attribute("href")
                title = item.text
                print(url + '\t' + title)
                self.table.insert(url, title, 'news')
            self.driver.find_element_by_xpath("//div[@class='bar_pages']/a[@class='bar_pages_flip']").click()

    def __del__(self):
        self.conn.commit()
        self.driver.close()


if __name__ == '__main__':
    spider = NeteaseNewsSpider()
    spider.parse()
