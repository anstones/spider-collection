# -*- coding: utf-8 -*-
from scrapy.selector import Selector
import scrapy
from scrapy.contrib.loader import ItemLoader
from Coser.items import CoserItem


class CoserSpider(scrapy.Spider):
    name = "coser"
    allowed_domains = ["bcy.net"]
    start_urls = (
        'http://bcy.net/cn125101',
        'http://bcy.net/cn126487',
        'http://bcy.net/cn126173'
    )

    def parse(self, response):
        sel = Selector(response)

        for link in sel.xpath("//ul[@class='js-articles l-works']/li[@class='l-work--big']/article[@class='work work--second-created']/h2[@class='work__title']/a/@href").extract():
            link = 'http://bcy.net%s' % link
            request = scrapy.Request(link, callback=self.parse_item)
            yield request

    def parse_item(self, response):
        item = ItemLoader(item=CoserItem(), response=response)
        item.add_xpath('name', "//h1[@class='js-post-title']/text()")
        item.add_xpath('info', "//div[@class='post__info']/div[@class='post__type post__info-group']/span/text()")
        urls = item.get_xpath('//img[@class="detail_std detail_clickable"]/@src')
        urls = [url.replace('/w650', '') for url in urls]
        item.add_value('image_urls', urls)
        item.add_value('url', response.url)

        return item.load_item()
