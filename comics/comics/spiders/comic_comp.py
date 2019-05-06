# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from selenium import webdriver
import os
from time import time, sleep
import urllib
from scrapy.selector import Selector


class ComicCompSpider(scrapy.Spider):
    name = 'comic_comp'
    allowed_domains = ['www.js518.net']
    start_urls = ['http://www.js518.net/rexueshaonian/5923/']

    def __init__(self):
        # 'chromedriver.exe' been put in virtual environment root
        self.driver = webdriver.Chrome()

    def parse(self, response):
        tar_chapters = ['第6卷', '第85话', '第86话', '第87话']
        urls = [
            response.urljoin(
                response.xpath(
                    '//a[text()="{}"]/@href'.format(tc)
                ).extract_first())
            for tc in tar_chapters
        ]
        chapters = {}
        for i, c in enumerate(tar_chapters):
            chapters[c.replace('第', '')] = urls[i]

        for k, v in chapters.items():
            self.parse_chapter(url=v, chapter=k)

    def parse_chapter(self, url, chapter=None):
        if chapter and not os.path.exists('./output/{}'.format(chapter)):
            os.makedirs('./output/{}'.format(chapter))

        d = self.driver
        d.get(url)
        sel = Selector(text=d.page_source)

        tot_page_num = sel.xpath('//*[@id="k_total"]/text()').extract_first()
        cur_page_num = sel.xpath('//*[@id="k_page"]/text()').extract_first()

        while cur_page_num != tot_page_num:
            sel = Selector(text=d.page_source)
            cur_page_num = sel.xpath(
                '//*[@id="k_page"]/text()').extract_first()
            img_url = sel.xpath('//td/img/@src').extract_first()
            nxt_btn = d.find_element_by_xpath('//a[@id="k_next"]')
            self.parse_page(img_url, cur_page_num, chapter)
            nxt_btn.click()

    def parse_page(self, img_url, page, chapter):
        sleep(1)
        urllib.request.urlretrieve(
            url=img_url, filename='./output/{}/{}.jpg'.format(chapter, page))
