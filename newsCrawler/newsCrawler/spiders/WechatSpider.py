from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from scrapy.linkextractors import LinkExtractor
from newsCrawler.items import NewsItem
from scrapy import Request
from .agent import agent
import random
from scrapy.selector import Selector


class WechatNews(Spider):
    name = 'rumor'
    headers = {
        'User-Agent': agent[random.randint(0, len(agent) - 1)],
        'Referer': 'http://weixin.sogou.com/',
        'Host': 'weixin.sogou.com'
    }
    start_urls = ['http://mp.weixin.qq.com/profile?src=3&timestamp=1475658039&ver=1&signature=*7aQj9NeKS4m4A8BoR4bkYSP6Vpc-7ao55D*-PXE2AOE55o10iEc1U*5ah5dCLO5nr03np1LilFu9laJNTIp5g==']

    allowed_domains = ['weixin.qq.com']
    news_url_pattern = [r'http://mp.weixin.qq.com/s?timestamp=\d+&src=\d*&ver=\d*&signature=.*']
    news_extractor = LinkExtractor(allow=news_url_pattern)

    def start_requests(self):
        for url in self.start_urls:
            print(url)
            yield SplashRequest(url, self.parse, headers=self.headers, args={'wait': 50.0})

    def parse(self, response):
        print(response.url)
        if u'用户您好，您的访问过于频繁，为确认本次访问为正常用户行为，需要您协助验证' in response.body:
            print(response.body)
        else:
            hxs = Selector(response)
            news_urls = hxs.xpath(
                "//div[@id='history']/div[@class='weui_msg_card']//div[@class='weui_media_bd']/h4/@hrefs")
            news_titles = hxs.xpath(
                "//div[@id='history']/div[@class='weui_msg_card']//div[@class='weui_media_bd']/h4/text()")
            assert (len(news_urls) == len(news_titles))
            for (t, u) in zip(news_titles, news_urls):
                item = dict()
                item['url'] = u
                item['title'] = t
                yield NewsItem(item)
