# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsSpiderItem(scrapy.Item):
    url=scrapy.Field()
    title=scrapy.Field()
    content=scrapy.Field()
    time=scrapy.Field()
    description=scrapy.Field()

class SnapshotItem(scrapy.Item):
    link = scrapy.Field()
    html = scrapy.Field()
    url = scrapy.Field()

class UrlSpiderItem(scrapy.Item):
    urls=scrapy.Field()
    id=scrapy.Field()

class MovieSpiderItem(scrapy.Item):
    id=scrapy.Field()
    douId=scrapy.Field()
    title=scrapy.Field()
    language=scrapy.Field()
    length=scrapy.Field()
    aka=scrapy.Field()
    directors=scrapy.Field()
    casts=scrapy.Field()
    writers=scrapy.Field()
    year=scrapy.Field()
    genres=scrapy.Field()
    countries=scrapy.Field()
    summary=scrapy.Field()
    rating_num=scrapy.Field()
    rating_people=scrapy.Field()
    stars5=scrapy.Field()
    stars4=scrapy.Field()
    stars3=scrapy.Field()
    stars2=scrapy.Field()
    stars1=scrapy.Field()
    image=scrapy.Field()

class UrlItem(scrapy.Item):
    url=scrapy.Field()
    statu=scrapy.Field()