# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field,Item



class YouyuanItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 个人头像链接
    header_url = Field()
    # 用户名
    username = Field()
    # 内心独白
    monologue = Field()
    # 相册图片链接
    pic_urls = Field()
    # 年龄
    age = Field()

    # 网站来源 youyuan
    source = Field()
    # 个人主页源url
    source_url = Field()

    # 获取UTC时间
    crawled = Field()
    # 爬虫名
    spider = Field()
