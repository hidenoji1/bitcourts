import scrapy
import re
from urllib.parse import urljoin

from scrapy.http import request
from spiders.BitcourtSpider import BitcourtSpider
from utils import BLOCKS

class BitcourtResultSpider(BitcourtSpider):
    name = 'bitcourts_result'
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
        #'LOG_ENABLED':True,
        #'LOG_FILE': 'bitcourts_auction.log', 
        'ITEM_PIPELINES':{
            'pipelines.BitCourtsValidations': 100,
            'pipelines.BitPropertyPipeline': 200,
            'pipelines.BitPropertyHeaderPipeline': 201,
            'pipelines.BitResultPipeline': 203,
            # 'pipelines.BitPropertyDetailItemPipeline': 201,
            # 'pipelines.BitPropertyPdfPipeline': 202,
            # 'pipelines.BitResultItemPipeline': 203,
        },
        'DOWNLOAD_DELAY':1,
        'DEPTH_LIMIT':0,
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BitcourtResultSpider, cls).from_crawler(crawler, *args, **kwargs)
        return spider

    # リクエスト開始
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, errback=self.errback, dont_filter=True)

    # トップページ
    def parse(self, response):
        requests = []
        # ページ階層表示
        hierarchy = ['BIT 不動産競売物件情報サイト']
        self.logger.info(' > '.join(hierarchy))
        # パラメータ情報
        cookies  = self.get_response_cookies(response)
        formdata = self.get_response_formdata(response, 'headerForm')
        # リクエスト情報
        post_action = response.xpath('//form[@id="headerForm"]/@action').get() 
        post_url    = response.urljoin(post_action)
        # 売却結果(日本地図)へ移動
        for element in response.xpath('//li[@id="baikyakublock"]/a'):
            blockNm = element.xpath('text()').get()
            onclick = element.xpath('@onclick').get()  
            args = re.findall('"(.*?)"', re.sub('\'', '"', onclick)) 
            if onclick.startswith('tranArea('):
                formdata['tabId']    = args[0]
                formdata['blockCls'] = args[1]
                # ルート情報
                route = hierarchy.copy()
                route.append(blockNm)
                # リクエスト発行
                request = scrapy.FormRequest(post_url, self.parse_map_japan, 
                    method='POST',
                    cookies=cookies,
                    formdata=formdata,
                    meta={ 
                        'hierarchy': route.copy(),
                        'dont_merge_cookies': True,
                    },
                    errback=self.errback,
                    dont_filter=True,
                )
                requests.append(request)
        return requests

    # 売却結果(日本地図)
    def parse_map_japan(self, response):
        requests = []
        # ページ階層表示
        hierarchy = ['BIT 不動産競売物件情報サイト']
        self.logger.info(' > '.join(hierarchy))
        # パラメータ情報
        cookies  = self.get_response_cookies(response)
        formdata = self.get_response_formdata(response, 'areaForm')
        # リクエスト情報
        post_action = response.xpath('//form[@id="areaForm"]/@action').get() 
        post_url    = response.urljoin(post_action)
        # エリア詳細に移動
        for block in BLOCKS:
            formdata['blockCls'] = block['blockCls']
            # ルート情報
            route = hierarchy.copy()
            route.append('売却結果')
            route.append(''.join(block['blockNm'])) 
            request = scrapy.FormRequest(post_url, self.parse_map_block, 
                method='POST',
                cookies=cookies,
                formdata=formdata,
                meta={ 
                    'block': block,
                    'hierarchy': route.copy(),
                    'dont_merge_cookies': True,
                },
                errback=self.errback,
                dont_filter=True,
            )
            requests.append(request)
        return requests
 
    # 売却結果(ブロック地図)
    def parse_map_block(self, response):
        requests = []
        # ページ階層表示
        hierarchy = response.meta['hierarchy']
        self.logger.info(' > '.join(hierarchy))
        # パラメータ情報
        block = response.meta['block']
        # 開札結果の検索
        cookies  = self.get_response_cookies(response)
        formdata = self.get_response_formdata(response, 'peroidResultSearchForm')
        for element in response.xpath('//a[@id="kaisastu-tab"]'):
            tabNm   = element.xpath('text()').get() 
            onclick = element.xpath('@onclick').get() 
            args    = re.findall('"(.*?)"', re.sub('\'', '"', onclick)) 
            if onclick.startswith('tranPeroidSearch('):
                formdata['peroidSaleType'] = '1'
                formdata['peroidBlockCls'] = args[0]  
                formdata['tabId']          = args[1]
                # ルート情報
                route = hierarchy.copy()
                route.append(tabNm)
                # リクエスト作成
                post_action = '/app/peroidsearch/ps007/h09'
                post_url    = response.urljoin(post_action)
                request = scrapy.FormRequest(post_url, self.parse_result_peroid_search, 
                    method='POST',
                    cookies=cookies,
                    formdata=formdata,
                    meta={ 
                        'block': block,
                        'hierarchy': route.copy(),
                        'dont_merge_cookies': True,
                    },
                    errback=self.errback,
                    dont_filter=True,
                )
                requests.append(request)
        # 特別売却結果の検索
        cookies  = self.get_response_cookies(response)
        formdata = self.get_response_formdata(response, 'specialResultSearchForm')
        for element in response.xpath('//a[@id="tokubetsu-tab"]'):
            tabNm   = element.xpath('text()').get() 
            onclick = element.xpath('@onclick').get() 
            args    = re.findall('"(.*?)"', re.sub('\'', '"', onclick))  
            if onclick.startswith('tranSpecialSearch('):
                formdata['specialSaleType'] = '2'
                formdata['specialBlockCls'] = args[0]  
                formdata['tabId']           = args[1]
                # ルート情報
                route = hierarchy.copy()
                route.append(tabNm)
                # リクエスト作成
                post_action = '/app/specialsearch/ps008/h09'
                post_url    = response.urljoin(post_action)
                request = scrapy.FormRequest(post_url, self.parse_result_special_search, 
                    method='POST',
                    cookies=cookies,
                    formdata=formdata,
                    meta={ 
                        'block': block,
                        'hierarchy': route.copy(),
                        'dont_merge_cookies': True,
                    },
                    errback=self.errback,
                    dont_filter=True,
                )
                #requests.append(request)
        return requests

    # 売却結果(開札結果の検索)
    def parse_result_peroid_search(self, response):
        requests = []
        # ページ階層表示
        hierarchy = response.meta['hierarchy']
        self.logger.info(' > '.join(hierarchy))
        # パラメータ情報
        block = response.meta['block']
        blockCls = block['blockCls']
        blockId  = block['blockId']
        blockNm  = block['blockNm']
        # 開札結果の検索
        cookies  = self.get_response_cookies(response)
        formdata = self.get_response_formdata(response, 'peroidResultSearchForm')
        # リクエスト作成
        for element in response.xpath(f'//map[@name="bit__map_{blockId}_chiiki"]/area'):
            areaNm  = element.xpath('@alt').get() 
            onclick = element.xpath('@onclick').get() 
            args    = re.findall('"(.*?)"', re.sub('\'', '"', onclick))
            if onclick.startswith('showSearchCondition('):
                formdata['prefecturesId']       = args[0]
                formdata['saleType']            = args[1]
                formdata['mapSelectedAreaName'] = args[2]
                formdata['blockCls']            = blockCls
                formdata['blockName']           = blockNm
                formdata['tabId']               = 'result'
                # ルート情報
                route = hierarchy.copy()
                route.append(areaNm)
                # リクエスト作成
                post_action = '/app/peroidsearch/ps007/h02'
                post_url    = response.urljoin(post_action)
                request = scrapy.FormRequest(post_url, self.parse_result_peroid_click, 
                    method='POST',
                    cookies=cookies,
                    formdata=formdata,
                    meta={ 
                        'block': block,
                        'hierarchy': route.copy(),
                        'dont_merge_cookies': True,
                    },
                    errback=self.errback,
                    dont_filter=True,
                )
                requests.append(request)
        return requests

    # 売却結果(検索条件を表示する(マップクリック))
    def parse_result_peroid_click(self, response):
        # ページ階層表示
        hierarchy = response.meta['hierarchy']
        self.logger.info(' > '.join(hierarchy))
        # パラメータ情報
        block = response.meta['block']
        # 開札結果の検索
        cookies  = self.get_response_cookies(response)
        formdata = self.get_response_formdata(response, 'peroidResultSearchForm')
        jsondata = self.get_response_jsondata(response, 'peroidResultSearchForm')
        formdata['searchType'] = '1'
        formdata['saleScdId']  = jsondata['pSaleScdId']
        formdata['fiscalYear'] = jsondata['pFiscalYear']
        formdata['codeCls']    = jsondata['pCodeCls']
        formdata['caseNo']     = jsondata['pCaseNo']
        # リクエスト作成
        post_action = '/app/peroidsearch/ps007/h03'
        post_url    = response.urljoin(post_action)
        return scrapy.FormRequest(post_url, self.parse_result, 
            method='POST',
            cookies=cookies,
            formdata=formdata,
            meta={ 
                'block': block,
                'hierarchy': hierarchy.copy(),
                'dont_merge_cookies': True,
            },
            errback=self.errback,
            dont_filter=True,
        )

    # 売却結果(特別売却結果の検索)
    def parse_result_special_search(self, response):
        pass

    # 売却結果(特別売却結果の検索)
    def parse_result_special_click(self, response):
        pass
