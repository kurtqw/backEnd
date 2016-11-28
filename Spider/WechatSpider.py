import re
import requests
from urllib.request import quote
from selenium import webdriver
from table import NewsTable
import configparser
import pymysql


# http://mp.weixin.qq.com/profile?src=3&timestamp=1475665736&ver=1&signature=*7aQj9NeKS4m4A8BoR4bkYSP6Vpc-7ao55D*-PXE2AOE55o10iEc1U*5ah5dCLO58Cl362EC2*cJzV1vZX4inQ==


class WechatNewsSpider(object):
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
        self.driver = webdriver.Chrome('/home/wqlin/PycharmProjects/chromedriver')
        self.table = NewsTable(self.conn, 'Wechat', 1, False)

    def parse(self, OA_name):
        request_url = 'http://weixin.sogou.com/weixin?query=' + quote(
            OA_name) + '&_sug_type_=&_sug_=n&type=1' + '&ie=utf8'
        self.driver.get(request_url)
        OA_url = self.driver.find_element_by_xpath('//*[@id="sogou_vr_11002301_box_0"]').get_attribute('href')
        self.driver.get(OA_url)
        items = self.driver.find_elements_by_tag_name('h4')
        for item in items:
            arg = []
            title = item.text
            url = 'http://mp.weixin.qq.com' + item.get_attribute('hrefs')
            arg.append(title.encode('utf-8'))
            arg.append(url)
            self.table.insert(url, title)

        self.conn.commit()

    def __del__(self):
        self.conn.commit()


if __name__ == '__main__':
    spider = WechatNewsSpider()
    spider.parse(u'华工微博协会')

"""
if __name__ == '__main__':
    url = 'http://mp.weixin.qq.com/profile?src=3&timestamp=1475647528&ver=1&signature=*7aQj9NeKS4m4A8BoR4bkYSP6Vpc-7ao55D*-PXE2AOE55o10iEc1U*5ah5dCLO5jvdmHM8ohFvNQ81un9hDgg=='
    res = requests.get(url).text
    bizRe = re.compile(r'var biz = \"(.*)\" \|\| ')
    srcRe = re.compile(r'var src = \"(\d+)\" ;')
    verRe = re.compile(r'var ver = \"(\d+)\" ;')
    timestampRe = re.compile(r'var signature = \"(.+)\" ;')
    print(bizRe.findall(res))
    print(srcRe.findall(res))
    print(verRe.findall(res))
    print(timestampRe.findall(res))
"""
