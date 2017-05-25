#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from items import NewsSpiderItem,SnapshotItem,UrlItem,MovieSpiderItem
from function import LogError
from DBUnit import DBUnit
#from scrapy import log
#from Hbase import Hbase
import os,requests,re
import json
import logging
logger = logging.getLogger(__name__)

class NewsPipeline(object):
    def __init__(self):
        self.file = open('items.jl', 'wb')
        self.DB = DBUnit()
        print 'pipe'

    def process_item(self, item, spider):
        print 'process_item run'
        if isinstance(item,MovieSpiderItem):
            self.processMovieItem(item)
        elif isinstance(item, UrlItem):
            self.processUrl(item)
        return item

    def processMovieItem(self, item):
        print 'process Movie run'
        movId=self.DB.getMovIdBydouId(item['douId'])
        if movId and item['douId']:
            return
    #    self.writeJson(item)
        img=''
        if item['image']:
            img=self.downloadFile(item['image'])
        res = self.DB.insertMovie(int(item['douId']),item['title'],item['aka'],item['year'],item['length'],item['summary'],item['rating_num'],item['rating_people'],item['stars5'],item['stars4'],item['stars3'],item['stars2'],item['stars1'],img,item['image'])
        self.DB.db.commit()
        if res:
            movId=self.DB.getMovIdBydouId(item['douId'])
            if not movId:
                logger.warning('get movId false,douId:%s'%item['douId'])
                return
        else:
            logger.error('insert movie false,douId:'+str(item['douId']))
        self.insertPerson('writers_rela',item['writers'],movId)
        self.insertPerson('directors_rela', item['directors'], movId)
        self.insertPerson('casts_rela', item['casts'], movId)
        self.DB.insertCountries(item['countries'],movId)
        self.DB.insertGenres(item['genres'],movId)
        self.DB.insertLanguages(item['language'],movId)

    def processUrl(self,item):
        print 'processUrl run'
        url=item['url']
        start,type,statu=['0','T',0]
        pattern = re.compile('start=(\d+).*?type=(\w+)')
        res=pattern.findall(url)
        if res:
            if res[0][0]:
                start=res[0][0]
            if res[0][1]:
                type=res[0][1]
        if item['statu']:
            statu=item['statu']
        url=url.split('?')[0]
        if res or statu:
            #ul = pattern.sub(r'start=',url)
            self.DB.updateUrl(url,start,type,statu)
        else:
            self.DB.updateUrl(url, '0', "T",statu)


    def insertPerson(self,table,persons,movId=0):
        for person in persons:
            personId = self.DB.slctPersonIdByName(person)
            if not personId:
                res = self.DB.insertPerson(person)
                self.DB.db.commit()
                if not res:
                    logger.warning('insert person false,person:"%s"' % person)
                else:
                    personId = self.DB.slctPersonIdByName(person)
            if personId and movId:
                res = self.DB.insertRelation(table, personId, movId)
                if not res:
                    logger.warning(
                        'insert Ralation false,table:"%s",personId:%s,movId:%s' % ('writers', personId, movId))

    def writeJson(self,item):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)

    def insertMovie(self,douId, title, aka, year, length, summary, rating_num, rating_people, stars5, stars4, stars3,stars2, stars1):
        sql = 'insert into movie(douId,title,aka,year,length,summary,rating_num,' \
              'rating_people,stars5,stars4,stars3,stars2,stars1)' \
              'VALUES(%s,"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' \
              % (douId, title, aka, year, length, summary, rating_num, rating_people,
                 stars5, stars4, stars3, stars2, stars1)
        return self.DB.cursor.execute(sql)

    def downloadFile(self,url):
        name=url.split('/')[-1]
        path='W:/Python/news_spider1.0/pic/'+name
        content=requests.get(url).content
        if content:
            with open(path,'wb') as code:
                code.write(content)
            return path
        return ''






