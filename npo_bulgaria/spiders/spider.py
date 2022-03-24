import re

import scrapy

from scrapy.loader import ItemLoader

from ..items import NpoBulgariaItem
from itemloaders.processors import TakeFirst


class NpoBulgariaSpider(scrapy.Spider):
    name = 'npo_bg'
    start_urls = [
        'https://www.ngobg.info/bg/organizations/%D1%81%D0%B4%D1%80%D1%83%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-3-1.html',
        'https://www.ngobg.info/bg/organizations/%D0%BA%D0%BB%D0%BE%D0%BD%D0%BE%D0%B2%D0%B5-%D0%BD%D0%B0-%D1%87%D1%83%D0%B6%D0%B4%D0%B5%D1%81%D1%82%D0%B0%D0%BD%D0%BD%D0%B8-%D0%BD%D0%BF%D0%BE-3-2.html',
        'https://www.ngobg.info/bg/organizations/%D0%BD%D0%B5%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D0%BB%D0%BD%D0%B8-%D0%B3%D1%80%D0%B0%D0%B6%D0%B4%D0%B0%D0%BD%D1%81%D0%BA%D0%B8-%D0%B3%D1%80%D1%83%D0%BF%D0%B8-3-3.html',
        'https://www.ngobg.info/bg/organizations/%D1%83%D1%87%D0%B8%D0%BB%D0%B8%D1%89%D0%BD%D0%B8-%D0%BD%D0%B0%D1%81%D1%82%D0%BE%D1%8F%D1%82%D0%B5%D0%BB%D1%81%D1%82%D0%B2%D0%B0-3-4.html',
        'https://www.ngobg.info/bg/organizations/%D1%87%D0%B8%D1%82%D0%B0%D0%BB%D0%B8%D1%89%D0%B0-3-5.html',
        'https://www.ngobg.info/bg/organizations/%D1%81%D0%B4%D1%80%D1%83%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-%D1%81%D0%BF%D0%BE%D1%80%D1%82%D0%BD%D0%B8-%D0%BA%D0%BB%D1%83%D0%B1%D0%BE%D0%B2%D0%B5-%D1%84%D0%B5%D0%B4%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D0%B8-3-6.html'
    ]

    def parse(self, response):
    #     kind_links = response.xpath('(//ul[@class="links"])[last()]//a/@href').getall()
    #     yield from response.follow_all(kind_links, self.parse_kind)
    #
    # def parse_kind(self, response):
        npo_links = response.xpath('//h4//a/@href').getall()
        yield from response.follow_all(npo_links, self.parse_data)

        next_page = response.xpath('(//div[@class="paging"]/a[@class="arrow"])[last()]/@href').getall()
        yield from response.follow_all(next_page, self.parse)

    def parse_data(self, response):
        title = response.xpath('//h4[@class="title"]/text()').get()
        kind = response.xpath('//div[@class="orgname"]/em/text()').get()
        domain = response.xpath('//div[@class="c3 p12"][span[text()="Интернет страница:"]]/a/@href').get()
        if not domain:
            domain = ''

        print(title, kind, domain, response.url)

        if not title:
            print('NPO: ', response.text)
        item = ItemLoader(item=NpoBulgariaItem(), response=response)
        item.default_output_processor = TakeFirst()
        item.add_value('title', title)
        item.add_value('kind', kind)
        item.add_value('domain', domain)
        item.add_value('url', response.url)

        yield item.load_item()
