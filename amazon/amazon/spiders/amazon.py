# -*- coding: utf-8 -*-
import scrapy
from Amazon.items import AmazonItem


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']
    start_urls = ['https://www.amazon.cn/gp/book/all_category/ref=sv_b_1']

    def parse(self, response):
        node_list = response.xpath('//div[@class="a-column a-span9 a-text-center"]/table/tr/td')
        temp = {}
        for node in node_list[0:1]:
            temp['samll_cate'] = node.xpath('./a/@title').extract_first()
            temp['samll_cate_link'] = node.xpath('./a/@href').extract_first()

            yield scrapy.Request(temp['samll_cate_link'],callback=self.parse_book_list,meta={'type':temp['samll_cate']})

    def parse_book_list(self, response):
        node_list = response.xpath('//div[@id="search-results"]/div[2]/ul/li|//div[@id="centerMinus"]/div/ul/li')
        for node in node_list:
            item = AmazonItem()
            item['name'] = node.xpath('./div/div/div/div[2]/div[1]/div[1]/a/h2/text()').extract_first()
            item['link'] = node.xpath('./div/div/div/div[2]/div[1]/div[1]/a/@href').extract_first()
            item['cover_link'] = node.xpath('./div/div/div/div[1]/div/div/a/img/@src').extract_first()
            item['authors'] = node.xpath('./div/div/div/div[2]/div[1]/div[2]/span/text()').extract_first()
            item['price'] = node.xpath('./div/div/div/div[2]/div[2]/div[1]/div[2]/a/span[2]/text()').extract_first()
            item['praiseNum'] = node.xpath('//div/div/div/div[2]/div[2]/div[2]/div[1]/a/text()').extract_first()
            item['Discount'] = node.xpath(
                './div/div/div/div[2]/div[2]/div[1]/div[3]/div[2]/a/span[1]/text()|./div/div/div/div[2]/div[2]/div[1]/div[4]/div[2]/a/span[1]/text()').extract_first()
            item['sellersNum'] = node.xpath(
                './div/div/div/div[2]/div[2]/div[1]/div[4]/div[2]/a/span[4]/text()').extract_first()



            item['url'] = node.xpath('//div[@class="a-row a-spacing-none"]/a[@class="a-size-small a-link-normal a-text-normal"]/@href').extract_first()
            print(item['url'])
            yield scrapy.Request(item['url'], callback=self.get_sellers, meta={"data": item})

        # 翻页
        # base_url = 'https://www.amazon.cn'
        # next_url = base_url + response.xpath('//*[@id="pagnNextLink"]/@href').extract_first()
        # yield scrapy.Request(next_url, callback=self.parse)

    def get_sellers(self, response):
        item = response.meta['data']
        # print(response.meta['data'])
        node_list = response.xpath('//*[@id="olpOfferList"]/div/div/div[@class="a-row a-spacing-mini olpOffer"]')
        sellers = []
        for node in node_list:
            temp = {}
            temp['sellersprice'] = node.xpath('./div[1]/span/text()').extract_first().strip()
            temp['sellersInfo'] = node.xpath('./div[3]/h3/img/@alt|./div[3]/h3/span/a/text()').extract_first()
            temp['Gpraise'] = node.xpath('./div[3]/p/a/b/text()').extract_first()
            sellers.append(temp)

            item['sellers'] = sellers

        # print(item)
        yield item
    # #
    #     # # 翻页
    #     # src = 'https://www.amazon.cn'
    #     # next_url = src + response.xpath('//*[@id="olpOfferListColumn"]/div[2]/ul/li[4]/a/@href').extract_first()
    #     # if next_url != None:
    #     #     yield scrapy.Request(next_url, callback=self.get_sellers)
