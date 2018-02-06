#!/usr/bin/env python
# coding:utf-8
# Created by  on 18-2-6
# Copyright (c) 2018 $USER.ALL rights reserved.
"""
策略一：直接POST数据（比如需要登陆的账户信息)
只要是需要提供post数据的，就可以用这种方法。下面示例里post的数据是账户密码：
"""
import scrapy


class Renren1Spider(scrapy.Spider):
    name = "renren1"
    allowed_domains = ["renren.com"]

    def start_requests(self):
        url = 'http://www.renren.com/PLogin.do'
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
                url = url,
                formdata = {"email" : "mr_mao_hacker@163.com", "password" : "axxxxxxxe"},
                callback = self.parse_page)

    def parse_page(self, response):
        with open("mao2.html", "w") as filename:
            filename.write(response.body)