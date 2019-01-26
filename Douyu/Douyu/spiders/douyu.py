# -*- coding: utf-8 -*-
import scrapy
import json
from Douyu.items import DouyuItem

class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    # 修改允许的域
    allowed_domains = ['douyucdn.cn']
    base_url= 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=100&offset='
    offset = 0
    # 修改起始的URL
    start_urls = [base_url]

    def parse(self, response):
        # 获取直播列表
        room_list = json.loads(response.text)['data']

        # 遍历直播列表
        for room in room_list:
            # 创建item实例
            item = DouyuItem()

            # 抽取数据
            item['nick_name'] = room['nickname']
            item['uid'] = room['owner_uid']
            item['image_url'] = room['vertical_src']
            item['city'] = room['anchor_city']
            # print (item)
            # 返回数据
            yield item

        # 翻页
        if  len(room_list) != 0:
            self.offset += 100
            next_url = self.base_url + str(self.offset)
            yield scrapy.Request(next_url, callback=self.parse)