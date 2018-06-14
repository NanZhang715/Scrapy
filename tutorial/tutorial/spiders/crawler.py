import scrapy
from tutorial.items import TutorialItem
import sqlite3
import os


con = None


class nzhangSpider(scrapy.Spider):
    name = 'nzhang'

    def __init__(self):
        self.con = sqlite3.connect(os.getcwd() + '/test.db')
        self.cur = self.con.cursor()
        self.start_requests()

    def start_requests(self):
        sql = 'select url from crawl'
        self.cur.execute(sql)
        start_urls = [url[0] for url in self.cur.fetchall()]  # 列表生成器将 tuple 转换成 list

        # start_urls = ['http://114.jxhz.com']
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        item = TutorialItem()

        item['title'] = response.xpath('//title/text()').extract()
        item['keywords'] = response.xpath("//meta[@name='keywords']/@content")[0].extract()
        item['description'] = response.xpath("//meta[@name='description']/@content")[0].extract()
        item['url'] = response.url
        item['unicode'] = response.body_as_unicode().strip()

        yield item



