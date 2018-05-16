# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilianspiderItem(scrapy.Item):
    zwmc = scrapy.Field()  # 职位名称
    fkl = scrapy.Field()  # 反馈率
    gsmc = scrapy.Field()  # 公司名称
    zwyx = scrapy.Field()  # 职位月薪
    gzdd = scrapy.Field()  # 工作地点
    zwmcurl = scrapy.Field()  # 职位地址
    fl = scrapy.Field()  # 福利
    gzjy = scrapy.Field()  # 工作经验
    zdxl = scrapy.Field()  # 最低学历
    zprs = scrapy.Field()  # 招聘人数
    zwms = scrapy.Field()  # 职位描述
