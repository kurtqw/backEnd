import pymysql
from scrapy.exceptions import DropItem
from newsCrawler.items import NewsItem
from newsCrawler.table import NewsTable


class NewsCheckPipeline(object):
    def process_item(self, item, spider):
        for key in item:
            if item[key] is None:
                raise DropItem('%s missing %s' % (item, key))
        return item


class NewsEncodePipeline(object):
    def process_item(self, item, spider):
        item['url'] = item['url'].encode('UTF-8')
        item['title'] = item['title'].encode('UTF-8')
        item['type'] = item['type'].encode('UTF-8')
        return item


class MySQLPipeline(object):
    def __init__(self, host, username, password, db):
        self.conn = None
        self.newsTable = None
        self.host = host
        self.username = username
        self.password = password
        self.db = db

    @classmethod
    def from_settings(cls, settings):
        host = settings['MYSQL_HOST']
        username = settings['MYSQL_USERNAME']
        password = settings['MYSQL_PASSWORD']
        db = settings['MYSQL_DB']
        return cls(host, username, password, db)

    def process_item(self, item, spider):
        self.newsTable.insert(item['url'], item['title'], item['type'])
        return item

    def open_spider(self, spider):
        self.conn = pymysql.connect(self.host, self.username, self.password, self.db, charset='utf8')
        self.newsTable = NewsTable(conn=self.conn, spider_name=spider.name, cache_size=100, is_created=False)

    def close_spider(self, spider):
        self.newsTable.flush()
        self.conn.close()
