# -*- coding:UTF-8 -*-

import traceback
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
    ssurl1 = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E4%B8%8A%E6%B5%B7%2B%E6%97%A0%E9%94%A1%2B%E8%8B%8F%E5%B7%9E&kw=' + gsmc + '&p=1&isadv=0'
    print(ssurl1);
    start_urls.append(ssurl1)
    CommonCode.ALLNUMBER = CommonCode.ALLNUMBER + 1
    print("一共客户请求数：" + str(len(start_urls)))


    def parse(self, response):
        CommonCode.DEALNUMBER = CommonCode.DEALNUMBER + 1
        print("处理进度：" + str(CommonCode.DEALNUMBER) + "/" + str(CommonCode.ALLNUMBER))
        self.logger.info("处理进度：" + str(CommonCode.DEALNUMBER) + "/" + str(CommonCode.ALLNUMBER))
        try:
            # 第一页数据
            zw_table = response.xpath('//table[@class="newlist"]')
            # 遍历每个职位
            print("开始处理第1页数据，职位数量："+str(len(zw_table)-1))
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
                        nexturl = theUrl.split('&p=')[0] + '&p=' + str(m + 1)
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
            print("开始处理第" + str(pagenum) + "页数据，职位数量：" + str(len(zw_table)-1))
            print(response.url)
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

            # fbrq = ''
            # fbrqs = response.xpath('//ul[@class="terminal-ul clearfix"]//li[3]/strong/span/text()').extract()
            # if (len(fbrqs) == 0):
            #     fbrq = response.xpath('//ul[@class="terminal-ul clearfix"]//li[3]/strong/text()').extract()[0]
            # else:
            #     fbrq = fbrqs[0]

            gzjy = response.xpath('//ul[@class="terminal-ul clearfix"]//li[5]/strong/text()').extract()[0]
            zdxl = response.xpath('//ul[@class="terminal-ul clearfix"]//li[6]/strong/text()').extract()[0]
            zprs = response.xpath('//ul[@class="terminal-ul clearfix"]//li[7]/strong/text()').extract()[0]

            zwmss = response.xpath('//div[@class="terminalpage-main clearfix"]//div[@class="tab-cont-box"]/div[1]')
            zwms = ''
            if (len(zwmss) > 0):
                zwms = zwmss[0].xpath('string(.)').extract()[0].strip().replace(' ', '')

            if ('工作地址：' in zwms):
                zwms = zwms[0:int(zwms.index('工作地址：'))]
            item['fl'] = fl
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
