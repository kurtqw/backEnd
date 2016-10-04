from scrapy.spiders import Spider
from scrapy import Request
from scrapy.loader import ItemLoader
from newsCrawler.items import NewsItem
from scrapy.linkextractors import LinkExtractor
from datetime import datetime
from scrapy_splash import SplashRequest


class TencentNews(Spider):
    name = 'netease'
    start_urls = ['http://news.163.com/rank/', 'http://news.163.com', 'http://news.163.com/domestic/',
                  'http://news.163.com/world/',
                  'http://news.163.com/shehui/', 'http://gd.news.163.com/']
    allowed_domains = ['news.163.com']
    now = datetime.now()
    news_url_pattern = [r'http://news.163.com/16/10\d+/\d+/.*']
    news_extractor = LinkExtractor(allow=news_url_pattern)

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        for link in self.news_extractor.extract_links(response):
            yield SplashRequest(link.url, callback=self.parse_item, args={'wait': 0.5})

    def parse_item(self, response):
        print(response.url)
        news = ItemLoader(item=NewsItem(), response=response)
        news.add_value('url', response.url)
        news.add_xpath('title', '//head/title/text()')
        news.add_xpath('type', '//div[@class="post_crumb"]/a[3]/text()')
        yield news.load_item()

        for link in self.news_extractor.extract_links(response):
            yield SplashRequest(link.url, callback=self.parse_item, args={'wait': 0.5})
