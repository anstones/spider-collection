# coding:utf-8
import requests
from lxml import etree
import os, json, sys


class Anzi_P(object):
    def __init__(self, page):
        self.url = 'http://www.azmyfw.com/list/?1_{}.html'.format(page)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 ',
            # 'Cookie':'ASPSESSIONIDCCDRACAT=HFOFNDGAFDDNHGOOAFLKGIJO; Hm_lvt_307821e29ffab841ee7bd4f2244f0766=1517377654,1517394503; ASPSESSIONIDAACRBBDT=DJLLODPAACOIBGPBDGIFOCPI; Hm_lpvt_307821e29ffab841ee7bd4f2244f0766=1517457403'
        }
        self.file = open('anzi.json', 'w')

    def get_data(self, url):
        response = requests.get(url, headers=self.headers,timeout=30)
        return response.content

    def parse_list_page(self, data):
        # 将源码转换成element对象
        html = etree.HTML(data)
        # 获取节点列表
        node_list = html.xpath('//*[@id="web_main"]/div[4]/div[1]/div/div/div[1]/dl')
        # print (len(node_list))
        # 构建返回数据的列表
        data_list = []
        # 遍历节点列表
        for node in node_list:
            temp = {}
            try:
                temp['title'] = node.xpath('./dt/a/text()')[0]
            except:
                temp['title'] = None
            # 详情页url
            temp['url'] = 'http://www.azmyfw.com' + node.xpath('./dt/a/@href')[0]
            data_list.append(temp)

        # 获取下一页url
        next_u = html.xpath('//div[@class="cpages"]/a[last()-1]/@href')[0]
        next_url = 'http://www.azmyfw.com/list/'+ next_u
        print(next_url)
        return data_list,next_url

    def parse_detail_page(self, data):
        html = etree.HTML(data)

        image_list = html.xpath('//div[@class="content"]/p/img/@src')

        return image_list

    def download(self, image_list, title):
        if not os.path.exists('image'):
            os.makedirs('image')

        # for url,index in image_list:
        for i, element in enumerate(image_list):
            # filename = 'image' + os.sep + url.split('/')[-1]
            if len(image_list) == 0:
                pass

            if len(image_list) == 1:
                filename = 'image' + os.sep + title + '.jpg'
                data = self.get_data(element)
                with open(filename, 'wb')as f:
                    f.write(data)

            if len(image_list) > 1:
                filename = 'image' + os.sep + title + str(i) + '.jpg'
                data = self.get_data(element)
                with open(filename, 'wb')as f:
                    f.write(data)


    def save_data(self, data):
        str_data = json.dumps(data, ensure_ascii=False) + ',\n'
        self.file.write(str_data)

    def __del__(self):
        self.file.close()

    def run(self):
        # 构建url
        # 构建请求头
        next_url = self.url
        while True:
            # 发送请求获取响应
            data = self.get_data(next_url)
            # 从列表页面响应中，抽取详情页面数据列表，下一页url
            detail_list,next_url = self.parse_list_page(data)
            # 遍历详情页面列表
            for detail in detail_list:
                # 获取详情页面的响应
                detail_data = self.get_data(detail['url'])
                # 提取图片链接列表
                image_list = self.parse_detail_page(detail_data)
                # 下载图片
                self.download(image_list, detail['title'])
                # 保存数据
                detail['images'] = image_list
                self.save_data(detail)


if __name__ == '__main__':
    tieba = Anzi_P('1')
    tieba.run()
