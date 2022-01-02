import scrapy
import re
from urllib.parse import urljoin
from spiders.BitcourtSpider import BitcourtSpider
from utils import COURTS
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

class BitcourtAuctionSpider(BitcourtSpider):
    name = 'bitcourts_auction'
    allowed_domains = ['bit.courts.go.jp']
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
            # 'pipelines.BitPropertyDetailItemPipeline': 201,
            # 'pipelines.BitPropertyPdfPipeline': 202,
            # 'pipelines.BitResultItemPipeline': 203,
        },
        'DOWNLOAD_DELAY':1,
        'DEPTH_LIMIT':0,
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BitcourtAuctionSpider, cls).from_crawler(crawler, *args, **kwargs)
        return spider

    # リクエスト開始
    def start_requests(self):
        requests = []
        start_url = 'https://www.bit.courts.go.jp/'
        # ページ階層表示
        hierarchy = ['BIT 不動産競売物件情報サイト', 'スケジュール']
        self.logger.info(' > '.join(hierarchy))
        for court in COURTS:
            # 裁判所コード
            courtId = court['courtId']
            # ページ階層の更新
            route = hierarchy.copy()
            route.append(court['courtNm'])
            # リクエスト発行
            get_action = f'/app/schedule/pr005/h01?courtId={courtId}'
            get_url = urljoin(start_url, get_action)
            request = scrapy.Request(get_url, self.parse, 
                    method='GET',
                    meta={ 
                        'court': court,
                        'hierarchy': route.copy(),
                        'dont_merge_cookies': True,
                    },
                    errback=self.errback,
                    dont_filter=True,
            )
            requests.append(request)
        return requests

    # トップページ(裁判所別スケジュール)
    def parse(self, response):
        # ページ階層表示
        court = response.meta['court']
        hierarchy = response.meta['hierarchy']
        self.logger.info(' > '.join(hierarchy))
        # パラメータ情報
        cookies = self.get_response_cookies(response)
        formdata = self.get_response_formdata(response, 'scheduleForm')
        # リクエスト情報
        post_action = response.xpath('//form[@id="scheduleForm"]/@action').get() 
        post_url = response.urljoin(post_action)
        # コンテンツ情報
        for element in response.xpath('///td/p/a'):
            onclick = element.xpath('@onclick').get()  
            args = re.findall('"(.*?)"', re.sub('\'', '"', onclick)) 
            # 競売物件情報
            if onclick.startswith('tranPropertyResult('):
                formdata['period'] = args[0]
                formdata['prefecturesId'] = args[1]
                formdata['courtId'] = args[2]
                formdata['saleScdId'] = args[3]
                formdata['linkFlg'] = args[4]
                formdata['etsuranLink'] = args[5]
                # ルート情報
                route = hierarchy.copy()
                #route.appand('')
                # リクエスト発行
                yield scrapy.FormRequest(post_url, self.parse_property, 
                    method='POST',
                    cookies=cookies,
                    formdata=formdata,
                    meta={ 
                        'court': court,
                        'hierarchy': route.copy(),
                        'dont_merge_cookies': True,
                    },
                    errback=self.errback,
                    dont_filter=True,
                )
