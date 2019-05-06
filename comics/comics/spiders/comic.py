# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from scrapy import Request
from time import time, sleep
import urllib
import os


class ComicSpider(scrapy.Spider):
    name = 'comic'
    # comic incomplete, need to be crawled from two sites. crawl volume 1-5,7, chapter 56-84,88-101 from this site
    allowed_domains = ['www.36mh.com']
    start_urls = ['https://www.36mh.com/manhua/heijiao/']

    def __init__(self):
        # 'chromedriver.exe' been put in virtual environment root
        self.driver = webdriver.Chrome()

    # parse catalog here
    def parse(self, response):
        chapters = response.xpath('//ul[@id="chapter-list-4"]/li')
        tar_chapters = list(range(1, 6)) + \
            [7] + list(range(56, 85)) + list(range(88, 102))
        tar_chapters = {str(vc) + '话': None for vc in tar_chapters}

        # get a dict with chapters as keys and URLs as values
        for k in tar_chapters.keys():
            for c in chapters:
                if k in c.xpath('./a/span/text()').extract_first():
                    tar_chapters[k] = response.urljoin(
                        c.xpath('./a/@href').extract_first())
                    break

        for k, v in tar_chapters.items():
            self.parse_chapter(url=v, chapter=k)

    def parse_chapter(self, url, chapter=None):
        if chapter and not os.path.exists('./output/{}'.format(chapter)):
            os.makedirs('./output/{}'.format(chapter))

        d = self.driver
        d.get(url)
        sel = Selector(text=d.page_source)

        # wait for image loading. will have style="display: none;" if image loaded.
        # start_time = time()
        # while not sel.xpath('//*[@id="imgLoading"]/@style').extract():
        #     sleep(1)
        #     sel = Selector(text=d.page_source)
        #     if time() - start_time > 5:
        #         raise Exception(
        #             'Failed to get image at chapter: {}, with url: {}'.format(chapter, url))

        total_page_num = sel.xpath(
            '//h1/following-sibling::span/text()'
        ).extract()[1][1:-1]
        cur_page_num = sel.xpath(
            '//h1/following-sibling::span/span/text()'
        ).extract_first()

        while total_page_num != cur_page_num:
            sel = Selector(text=d.page_source)

            # wait for image loading. will have style="display: none;" if image loaded.
            # start_time = time()
            # while not sel.xpath('//*[@id="imgLoading"]/@style').extract():
            #     sleep(1)
            #     sel = Selector(text=d.page_source)
            #     if time() - start_time > 5:
            #         raise Exception(
            #             'Failed to get image at chapter: {}, with url: {}'.format(chapter, url))

            cur_page_num = sel.xpath(
                '//h1/following-sibling::span/span/text()').extract_first()
            img_url = sel.xpath('//*[@id="images"]/img/@src').extract_first()
            nxt_page_btn = d.find_element_by_class_name("nextPage")
            self.parse_page(img_url, cur_page_num, chapter)
            nxt_page_btn.click()

    def parse_page(self, img_url, page, chapter):
        sleep(1)
        urllib.request.urlretrieve(
            url=img_url, filename='./output/{}/{}.jpg'.format(chapter, page))
