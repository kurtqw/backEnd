import re
import requests
from urllib.request import quote
from selenium import webdriver
from table import NewsTable
import configparser
import pymysql
from Spider.TopicSpider import baseSpider


class NeteaseNewsSpider(baseSpider):
    def __init__(self):
        baseSpider.__init__(self, 'Netease')

    def parse(self):
        url = 'http://news.163.com/latest/'
        self.driver.get(url)
        i = 1
        while i < 18:
            print(str(i))
            i += 1
            news_items = self.driver.find_elements_by_xpath(
                "//div[@id='instantPanel']/div[@class='cnt']/ul[@class='list_txt']/li/a[2]")
            for item in news_items:
                url = item.get_attribute("href")
                title = item.text
                print(url + '\t' + title)
                self.table.insert(url, title, 'news')
            self.driver.find_element_by_xpath("//div[@class='bar_pages']/a[@class='bar_pages_flip']").click()


if __name__ == '__main__':
    spider = NeteaseNewsSpider()
    spider.parse()
