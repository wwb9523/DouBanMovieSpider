#!/usr/bin/env/python
# -*- coding: utf-8 -*-
import MySQLdb,sys,re
import time
from function import LogError
reload(sys)
import logging
logger = logging.getLogger(__name__)
sys.setdefaultencoding("utf-8")

class DBUnit(object):
    def __init__(self):
        self.db = MySQLdb.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='',
            db='recom',
            charset='utf8'
        )
        self.cursor = self.db.cursor()

    def slctRelation(self,table,personId=0,movId=0):
        if personId:
            sql='select movId from '+table+' where personId =%s'%personId
        elif movId:
            sql = 'select personId from ' + table + ' where movId =%s' % movId
        else:
            return None
        self.cursor.execute(sql)
        res=self.cursor.fetchall()
        if res:
            return res[0][0]
        else:
            return None

    def insertRelation(self,table,personId,movId):
        sql='insert into '+table+'(movId,personId) values(%s,%s)'%(movId,personId)
        res=self.cursor.execute(sql)
        if not res:
            logger.error('error sql:"%s"' % sql)
        return res

    def slctPersonIdByName(self,name):
        sql='select id from person where name ="%s"'%MySQLdb.escape_string(name)
        self.cursor.execute(sql)
        res=self.cursor.fetchall()
        if res:
            return res[0][0]
        else:
            return None


    def insertPerson(self,name):
        sql = 'insert into person(name) VALUES("%s")'%MySQLdb.escape_string(name)
        res=self.cursor.execute(sql)
        if not res:
            logger.error('error sql:"%s"' % sql)
        return res

    def insertMovie(self,douId,title,aka,year,length,summary,rating_num,rating_people,stars5,stars4,stars3,stars2,stars1,image):
        sql = 'insert into movie(douId,title,aka,year,length,summary,rating_num,' \
              'rating_people,stars5,stars4,stars3,stars2,stars1,image)' \
            'VALUES(%s,"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'\
            %(douId,MySQLdb.escape_string(title),MySQLdb.escape_string(aka),year,length,MySQLdb.escape_string(summary),rating_num,rating_people,
              stars5,stars4,stars3,stars2,stars1,image)
        res=self.cursor.execute(sql)
        if not res:
            logger.error('error sql:"%s"' % sql)
        return res

    def getCountryId(self,countryName):
        sql='select id from countries where name="%s"'%countryName
        self.cursor.execute(sql)
        res=self.cursor.fetchall()
        if res:
            return res[0][0]
        return None

    def insertCountries(self,countries,movId):
        for country in countries:
            countryId=self.getCountryId(country)
            if not countryId:
                sql='insert into countries(name) VALUES("%s")'%country
                res=self.cursor.execute(sql)
                if not res:
                    logger.error('error sql:"%s"' % sql)
                self.db.commit()
                countryId = self.getCountryId(country)
            if countryId and movId:
                sql='insert into country_mov(movId,countryId) VALUES(%s,%s)'%(movId,countryId)
                res=self.cursor.execute(sql)
                if not res:
                    logger.error('error sql:"%s"' % sql)

    def getGenresId(self,genres):
        sql='select id from genres where name="%s"'%MySQLdb.escape_string(genres)
        self.cursor.execute(sql)
        res=self.cursor.fetchall()
        if res:
            return res[0][0]
        return None


    def insertGenres(self,genres,movId=0):
        for gen in genres:
            genresId=self.getGenresId(gen)
            if not genresId:
                sql='insert into genres(name) VALUES("%s")'%gen
                res=self.cursor.execute(sql)
                if not res:
                    logger.error('error sql:"%s"' % sql)
                self.db.commit()
                genresId=self.getGenresId(gen)
            if genresId and movId:
                sql='insert into genres_mov(genresId,movId) VALUES(%s,%s)'%(genresId,movId)
                res=self.cursor.execute(sql)
                if not res:
                    logger.error('error sql:"%s"' % sql)

    def getLanguageId(self,language):
        sql='select id from language where name="%s"'%language
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        if res:
            return res[0][0]
        return None

    def insertLanguages(self,languages,movId=0):
        for language in languages:
            langId=self.getLanguageId(language)
            if not langId:
                sql='insert into language(name) VALUES("%s")'%language
                res=self.cursor.execute(sql)
                if not res:
                    logger.error('error sql:"%s"' % sql)
                self.db.commit()
                langId=self.getLanguageId(language)
            if langId and movId:
                sql='insert into lang_mov(languageId,movId) VALUES(%s,%s)'%(langId,movId)
                res=self.cursor.execute(sql)
                if not res:
                    logger.error('error sql:"%s"' % sql)


    def getMovIdBydouId(self,douId):
        sql='select id from movie where douId=%s'%douId
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        if res:
            return res[0][0]
        else:
            return None

    def updateUrl(self,url,start="0",type="T",statu=0):
        sql='select id,url,start,type from url where url="%s"'%url
        self.cursor.execute(sql)
        res=self.cursor.fetchall()
        if res:
            sql='update url set start="%s" , type="%s" , statu=%s where id=%s'%(start,type,statu,res[0][0])
            return self.cursor.execute(sql)
        else:
            sql='insert into url(url,start,type) VALUES("%s","%s","%s")'%(url,start,type)
            return self.cursor.execute(sql)

    def getUrl(self):
        sql='select url,start,type from url where statu=0'
        self.cursor.execute(sql)
        res=self.cursor.fetchall()
        if res:
            list=[]
            for row in res:
                url=row[0]+'?start='+row[1]+'&type='+row[2]
                list.append(url)
            return list
        else:
            return None



