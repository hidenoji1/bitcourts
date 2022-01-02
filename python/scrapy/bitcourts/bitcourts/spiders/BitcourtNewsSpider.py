import scrapy
import logging
import re
from spiders.BitcourtSpider import BitcourtSpider
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

DATABASE = 'mysql://root:password@mysql/mydb?charset=utf8'

class BitcourtNewsSpider(BitcourtSpider):
    name = 'bitcourts_news'
    allowed_domains = ['bit.courts.go.jp']
    start_urls = ['https://www.bit.courts.go.jp/']

    # ローカル設定
    custom_settings = {
        'USER_AGENT':{
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        },
        'DEFAULT_REQUEST_HEADERS':{
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ja,en-US;q=0.9,en;q=0.8,und;q=0.7',
        },   
        'ITEM_PIPELINES':{
            'pipelines.BitCourtsValidations': 100,
            'pipelines.BitPropertyItemPipeline': 200,
            'pipelines.BitPropertyDetailItemPipeline': 201,
            # 'pipelines.BitPropertyPdfPipeline': 202,
            # 'pipelines.BitResultItemPipeline': 203,
        },
        'DOWNLOAD_DELAY':3,
    }

    # リクエスト開始
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, errback=self.errback, dont_filter=True)

    # トップページ(新着)
    def parse(self, response):
        # ページ階層表示
        hierarchy = ['BIT 不動産競売物件情報サイト']
        logging.info(' > '.join(hierarchy))
        # パラメータ情報
        cookies  = self.get_response_cookies(response)
        formdata = self.get_response_formdata(response, 'topForm')
        # リクエスト情報
        post_action = response.xpath('//form[@id="topForm"]/@action').get() 
        post_url    = response.urljoin(post_action)
        # コンテンツ情報
        for element in response.xpath('//*[@id="bit__top_latestInformation"]/div/ul/li/a'):
            linkText = element.xpath('span/text()').getall()
            onclick  = element.xpath('@onclick').get()  
            args     = re.findall('"(.*?)"', re.sub('\'', '"', onclick)) 
            # 競売物件情報(新着)
            if onclick.startswith('tranPropertyResult('):
                formdata['prefecturesId'] = args[0]
                formdata['courtId']       = args[1]
                formdata['saleScdId']     = args[2]
                formdata['saleCls']       = args[3]
                formdata['tabId']         = args[4]
                # ルート情報
                route = hierarchy.copy()
                route.append('競売物件(新着)')
                route.append(''.join(linkText)) 
                yield scrapy.FormRequest(post_url, self.parse_property, 
                    method='POST',
                    cookies=cookies,
                    formdata=formdata,
                    meta={ 
                        'cookies': cookies.copy(),
                        'hierarchy': route.copy(),
                        'dont_merge_cookies': True,
                    },
                    errback=self.errback,
                    dont_filter=True,
                )
            
            continue

            # 売却結果情報(新着)
            if onclick.startswith('tranResult('):
                formdata['prefecturesId'] = args[0]
                formdata['courtId']       = args[1]
                formdata['saleScdId']     = args[2]
                formdata['saleCls']       = args[3]
                formdata['tabId']         = args[4]
                # ルート情報
                route = hierarchy.copy()
                route.append('売却結果(新着)')
                route.append(''.join(linkText)) 
                yield scrapy.FormRequest(post_url, self.parse_result, 
                    method='POST',
                    cookies=cookies,
                    formdata=formdata,
                    meta={ 
                        'cookies': cookies.copy(),
                        'hierarchy': route.copy(),
                        'dont_merge_cookies': True,
                    },
                    errback=self.errback,
                    dont_filter=True,
                )
 