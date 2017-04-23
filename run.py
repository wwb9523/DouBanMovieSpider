#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/10/20 0020 17:25
# @Author  : Sz
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from news_spider.spiders.content_spider import ContentSpider

runner = CrawlerRunner()
runner.crawl(ContentSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run()
