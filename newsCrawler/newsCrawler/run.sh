#!/usr/bin/env bash
#sudo docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash
rm -f test.log
scrapy crawl rumor