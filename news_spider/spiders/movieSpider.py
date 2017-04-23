#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from scrapy import cmdline
from furl import furl
import re,os,sys,datetime,json
import time
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from news_spider.items import MovieSpiderItem
from news_spider.items import UrlItem
from news_spider.DBUnit import DBUnit

reload(sys)
sys.setdefaultencoding("utf-8")


class MovieSpider(CrawlSpider):
    name='movieSpider'

    allowed_domain=['douban.com']
    db = DBUnit()
    #rows = db.getUrl()
    rows=['https://movie.douban.com/tag/',
          ]
    url=[]
    cookie={
        'bid':'zmrKGEvLMkw',
        'gr_user_id':'0a7afdfd - 1b63 - 4899 - abe6 - 771b2c3674fc',
        'll':"108289",
        'viewed':"4828875_3288908_24703171",
        'ps':'y',
        'ap' : 1,
        'ue' : "48450976@qq.com",
        'dbcl2' : "159444618:vzET3x2tiaE",
        'ck' : 'CMVL_pk_ref.100001.8cb4 = % 5B % 22 % 22 % 2C % 22 % 22 % 2C1490260693 % 2C % 22https % 3\
        A % 2F % 2Faccounts.douban.com % 2Flogin % 22 % 5D',
        'push_noty_num' : 0,
        'push_doumail_num' :0,
        '_pk_id.100001.8cb4' : '4615bb76fa621e32.1478607450.7.1490261182.1490258760.',
        '_pk_ses.100001.8cb4' : '*',
        '__utma' : '30149280.1261062391.1478527591.1490258505.1490258583.18',
        '__utmb' : '30149280.6.10.1490258583',
        '__utmc' : '30149280',
        '__utmz' : '30149280.1490258583.18.10.utmcsr = baidu | utmccn = (organic) | utmcmd = organic',
        '__utmv' : '30149280.15944',
        '_vwo_uuid_v2' : '61DCE5169C3BD469097D2632928009A0 | 7d3c0bee4ff6dd33cbd594f0f69f5c5b'
    }
    heard={'Host':'movie.douban.com',
           'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
          # 'Cookie':'bid=zmrKGEvLMkw; gr_user_id=0a7afdfd-1b63-4899-abe6-771b2c3674fc; ll="108289"; viewed="4828875_3288908_24703171"; as="https://sec.douban.com/b?r=https%3A%2F%2Fmovie.douban.com%2F"; ps=y; dbcl2="158008010:F8uRm55Vyxw"; ck=-3uc; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1490095686%2C%22https%3A%2F%2Fopen.weixin.qq.com%2Fconnect%2Fqrconnect%3Fappid%3Dwxd9c1c6bbd5d59980%26redirect_uri%3Dhttps%253A%252F%252Fwww.douban.com%252Faccounts%252Fconnect%252Fwechat%252Fcallback%26response_type%3Dcode%26scope%3Dsnsapi_login%26state%3DzmrKGEvLMkw%252523None%252523https%25253A%252F%252Fmovie.douban.com%252F%22%5D; _pk_id.100001.4cf6=a30e38b6ddc03e2e.1483962832.11.1490095686.1490017745.; _pk_ses.100001.4cf6=*; __utma=30149280.1261062391.1478527591.1490017325.1490095686.13; __utmb=30149280.0.10.1490095686; __utmc=30149280; __utmz=30149280.1490095686.13.7.utmcsr=open.weixin.qq.com|utmccn=(referral)|utmcmd=referral|utmcct=/connect/qrconnect; __utma=223695111.395625854.1483962832.1490017325.1490095686.11; __utmb=223695111.0.10.1490095686; __utmc=223695111; __utmz=223695111.1490095686.11.5.utmcsr=open.weixin.qq.com|utmccn=(referral)|utmcmd=referral|utmcct=/connect/qrconnect; push_noty_num=0; push_doumail_num=0; _vwo_uuid_v2=61DCE5169C3BD469097D2632928009A0|7d3c0bee4ff6dd33cbd594f0f69f5c5b; ap=1',
          #  'Upgrade-Insecure-Requests':1,
         #  'Connection': 'keep - alive'
           }
   # href='https://movie.douban.com/subject/:id'
    # info='v2/movie/subject/:id'
    # photo='/v2/movie/subject/:id/photos'
    # reviews='/v2/movie/subject/:id/reviews'
    # comments='/v2/movie/subject/:id/comments'
    #ws=['id','title','original_title','year','summary']

    def start_requests(self):
        print 'movieSpider start!'
        self.url=self.db.getUrl()
        for url in self.url:
           # time.sleep(2)
            url=url.strip()
            if len(url.split('tag'))>1 and url.split('tag')[1].encode('utf-8').startswith('?'):
                yield Request(url,callback=self.parse_tag,headers=self.heard,cookies=self.cookie)
            elif len(url.split('tag/'))>1:
                yield Request(url, callback=self.parse0, headers=self.heard,cookies=self.cookie)
            elif 'subject' in url:
                yield Request(url, callback=self.parse1, headers=self.heard,cookies=self.cookie)
        # for row in self.rows:
        #     yield Request(row,callback=self.parse_tag,headers=self.heard)

    def parse_tag(self, response):
        print(response.url)
        selector=Selector(response)
        urls=selector.xpath('//div[@class="article"]/table[@class="tagCol"]').css('a::attr(href)').extract()
        i=0
        for url in urls:
            if 'https://movie.douban.com'+url.strip() in self.url:
                continue
            else:
                i=i+1
              #  time.sleep(2)
                yield Request('https://movie.douban.com'+url.strip(),callback=self.parse0,headers=self.heard,cookies=self.cookie)
        if i==0:
            urlItem=UrlItem({'url':'','statu':1})
            urlItem['url']=response.url
            urlItem.statu=1
            yield urlItem


    def parse0(self,response):
      #  print 'parse0 run'
        urlItem = UrlItem({'url':'','statu':0})
        urlItem['url'] = response.url
        print(response.url)
        yield urlItem
        selector = Selector(response)
        urls=selector.css('a[class=nbg]::attr(href)').extract()
        nextUrl=selector.xpath('//span[@class="next"]').css('a::attr(href)').extract()
        for url in urls:
            if url:
                id=url.strip('/').split('/')[-1]
                isExist=self.db.getMovIdBydouId(id)
                if not isExist:
                    yield Request(url,callback=self.parse1,headers=self.heard,cookies=self.cookie)
        if nextUrl and nextUrl[0].startswith('http'):
            yield Request(nextUrl[0],callback=self.parse0,headers=self.heard,cookies=self.cookie)
        else:
            urlItem['statu']=1
            yield urlItem



    def parse1(self,response):
    #    print 'parse1 run'
        movieItem = MovieSpiderItem({'aka': '','length':'','language':'', 'countries': '','image':'',
                                     'year':'','summary':'','rating_num':'','rating_people':'',
                                     'stars5':'','stars4':'','stars3':'','stars2':'','stars1':'',
                                     'genres': {},'directors':[],'writers':[],'casts':[]})
        url=response.url
        print(url)
        pattern=re.compile(r'subject/(\d+)/')
        res=pattern.findall(url)
        if res:
            movieItem['douId']=int(res[0])
        selector = Selector(response)
        head=selector.xpath('body/div[@id="wrapper"]/div[@id="content"]/h1/span/text()').extract()
        if head:
            movieItem['title']=head[0]
        if len(head)>1:
            movieItem['year']=head[1].strip('(').strip(')')
       # directors = selector.xpath('body/div[@id="wrapper"]/div[@id="content"]/div[@id="info"]/span[@class="attrs"]/text()').extract()
        descps=selector.xpath('body/div[@id="wrapper"]/div[@id="content"]//div[@id="link-report"]/span/text()').extract()
        spans=selector.xpath('body/div[@id="wrapper"]/div[@id="content"]//div[@id="info"]/span')
        vls=selector.xpath('body/div[@id="wrapper"]/div[@id="content"]//div[@id="info"]/node()').extract()
        # movieItem['directors']=[]
        # movieItem['writers']=[]
        # movieItem['casts']=[]
        st=''
        for desc in descps:
            st+=desc
        img=selector.xpath('//div[@id="mainpic"]/a/img/@src').extract()
        if img:
            movieItem['image'] = img[0]
        movieItem['summary']=st.replace('  ','').replace('\n','').replace('\t','').replace('\r','').encode('utf-8').strip()
        for i in range(len(spans)):
            if i<3:
                vals = spans[i].xpath('./span/a/text()').extract()
                for val in vals:
                    if i==0:
                        movieItem['directors'].append(val)
                    elif i==1:
                        movieItem['writers'].append(val)
                    elif i==2:
                        movieItem['casts'].append(val)
                        continue
        str=''
        for vl in vls:
            str=str+vl
        str=str.replace(' ','').replace('\n','').replace('\t','').replace('\r','').encode('utf-8')
        word={'countries':'制片国家','language':'语言','length':'片长','aka':'又名','genres':'类型'}
        for w in word:
            s=word[w]+r'[\s\S]+?>([^>]+?)<'
            pattern = re.compile(s)
            res=pattern.findall(str)
            if res:
                if w=='aka' or w=='length':
                    movieItem[w]=res[0]
                else:
                    movieItem[w]=res[0].split('/')
        sect1=selector.xpath('//div[@id="interest_sectl"]').extract()[0].replace(' ','').replace('\n','').replace('\t','').replace('\r','').encode('utf-8')
        ws={'rating_num':'豆瓣评分','rating_people':'rating_people','stars5':'5星','stars4':'4星','stars3':'3星','stars2':'2星','stars1':'1星'}
        for w in ws:
            s=ws[w]+r'[\s\S]+?(\d[^<>\s]+?)</'
            pattern = re.compile(s)
            res = pattern.findall(sect1)
            if res:
                movieItem[w] = res[0]
        yield movieItem

        # res=response.body
        # data=json.loads(res)
        # for w in self.ws:
        #     movieItem[w]=data[w]
        # for aka in data['aka']:
        #     movieItem['aka']+=aka+'&'
        # for casts in data['casts']:
        #     movieItem['casts']+=casts['name']+'&'
        # for countries in data['countries']:
        #     movieItem['countries']+=countries+'&'
        # for genres in data['genres']:
        #     movieItem['genres'] += genres+'&'
        # movieItem['rating']=data['rating']['average']
        # movieItem['directors']=data['directors']['name']
        # movieItem['writers']=data['writers']['name']
        # print movieItem

if __name__=='__main__':
    cmdline.execute("scrapy crawl movieSpider".split())


