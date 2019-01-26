# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # 图书名
    name = scrapy.Field()
    # 图书链接
    link = scrapy.Field()
    # 封面链接
    cover_link = scrapy.Field()
    # 作者
    authors = scrapy.Field()
    # 图书价格
    price = scrapy.Field()
    # 最低价
    Discount =scrapy.Field()
    # 图书总评论数量
    praiseNum = scrapy.Field()
    # 在售商家数量
    sellersNum = scrapy.Field()
    url = scrapy.Field()

    sellers = scrapy.Field()
    # # 在售商家信息
    # sellersInfo = scrapy.Field()
    # # 在售商家价格
    # sellersprice = scrapy.Field()
    # # 商家好评率
    # Gpraise = scrapy.Field()



