# -*- coding: utf-8 -*-

# Scrapy settings for newsCrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'newsCrawler'

SPIDER_MODULES = ['newsCrawler.spiders']
NEWSPIDER_MODULE = 'newsCrawler.spiders'

# USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'

ROBOTSTXT_OBEY = True
LOG_FILE = 'test.log'
LOG_LEVEL = 'INFO'

CONCURRENT_REQUESTS = 100

DOWNLOAD_DELAY = 0.5
RANDOMIZE_DOWNLOAD_DELAY = True

CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

DEPTH_LIMIT = 0
COOKIES_ENABLED = False

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #   'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'
}

ITEM_PIPELINES = {
    'newsCrawler.pipelines.NewsCheckPipeline': 300,
    #'newsCrawler.pipelines.NewsEncodePipeline': 400,
    'newsCrawler.pipelines.MySQLPipeline': 500
}

AUTOTHROTTLE_START_DELAY = 0.5
AUTOTHROTTLE_MAX_DELAY = 5

HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 30
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []

# Scrapy-Splash setting
SPLASH_URL = 'http://127.0.0.1:8050'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

# MYSQL_HOST = '119.29.161.184'
MYSQL_HOST = '0.0.0.0'
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DB = 'townmeet1'
