# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from scrapy import Request
import time


class ComicSpider(scrapy.Spider):
    name = 'comic'
    allowed_domains = ['www.36mh.com']
    

    def start_requests(self):
        self.driver = webdriver.Chrome()


    def parse(self, response):
        self.driver.get('https://www.36mh.com/manhua/heijiao/70245.html')

        sel = Selector(text=self.driver.page_source)
        start_time = time.time()
        while not sel.xpath('//*[@id="imgLoading"]/@style').extract():
            time.sleep(1)
            sel = Selector(text=self.driver.page_source)
            if time.time() - start_time > 5:
                raise Exception('Failed to get image ~ !')

        print('----------------------------')
        print(sel.xpath('//*[@id="imgLoading"]'))
        print(sel.xpath('//*[@id="imgLoading"]/@style').extract())
        print(sel.xpath('//*[@id="images"]/img/@src').extract())
        print('----------------------------')

        yield Request('https://www.36mh.com/manhua/heijiao/70245.html', callback=self.parse_chapter)

    def parse_chapter(self, response):
        pass
    
    def parse_page(self, response):
        pass
