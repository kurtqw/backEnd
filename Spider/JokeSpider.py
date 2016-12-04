import re
import requests
from urllib.request import quote
from selenium import webdriver
from Spider.table import JokeTable
import configparser
import pymysql
from Spider.TopicSpider import baseSpider


class JokeSpider(baseSpider):
    def __init__(self, name):
        baseSpider.__init__(self, name)

    def parse(self):
        self.table = JokeTable(self.conn, 'Joke', 1, False)
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
    spider = JokeSpider('qiushibaike')
    spider.parse()
