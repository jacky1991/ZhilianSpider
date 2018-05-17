# -*- coding:UTF-8 -*-

import traceback
import scrapy
import urllib.request
from scrapy.http import Request
from ZhilianSpider.items import ZhilianspiderItem
from ZhilianSpider.commoncode import *


class ZhiLianSpider(scrapy.Spider):
    logger = logging.getLogger()

    name = "zhilianspider"
    allowed_domains = ['zhaopin.com']
    CommonCode.DEALNUMBER = 0
    CommonCode.ALLNUMBER = 0
    start_urls = []
    # for line in open("customer_zhilian.txt"):
    #     if (line != '' and line.strip() != ''):
    keyword = "饿了么"
    gsmc = urllib.request.quote(keyword.strip())
    # 上海%2B无锡%2B苏州
    # ssurl1 = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E4%B8%8A%E6%B5%B7%2B%E6%97%A0%E9%94%A1%2B%E8%8B%8F%E5%B7%9E&kw=' + gsmc + '&p=1&kt=2&isadv=0'
    # 广东%2B江苏%2B山西%2B湖南%2B青海
    ssurl1 = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%B9%BF%E4%B8%9C%2B%E6%B1%9F%E8%8B%8F%2B%E5%B1%B1%E8%A5%BF%2B%E6%B9%96%E5%8D%97%2B%E9%9D%92%E6%B5%B7&kw=' + gsmc + '&p=1&kt=2&isadv=0'
    # 湖北%2B山东%2B内蒙古%2B海南%2B宁夏
    ssurl2 = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B9%96%E5%8C%97%2B%E5%B1%B1%E4%B8%9C%2B%E5%86%85%E8%92%99%E5%8F%A4%2B%E6%B5%B7%E5%8D%97%2B%E5%AE%81%E5%A4%8F&kw=' + gsmc + '&p=1&kt=2&isadv=0'
    # 陕西%2B浙江%2B黑龙江%2B贵州%2B新疆
    ssurl3 = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E9%99%95%E8%A5%BF%2B%E6%B5%99%E6%B1%9F%2B%E9%BB%91%E9%BE%99%E6%B1%9F%2B%E8%B4%B5%E5%B7%9E%2B%E6%96%B0%E7%96%86&kw=' + gsmc + '&p=1&kt=2&isadv=0'
    # 四川%2B广西%2B福建%2B云南%2B香港
    ssurl4 = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%B9%BF%E4%B8%9C%2B%E6%B1%9F%E8%8B%8F%2B%E5%B1%B1%E8%A5%BF%2B%E6%B9%96%E5%8D%97%2B%E9%9D%92%E6%B5%B7&kw=' + gsmc + '&p=1&kt=2&isadv=0'
    # 辽宁%2B安徽%2B江西%2B西藏%2B澳门
    ssurl5 = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E8%BE%BD%E5%AE%81%2B%E5%AE%89%E5%BE%BD%2B%E6%B1%9F%E8%A5%BF%2B%E8%A5%BF%E8%97%8F%2B%E6%BE%B3%E9%97%A8&kw=' + gsmc + '&p=1&kt=2&isadv=0'
    # 吉林%2B河北%2B河南%2B甘肃%2B台湾省
    ssurl6 = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%90%89%E6%9E%97%2B%E6%B2%B3%E5%8C%97%2B%E6%B2%B3%E5%8D%97%2B%E7%94%98%E8%82%83%2B%E5%8F%B0%E6%B9%BE%E7%9C%81&kw=' + gsmc + '&p=1&kt=2&isadv=0'

    start_urls.append(ssurl1)
    start_urls.append(ssurl2)
    start_urls.append(ssurl3)
    start_urls.append(ssurl4)
    start_urls.append(ssurl5)
    start_urls.append(ssurl6)
    CommonCode.ALLNUMBER = CommonCode.ALLNUMBER + 6
    print("一共客户请求数：" + str(len(start_urls)))


    def parse(self, response):
        CommonCode.DEALNUMBER = CommonCode.DEALNUMBER + 1
        print("处理进度：" + str(CommonCode.DEALNUMBER) + "/" + str(CommonCode.ALLNUMBER))
        self.logger.info("处理进度：" + str(CommonCode.DEALNUMBER) + "/" + str(CommonCode.ALLNUMBER))
        try:
            # 第一页数据
            zw_table = response.xpath('//table[@class="newlist"]')
            # 遍历每个职位
            # print("开始处理第1页数据，职位数量："+str(len(zw_table)-1))
            for i in range(len(zw_table)):
                if (i > 0):  # 第一个table是表格头部，不是职位信息
                    zwmc = zw_table[i].xpath('.//td[@class="zwmc"]//div/a[1]')[0].xpath('string(.)').extract()
                    fkl = zw_table[i].xpath('.//td[@class="fk_lv"]//span/text()').extract()
                    if (len(fkl) == 0):
                        fkl = ''
                    else:
                        fkl = fkl[0]
                    zwmcurl = zw_table[i].xpath('.//td[@class="zwmc"]//div/a[1]/@href').extract()
                    gsmc = zw_table[i].xpath('.//td[@class="gsmc"]//a[1]')[0].xpath('string(.)').extract()

                    zwyx = zw_table[i].xpath('.//td[@class="zwyx"]//text()').extract()
                    gzdd = zw_table[i].xpath('.//td[@class="gzdd"]//text()').extract()
                    #
                    item = ZhilianspiderItem()
                    item['zwmc'] = zwmc[0]
                    # print(zwmc)
                    item['fkl'] = fkl
                    item['gsmc'] = gsmc[0]
                    item['zwyx'] = zwyx[0]
                    item['gzdd'] = gzdd[0]
                    item['zwmcurl'] = zwmcurl[0]
                    # print(item)
                    # # 如果搜索的不是要获取的公司名（可能是模糊搜索到的）
                    # theGsmc = urllib.request.unquote(response.url.split('&kw=')[1].split('&p=')[0])
                    # if (theGsmc == item['gsmc']):
                    yield Request(item['zwmcurl'], meta={'item': item}, callback=self.parse_item_info)
        except Exception as err:
            print(err)
            self.logger.info("处理第一页职位列表异常：" + response.url + str(err))
            CommonCode.insertErrorLog("处理第一页职位列表出错：" + response.url, str(err))
        # 获取分页信息，并查询下一页
        try:
            # link_urls = response.xpath('//dd/a[1]/@href').extract()
            # 获取总页数
            countNumber = int(response.xpath('//span[@class="search_yx_tj"]//em/text()').extract()[0])
            if (countNumber > 0):
                theUrl = response.url
                perPageNumber = 60
                temP = 0
                if (countNumber % 60 > 0):
                    temP = 1;
                countPage = int(countNumber // perPageNumber) + int(temP)
                print("本次抓取职位总数：" + str(countNumber)+",总共"+str(countPage)+"页")
                for m in range(countPage):
                    if (m > 0):
                        nexturl = theUrl.split('&p=')[0] + '&p=' + str(m + 1)+'&kt='+theUrl.split('&kt=')[1]
                        # print(nexturl)
                        yield Request(nexturl,meta={"pagenum":m+1}, callback=self.parse_item)
        except Exception as err:
            print(err)
            traceback.print_exc()
            self.logger.info("获取下一页异常：" + response.url + str(err))
            CommonCode.insertErrorLog("获取下一页出错：" + response.url, str(err))

    # 处理一页一页的数据
    def parse_item(self, response):
        try:
            pagenum = response.meta["pagenum"]
            # 职位信息table
            zw_table = response.xpath('//table[@class="newlist"]')
            # print("开始处理第" + str(pagenum) + "页数据，职位数量：" + str(len(zw_table)-1))
            # 遍历每个职位
            for i in range(len(zw_table)):
                if (i > 0):  # 第一个table是表格头部，不是职位信息
                    zwmc = zw_table[i].xpath('.//td[@class="zwmc"]//div/a[1]/text()').extract()
                    # print(zwmc)
                    fkl = zw_table[i].xpath('.//td[@class="fk_lv"]//span/text()').extract()
                    if (len(fkl) == 0):
                        fkl = ''
                    else:
                        fkl = fkl[0]
                    zwmcurl = zw_table[i].xpath('.//td[@class="zwmc"]//div/a[1]/@href').extract()
                    gsmc = zw_table[i].xpath('.//td[@class="gsmc"]//a[1]/b/text()').extract()
                    if (len(gsmc) == 0):
                        gsmc = zw_table[i].xpath('.//td[@class="gsmc"]//a[1]/text()').extract()
                    zwyx = zw_table[i].xpath('.//td[@class="zwyx"]//text()').extract()
                    gzdd = zw_table[i].xpath('.//td[@class="gzdd"]//text()').extract()
                    #
                    item = ZhilianspiderItem()
                    # print(zwmc[0])
                    item['zwmc'] = zwmc[0]
                    item['fkl'] = fkl
                    item['gsmc'] = gsmc[0]
                    item['zwyx'] = zwyx[0]
                    item['gzdd'] = gzdd[0]
                    item['zwmcurl'] = zwmcurl[0]
                    yield Request(item['zwmcurl'], meta={'item': item}, callback=self.parse_item_info)
        except Exception as err:
            print(err)
            traceback.print_exc()
            self.logger.info("处理下一页职位列表异常：" + response.url + str(err))
            CommonCode.insertErrorLog("处理下一页职位列表出错：" + response.url, str(err))

    # 处理一个职位连接里的详情
    def parse_item_info(self, response):
        try:
            item = response.meta['item']
            # 福利
            fl = ''
            flarray = response.xpath('//div[@class="welfare-tab-box"]//span/text()').extract()
            for i in range(len(flarray)):
                if (i == 0):
                    fl = fl + flarray[i]
                else:
                    fl = fl + ',' + flarray[i]

            fbrq = ''
            fbrqs = response.xpath('//ul[@class="terminal-ul clearfix"]//li[3]/strong/span/text()').extract()
            if (len(fbrqs) == 0):
                fbrq = response.xpath('//ul[@class="terminal-ul clearfix"]//li[3]/strong/text()').extract()[0]
            else:
                fbrq = fbrqs[0]

            gzjy = response.xpath('//ul[@class="terminal-ul clearfix"]//li[5]/strong/text()').extract()[0]
            zdxl = response.xpath('//ul[@class="terminal-ul clearfix"]//li[6]/strong/text()').extract()[0]
            zprs = response.xpath('//ul[@class="terminal-ul clearfix"]//li[7]/strong/text()').extract()[0]
            zwlb = response.xpath('//ul[@class="terminal-ul clearfix"]//li[8]/strong/a[1]/text()').extract()[0]

            zwmss = response.xpath('//div[@class="terminalpage-main clearfix"]//div[@class="tab-cont-box"]/div[1]')
            zwms = ''
            if (len(zwmss) > 0):
                zwms = zwmss[0].xpath('string(.)').extract()[0].strip().replace(' ', '')

            if ('工作地址：' in zwms):
                zwms = zwms[0:int(zwms.index('工作地址：'))]

            item['fl'] = fl
            item['zwlb'] = zwlb
            item['fbrq']= fbrq
            item['gzjy'] = gzjy
            item['zdxl'] = zdxl
            item['zprs'] = zprs
            item['zwms'] = zwms
            # print(item)
            self.logger.info("解析成功：" + item['gsmc'] + "-" + item['zwmc'])
            yield item
        except Exception as err:
            print(err)
            traceback.print_exc()
            self.logger.info("处理职位详情异常：" + response.url + str(err))
            CommonCode.insertErrorLog("处理职位详情出错：" + response.url, str(err))
