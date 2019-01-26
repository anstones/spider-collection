# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from  scrapy.pipelines.images import ImagesPipeline
from  scrapy.utils.project import get_project_settings
import scrapy
import os

class DouyuPipeline(object):
    def process_item(self, item, spider):
        return item


class ImagePipeline(ImagesPipeline):

    IMAGES_STORE = get_project_settings().get('IMAGES_STORE')

    # 将需要下载的图片提交请求，不需要指定callback
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['image_url'])

    def item_completed(self, results, item, info):
        images = [data['path'] for status,data in results if status]

        # 拼接就图片名
        old_name = self.IMAGES_STORE + os.sep + images[0]
        # 创建新文件名
        new_name = self.IMAGES_STORE + os.sep + images[0].split(os.sep)[0] + os.sep + item['nick_name'] + '.jpg'

        # 重命名
        os.rename(old_name, new_name)

        item['image_path'] = new_name

        return item