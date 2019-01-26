# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouyuItem(scrapy.Item):
    # define the fields for your item here like:
    # 昵称
    nick_name = scrapy.Field()
    # 唯一id
    uid = scrapy.Field()
    # 图片链接
    image_url = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 图片存储位置
    image_path = scrapy.Field()
    pass
