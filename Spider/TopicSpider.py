import time
from selenium import webdriver
from table import NewsTable
import configparser
import pymysql


class baseSpider(object):
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
        self.table = NewsTable(self.conn, 'topicSpider', 1, False)

    def parse(self):
        pass

    def __del__(self):
        self.conn.commit()
        self.driver.close()


class SportSpider(baseSpider):  # 体育新闻爬虫
    def __init__(self):
        baseSpider.__init__(self)

    def parse(self):
        url = 'http://sports.ifeng.com/'
        self.driver.get(url)
        items = self.driver.find_elements_by_xpath(
            "/html/body//div[@class='col_01 pt01 clearfix']//div[@class='list06']//a")
        click_items = self.driver.find_elements_by_xpath("/html//div[@class='more02']/a")
        for item in click_items:
            item.click()
        for i, item in enumerate(items):
            if i < len(items) - 13:
                url = item.get_attribute("href")
                text = item.text
                if url is not None and text is not None:
                    self.table.insert(url, text, 'sport')
                    print(url + '\t' + text)


class MovieSpider(baseSpider):  # 电影新闻爬虫
    def __init__(self):
        baseSpider.__init__(self)

    def parse(self):
        url = 'http://ent.qq.com/movie/news_om.shtml'
        self.driver.get(url)
        i = 0
        while i < 5:
            items = self.driver.find_elements_by_xpath(
                "/html/body//div[@id='listZone']/div[@class='nrC']/h3/a[@class='newsTit']")
            for item in items:
                url = item.get_attribute("href")
                text = item.text
                self.table.insert(url, text, 'moive')
                print(url + '\t' + text)
            self.driver.find_element_by_xpath(
                "/html/body//div[@class='bd']/div[@id='pageZone']/span[@class='number']/a").click()
            time.sleep(5)
            i += 1


class GameSpider(baseSpider):  # 游戏新闻爬虫
    def __init__(self):
        baseSpider.__init__(self)

    def parse(self):
        url = 'http://play.163.com/'
        i = 1
        while i < 2:
            self.driver.get(url)
            height = self.driver.execute_script(
                "var h=document.documentElement.scrollHeight; window.scrollTo(0, h); return h;")
            print('height=   ' + str(height))
            items = self.driver.find_elements_by_xpath("//div[@id='Collist']/div[@class='m-collist']")
            for item in items:
                try:
                    url = item.find_element_by_xpath(".//a").get_attribute("href")
                    text = item.find_element_by_xpath(".//p").text
                    self.table.insert(url, text, 'game')
                    print(url + '\t' + text)
                except Exception as e:
                    pass
            i += 1


class TravelSpider(baseSpider):  # 旅行新闻爬虫
    def __init__(self):
        baseSpider.__init__(self)

    def parse(self):
        raw_url = 'http://chanyouji.com/?page=%d'
        i = 1
        while i < 360:
            url = raw_url % i
            self.driver.get(url)
            items = self.driver.find_elements_by_xpath(
                "//article[@class='trip-list-item']/div[@class='inner']")
            for item in items:
                url = item.find_element_by_xpath("./div[1]//a").get_attribute("href")
                text = item.find_element_by_xpath(".//h1").text
                self.table.insert(url, text, 'travel')
                print(url + '\t' + text)
            i += 1


class DBSpider(baseSpider):
    def __init__(self):
        baseSpider.__init__(self)

    def parse(self, raw_url, type):
        i = 0
        length = 0
        while i < 226:
            url = raw_url % i
            self.driver.get(url)
            items = self.driver.find_elements_by_xpath(
                "//div[@class='article']/div[@class='indent']/table/tbody//td/div[@class='pl2']/a")
            length += len(items)
            for item in items:
                url = item.get_attribute("href")
                text = item.text
                self.table.insert(url, text, type)
                print(url + '\t' + text)
            i += 25
        print(str(length))


if __name__ == '__main__':
    # sportSpider = SportSpider()
    # sportSpider.parse()
    # movieSpider = MovieSpider()
    # movieSpider.parse()
    # gameSpider = GameSpider()
    # gameSpider.parse()
    # travelSpider = TravelSpider()
    # travelSpider.parse()
    dbSpider = DBSpider()
    # dbSpider.parse(raw_url='https://music.douban.com/top250?start=%d', type='music')
    dbSpider.parse(raw_url='https://book.douban.com/top250?start=%d', type='library')
