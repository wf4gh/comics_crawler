# -*- coding: utf-8 -*-
import scrapy


class ComicCompSpider(scrapy.Spider):
    name = 'comic_comp'
    allowed_domains = ['www.js518.net']
    start_urls = ['http://www.js518.net/rexueshaonian/5923/']

    def parse(self, response):
        pass
