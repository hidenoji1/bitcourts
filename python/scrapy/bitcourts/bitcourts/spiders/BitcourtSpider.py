from re import T
import scrapy
import os
from utils import utils
from items import *
from tables import *
from scrapy import signals
from scrapy.loader import ItemLoader
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

#
class BitcourtSpider(scrapy.Spider):

    engine  = None
    session = None
        
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BitcourtSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        spider.engine = create_engine('mysql://root:password@mysql/mydb?charset=utf8', echo=True)
        return spider

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s', spider.name)
        # データベース接続開始
        #self.engine = create_engine('mysql://root:password@mysql/mydb?charset=utf8', echo=True)
        self.session = Session(bind=self.engine, autocommit=False, autoflush=False)

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)
        # データベース接続終了
        self.session.close()
        self.engine.dispose()

    # エラーハンドラ
    def errback(self, failure):
        self.logger.error(repr(failure))

    # 競売物件情報(一覧)
    def parse_property(self, response):
        # ページ階層表示
        court = response.meta['court']
        hierarchy = response.meta['hierarchy']
        self.logger.info(' > '.join(hierarchy))
        # パラメータ情報
        cookies  = self.get_response_cookies(response)
        formdata = self.get_response_formdata(response, 'propertyResultForm')
        # 競売物件一覧取得
        totalCount = self.get_formdata_totalCount(formdata)
        if (totalCount == 0):
            hierarchy.append('なし')
            self.logger.info(' > '.join(hierarchy))
        properties = []  
        for i in range(0, totalCount):
            courtId    = self.get_formdata_resultList(formdata, 'courtId',    i)  
            saleUnitId = self.get_formdata_resultList(formdata, 'saleUnitId', i)
            if (courtId != '' and saleUnitId != ''):
                # 競売物件情報の取得
                loader = ItemLoader(item=BitPropertyItem())
                loader.add_value('blockId', court['blockId'])
                loader.add_value('blockNm', court['blockNm'])
                loader.add_value('prefecturesId', court['prefecturesId'])
                loader.add_value('prefecturesNm', court['prefecturesNm'])
                for key in BitPropertyItem().fields.keys():
                    loader.add_value(key, self.get_formdata_resultList(formdata, key, i))
                # 競売物件情報の更新チェック
                property = loader.load_item()
                if self.has_property_modified(property):
                    properties.append(property)
        # 競売物件情報の出力
        for property in properties:
            yield property
        # 競売物件情報の更新
        for property in properties:
            # 競売物件情報(詳細)リクエスト
            saleUnitId = ''.join(property['saleUnitId'])
            courtId    = ''.join(property['courtId']) 
            formdata['saleUnitId']      = saleUnitId
            formdata['detailCourtId']   = courtId
            formdata['transitionTabId'] = '1'
            # ページ階層の更新
            route = hierarchy.copy()
            route.append(''.join(property['caseNoLink']))
            # POSTリクエスト発行
            post_action = '/app/propertyresult/pr001/h05'
            post_url    = response.urljoin(post_action)
            request = scrapy.FormRequest(post_url, self.parse_property_detail, 
                method='POST',
                cookies=cookies,
                formdata=formdata,
                meta={ 
                    'courtId': courtId,
                    'saleUnitId': saleUnitId,
                    'court': court,
                    'hierarchy': route.copy(),
                    'dont_merge_cookies': True,
                },
                errback=self.errback,
                dont_filter=True,
            )
            yield request
        
    # 競売物件情報の更新チェック
    def has_property_modified(self, property):
        courtId         = utils.to_str(property['courtId'])
        saleUnitId      = utils.to_str(property['saleUnitId'])               
        note            = utils.to_str(property['note'])
        stopInformation = utils.to_str(property['stopInformation'])
        periodBidStatus = utils.to_str(property['periodBidStatus'])
        row = self.session.query(
                BitProperties.note,
                BitProperties.stopInformation,
                BitProperties.periodBidStatus,
            ).filter(
                and_(
                    BitProperties.courtId   ==courtId,
                    BitProperties.saleUnitId==saleUnitId,
                )
            ).one_or_none()
        if (row is None):
            return True
        elif (note != row.note):
            return True
        elif (stopInformation != row.stopInformation):
            return True
        elif (periodBidStatus != row.periodBidStatus):
            return True
        return False

    # 競売物件情報(詳細)
    def parse_property_detail(self, response):
        # ページ階層表示
        hierarchy = response.meta['hierarchy']
        self.logger.info(' > '.join(hierarchy))
        # パラメータ情報
        cookies = self.get_response_cookies(response)
        # 競売物件情報
        courtId    = response.meta['courtId']
        saleUnitId = response.meta['saleUnitId']
        court      = response.meta['court']
        # 情報取得、競売物件ヘッダ
        items = self.parse_property_detail_header(response)
        if (0 == len(items)):
            # データなし
            pass
        else:
            # 情報登録、競売物件ヘッダ
            for item in items:
                yield item

            # サムネイルファイル
            for element in response.xpath('//img[@class="bit__image"]'):
                img_action = element.xpath('@src').get()
                img_url    = response.urljoin(img_action)
                # ファイルのダウンロード開始
                yield scrapy.Request(img_url, self.parse_property_thumbnails, 
                    cookies=cookies,
                    meta={ 
                        'courtId': courtId,
                        'saleUnitId': saleUnitId,
                        'court': court,
                        'hierarchy': hierarchy.copy(),
                        'dont_merge_cookies': True,
                    },
                    errback=self.errback,
                    dont_filter=True,
                )   

            # 情報登録、競売物件詳細
            for item in self.parse_property_detail_items(response):
                yield item

            # 3点セット（物件明細書，現況調査報告書及び評価書等）PDFファイル
            pdf_action = '/app/detail/pd001/h04'
            pdf_url    = response.urljoin(pdf_action)
            pdf_url   += f'?courtId={courtId}&saleUnitId={saleUnitId}'
            # PDFファイルのダウンロード開始
            yield scrapy.Request(pdf_url, self.parse_property_pdf, 
                cookies=cookies,
                meta={ 
                    'courtId': courtId,
                    'saleUnitId': saleUnitId,
                    'court': court,
                    'hierarchy': hierarchy.copy(),
                    'dont_merge_cookies': True,
                },
                errback=self.errback,
                dont_filter=True,
            )
    
    # 競売物件ヘッダ情報取得
    def parse_property_detail_header(self, response):
        items = []
        courtId    = response.meta['courtId']
        saleUnitId = response.meta['saleUnitId']
        # 競売物件ヘッダ情報
        for element in response.xpath('//*[@id="bit__main"]/div'):
            saleStatusDisp = element.xpath('div[2]/div/div[3]/div[2]/div/p/text()').get()
            loader = ItemLoader(item=BitPropertyHeaderItem(), selector=element)   
            loader.add_value('courtId',        courtId)
            loader.add_value('saleUnitId',     saleUnitId)
            loader.add_value('saleStatusDisp', saleStatusDisp)
            loader.add_xpath('caseNoLink',     'div[2]/div/div[1]/p/text()')
            # ヘッダー、期間入札/特別売却
            header = loader.nested_xpath('div[2]/div/div[3]') 
            if ('期間' in str(saleStatusDisp)):
                header.add_xpath('saleStandardAmountDisp',          'div[1]/div[1]/p[2]/text()')              # 売却基準価額  
                header.add_xpath('guaranteeAmountDisp',             'div[1]/div[2]/div[1]/p[2]/text()')       # 買受申出保証金
                header.add_xpath('purchaseableAmountDisp',          'div[1]/div[2]/div[2]/p[2]/text()')       # 買受可能価額
                header.add_xpath('announcementStartDateDisp',       'div[2]/div/div/div[1]/div[2]/text()')    # 公示開始日
                header.add_xpath('perusalStartDateDisp',            'div[2]/div/div/div[1]/div[4]/text()')    # 閲覧開始日
                header.add_xpath('bidPeriod',                       'div[2]/div/div/div[2]/div[2]/text()')    # 入札期間
                header.add_xpath('checkTenderDateDisp',             'div[2]/div/div/div[3]/div[2]/text()')    # 開札期日
                header.add_xpath('saleDecisionDateDisp',            'div[2]/div/div/div[3]/div[4]/text()')    # 売却決定期日
                header.add_xpath('specialSalePeriod',               'div[2]/div/div/div[4]/div[2]/text()')    # 特別売却期間
            elif ('特別' in str(saleStatusDisp)):   
                header.add_xpath('saleStandardAmountDisp',          'div[1]/div[1]/p[2]/text()')              # 売却基準価額  
                header.add_xpath('guaranteeAmountDisp',             'div[1]/div[2]/div[1]/p[2]/text()')       # 買受申出保証金
                header.add_xpath('purchaseableAmountDisp',          'div[1]/div[2]/div[2]/p[2]/text()')       # 買受可能価額
                header.add_xpath('specialSalePerusalStartDateDisp', 'div[2]/div/div/div[1]/div[2]/text()')    # 特別売却閲覧開始日
                header.add_xpath('specialSalePeriod',               'div[2]/div/div/div[2]/div[2]/text()')    # 特別売却期間
            # フッター、参考交通
            footer = loader.nested_xpath('div[4]/div/div/div[2]/div[4]/div/div')
            footer.add_xpath('referenceRoute1', 'div[2]/div[2]/text()[1]')   
            footer.add_xpath('referenceRoute2', 'div[2]/div[2]/text()[2]')   
            footer.add_xpath('referenceRoute3', 'div[2]/div[2]/text()[3]')   
            footer.add_xpath('referenceRoute4', 'div[2]/div[2]/text()[4]')   
            footer.add_xpath('referenceRoute5', 'div[2]/div[2]/text()[5]')   
            # 削除されたデータは保存しない
            if (saleStatusDisp is not None):
                items.append(loader.load_item())    
        return items

    # 競売物件詳細情報取得
    def parse_property_detail_items(self, response):
        items = []
        # パラメータ取得
        courtId    = response.meta['courtId']
        saleUnitId = response.meta['saleUnitId']
        court      = response.meta['court']
        # 物件詳細一覧
        for element in response.xpath('//*[@id="bloc"]/div/div[@class="form-contents"]'):
            loader = ItemLoader(item=BitPropertyDetailItem(), selector=element)
            loader.add_value('document',      element.get())            # HTML
            loader.add_value('prefecturesId', court['prefecturesId'])   # 都道府県コード
            loader.add_value('courtId',       courtId)                  # 裁判所コード
            loader.add_value('saleUnitId',    saleUnitId)               # 物件識別コード
            saleCls = element.xpath('div[1]/div/p/text()').get()
            if ('土地' in str(saleCls)):
                loader.add_value('thingCls',                '1')                                        # 種別コード
                loader.add_xpath('thingType',               'div[2]/div[1]/div[2]/span[1]/text()')      # 種別
                loader.add_xpath('thingKindAttribute1',     'div[2]/div[1]/div[2]/span[2]/text()')
                loader.add_xpath('thingKindAttribute2',     'div[2]/div[1]/div[2]/span[3]/text()')
                loader.add_xpath('thingNo',                 'div[2]/div[2]/div[2]/text()')              # 物件番号
                loader.add_xpath('address',                 'div[2]/div[3]/div[2]/span[1]/text()')      # 所在地
                loader.add_xpath('streetNo',                'div[2]/div[3]/div[2]/span[2]/text()')      # 番地
                loader.add_xpath('landCls',                 'div[2]/div[4]/div[2]/text()')              # 土地の地目（登記）
                loader.add_xpath('landClsStatus',           'div[2]/div[4]/div[4]/text()')              # 土地の地目（現況）
                loader.add_xpath('landLandArea',            'div[2]/div[5]/div[2]/span/node()')         # 土地の面積（登記）
                loader.add_xpath('landLandAreaStatus',      'div[2]/div[5]/div[4]')                     # 土地の面積（現況） 
                loader.add_xpath('landUseArea',             'div[2]/div[6]/div[2]/span/text()')         # 土地の用途地域
                loader.add_xpath('landConditionCls',        'div[2]/div[6]/div[4]/text()')              # 土地の利用状況
                loader.add_xpath('landBuildingCoverage',    'div[2]/div[7]/div[2]/span/node()')         # 土地の建ぺい率
                loader.add_xpath('landFloorArea',           'div[2]/div[7]/div[4]/span/text()')         # 土地の容積率
                loader.add_xpath('landEquity',              'div[2]/div[8]/div[2]/span/text()')         # 土地の持分
            # elif ('地上権' in str(saleCls)):
            #     pass
            elif ('区分所有' in str(saleCls)):
                loader.add_value('thingCls',                '3')                                        # 種別コード
                loader.add_xpath('thingType',               'div[2]/div[1]/div[2]/span[1]/text()')      # 種別
                loader.add_xpath('thingKindAttribute1',     'div[2]/div[1]/div[2]/span[2]/text()')
                loader.add_xpath('thingKindAttribute2',     'div[2]/div[1]/div[2]/span[3]/text()')
                loader.add_xpath('thingNo',                 'div[2]/div[2]/div[2]/text()')              # 物件番号
                loader.add_xpath('address',                 'div[2]/div[3]/div[2]/span/text()')         # 所在地
                loader.add_xpath('streetNo',                'div[2]/div[4]/div[2]/text()')              # 番地
                loader.add_xpath('mansionBuildingNo',       'div[2]/div[5]/div[2]/text()')              # マンションの建物番号
                loader.add_xpath('mansionCls',              'div[2]/div[6]/div[2]/span/text()')         # マンションの種類
                loader.add_xpath('mansionClsStatus',        'div[2]/div[6]/div[4]/span/text()')         # マンションの種類(現況)
                loader.add_xpath('mansionStructure',        'div[2]/div[7]/div[2]/span/text()')         # マンションの構造
                loader.add_xpath('mansionStructureStatus',  'div[2]/div[7]/div[4]')                     # マンションの構造(現況)
                loader.add_xpath('mansionFloorArea',        'div[2]/div[8]/div[2]/span/node()')         # マンションの専有面積
                loader.add_xpath('mansionFloorAreaStatus',  'div[2]/div[8]/div[4]/span/node()')         # マンションの専有面積(現況)
                loader.add_xpath('mansionRoomArrangement',  'div[2]/div[9]/div[2]/span/node()')         # マンションの間取り
                loader.add_xpath('mansionPossessor',        'div[2]/div[9]/div[4]/span/node()')         # マンションの敷地利用権    
                loader.add_xpath('mansionControlCost',      'div[2]/div[10]/div[2]/span/text()')        # マンションの管理費
                loader.add_xpath('mansionBalconyArea',      'div[2]/div[10]/div[4]/span/node()')        # マンションのバルコニー面積
                loader.add_xpath('mansionOthersSiteUse',    'div[2]/div[11]/div[2]/span/text()')        # マンションの占有者
                loader.add_xpath('mansionBuildingAge',      'div[2]/div[11]/div[4]/span/text()')        # マンションの築年月
                loader.add_xpath('mansionFloor',            'div[2]/div[12]/div[2]/span/text()')        # マンションの階
                loader.add_xpath('mansionTotalUnits',       'div[2]/div[12]/div[4]/span/text()')        # マンションの総戸数
                loader.add_xpath('mansionEquity',           'div[2]/div[13]/div[2]/span/node()')        # マンションの持分
            elif ('建物' in str(saleCls)):
                loader.add_value('thingCls',                '2')                                        # 種別コード
                loader.add_xpath('thingType',               'div[2]/div[1]/div[2]/span[1]/text()')      # 種別
                loader.add_xpath('thingKindAttribute1',     'div[2]/div[1]/div[2]/span[2]/text()')      
                loader.add_xpath('thingKindAttribute2',     'div[2]/div[1]/div[2]/span[3]/text()')
                loader.add_xpath('thingNo',                 'div[2]/div[2]/div[2]/text()')              # 物件番号
                loader.add_xpath('address',                 'div[2]/div[3]/div[2]/span/text()')         # 所在地
                loader.add_xpath('streetNo',                'div[2]/div[4]/div[2]/text()')              # 番地、家屋番号
                loader.add_xpath('detachedCls',             'div[2]/div[5]/div[2]/span/text()')         # 建物の種類
                loader.add_xpath('detachedClsStatus',       'div[2]/div[5]/div[4]/span/text()')         # 建物の種類(現況)
                loader.add_xpath('detachedStructure',       'div[2]/div[6]/div[2]/span/text()')         # 建物の構造
                loader.add_xpath('detachedStructureStatus', 'div[2]/div[6]/div[4]')                     # 建物の構造(現況)
                loader.add_xpath('detachedFloorArea',       'div[2]/div[7]/div[2]/span/node()')         # 建物の床面積
                loader.add_xpath('detachedFloorAreaStatus', 'div[2]/div[7]/div[4]/span/node()')         # 建物の床面積(現況)
                loader.add_xpath('detachedRoomArrangement', 'div[2]/div[8]/div[2]/span/text()')         # 建物の間取り
                loader.add_xpath('detachedPossessor',       'div[2]/div[8]/div[4]/span/text()')         # 建物の敷地利用権  
                loader.add_xpath('detachedOthersSiteUse',   'div[2]/div[9]/div[2]/span/text()')         # 建物の占有者
                loader.add_xpath('detachedBuildingAge',     'div[2]/div[9]/div[4]/span/text()')         # 建物の築年月  
                loader.add_xpath('detachedEquity',          'div[2]/div[10]/div[2]/span/text()')        # 建物の持分  
            else:
                loader.add_value('thingCls',                '4')                                          # 種別コード
                loader.add_xpath('thingType',               'div[2]/div[1]/div[2]/span[1]/text()')        # 種別
                loader.add_xpath('thingKindAttribute1',     'div[2]/div[1]/div[2]/span[2]/text()')
                loader.add_xpath('thingKindAttribute2',     'div[2]/div[1]/div[2]/span[3]/text()')
                loader.add_xpath('thingNo',                 'div[2]/div[2]/div[2]/text()')                # 物件番号
                loader.add_xpath('address',                 'div[2]/div[3]/div[2]/span/text()')           # 所在地
                loader.add_xpath('streetNo',                'div[2]/div[4]/div[2]/text()')                # 番地
            items.append(loader.load_item())
        return items

    # ダウンロード、サムネイルファイル
    def parse_property_thumbnails(self, response):
        # パラメータ情報
        courtId = response.meta['courtId']
        saleUnitId = response.meta['saleUnitId']
        court = response.meta['court']
        prefecturesId = court['prefecturesId']
        # ダウンロードファイル名
        attachment = os.path.basename(response.url)
        # 保存先ルートを取得
        saved_root = 'download'
        # 保存先パスを作成
        saved_path = prefecturesId
        saved_path = os.path.join(saved_path, courtId)
        saved_path = os.path.join(saved_path, f'{prefecturesId}_{courtId}_{saleUnitId}')
        saved_file = os.path.join(saved_root, saved_path)
        os.makedirs(saved_file, mode=0o777, exist_ok=True)
        if not os.path.exists(saved_file):
            # 保存先パス失敗
            pass
        else:
            # ダウンロードファイルを保存
            saved_file = os.path.join(saved_file, attachment)
            with open(saved_file, 'wb') as pdf:
                pdf.write(response.body)    
                pdf.close()

    # ダウンロード、3点セット（物件明細書，現況調査報告書及び評価書等）PDFファイル
    def parse_property_pdf(self, response):
        # パラメータ情報
        courtId = response.meta['courtId']
        saleUnitId = response.meta['saleUnitId']
        court = response.meta['court']
        prefecturesId = court['prefecturesId']
        # ダウンロードファイル名
        attachment = self.get_response_attachment(response)
        # 保存先ルートを取得
        saved_root = 'download'
        # 保存先パスを作成
        saved_path = prefecturesId
        saved_path = os.path.join(saved_path, courtId)
        saved_path = os.path.join(saved_path, f'{prefecturesId}_{courtId}_{saleUnitId}')
        saved_file = os.path.join(saved_root, saved_path)
        os.makedirs(saved_file, mode=0o777, exist_ok=True)
        if not os.path.exists(saved_file):
            # 保存先パス失敗
            pass
        else:
            # ダウンロードファイルを保存
            saved_file = os.path.join(saved_file, attachment)
            with open(saved_file, 'wb') as pdf:
                pdf.write(response.body)    
                pdf.close()
            # ダウンロードファイルサイズ
            saved_size = os.path.getsize(saved_file)
            # 参照データ情報
            loader = ItemLoader(item=BitPropertyPDF()) 
            loader.add_value('prefecturesId', prefecturesId)    # 都道府県コード
            loader.add_value('courtId',       courtId)          # 裁判所コード
            loader.add_value('saleUnitId',    saleUnitId)       # 物件識別コード
            loader.add_value('savedRoot',     saved_root)       # 保存先ルートパス
            loader.add_value('savedPath',     saved_path)       # 保存先パス
            loader.add_value('savedFile',     attachment)       # ファイル名
            loader.add_value('savedSize',     saved_size)       # ファイルサイズ
            yield loader.load_item()

    # 売却結果情報(一覧)
    def parse_result(self, response):
        # ページ階層表示
        hierarchy = response.meta['hierarchy']
        self.logger.info(' > '.join(hierarchy))
        # パラメータ情報
        cookies  = self.get_response_cookies(response)
        formdata = self.get_response_formdata(response, 'resultDetailForm')
        # 都道府県コード、裁判所コード
        prefecturesId = self.get_formdata_value(formdata, 'prefecturesId')
        courtId       = self.get_formdata_value(formdata, 'courtId')
        #saleScdId
        #saleType 期間(=1),特売(=2)
        saleScdId = self.get_formdata_value(formdata, 'saleScdId')
        saleType  = self.get_formdata_value(formdata, 'saleType')
        # 売却結果
        for element in response.xpath('//*[@id="resultDetailForm"]/div/div/div/div/div'):
            loader = ItemLoader(item=BitResultItem(), selector=element)
            loader.add_value('document',               element.get())
            loader.add_value('prefecturesId',          prefecturesId)
            loader.add_value('courtId',                courtId)
            loader.add_value('saleScdId',              saleScdId)
            loader.add_value('saleType',               saleType)
            loader.add_xpath('saleClsDisp',            'div[1]/div[1]/p/span/text()')
            loader.add_xpath('caseNoText',             'div[1]/div[2]/p/text()')
            loader.add_xpath('saleAmountDisp',         'div[2]/div/div[1]/div/div[1]/p[2]/text()')
            loader.add_xpath('saleStandardAmountDisp', 'div[2]/div/div[1]/div/div[2]/p[2]/text()')
            loader.add_xpath('address',                'div[2]/div/div[2]/p/text()')            
            loader.add_xpath('thingNoList',            'div[2]/div/div[3]/ul/li[1]/div[2]/text()')
            loader.add_xpath('saleStatusDisp',         'div[2]/div/div[3]/ul/li[2]/div[2]/text()')
            if ('1' == str(saleType)):     # 期間入札
                loader.add_xpath('bitUsers',           'div[2]/div/div[3]/ul/li[3]/div[2]/text()')
                loader.add_xpath('bitUserClsDisp',     'div[2]/div/div[3]/ul/li[4]/div[2]/text()')
            elif ('2' == str(saleType)):   # 特別売却
                loader.add_xpath('bitUserClsDisp',     'div[2]/div/div[3]/ul/li[3]/div[2]/text()')
            yield loader.load_item()
        # 次ページへ移動
        if self.has_result_next_page(formdata):
            post_action = '/app/resultlist/pr002/h03'
            post_url    = response.urljoin(post_action)
            yield scrapy.FormRequest(post_url, self.parse_result, 
                method='POST',
                cookies=cookies,
                formdata=formdata,
                meta={ 
                    'cookies': cookies.copy(),
                    'hierarchy': hierarchy,
                    'dont_merge_cookies': True,
                },
                errback=self.errback,
                dont_filter=True,
            )

    # 売却結果情報、次ページチェック
    def has_result_next_page(self, formdata):
        pageSize   = self.get_formdata_pageSize(formdata)
        currPage   = self.get_formdata_currentPage(formdata)
        totalCount = self.get_formdata_totalCount(formdata)
        pagesCount = pageSize * currPage
        if (0 < pagesCount and pagesCount < totalCount):
            formdata['currPage']    = f'{currPage+1}'
            formdata['saleClsList'] = ''
            return True
        return False
        
   # cookies パラメータ取得
    def get_response_cookies(self, response):
        cookies = {}
        for element in response.headers.getlist('Set-Cookie'):
            cookie = element.decode('utf-8').split(';')[0].split('=')
            if (cookie[0] != '' and cookie[1] != ''):
                cookies[cookie[0]] = cookie[1]
        return cookies

    # form input パラメータ取得
    def get_response_formdata(self, response, formId):
        formdata = {}
        for element in response.xpath(f'//form[@id="{formId}"]/descendant::*[self::input or self::select]'): 
            name  = element.xpath('@name').get() 
            value = element.xpath('@value').get()
            value = value if value is not None else ''
            if (name is not None):
                formdata[name] = value
        # 指定されたformIdが存在しない場合
        if (not formdata):
            for element in response.xpath(f'//form/descendant::*[self::input or self::select]'): 
                name  = element.xpath('@name').get() 
                value = element.xpath('@value').get()
                value = value if (value is not None) else ''
                if (name is not None):
                    formdata[name] = value
        return formdata

    # form input パラメータ取得
    def get_response_jsondata(self, response, formId):
        formdata = {}
        for element in response.xpath(f'//form[@id="{formId}"]/descendant::*[self::input or self::select]'): 
            id    = element.xpath('@id').get() 
            value = element.xpath('@value').get()
            value = value if value is not None else ''
            if (id is not None):
                formdata[id] = value
        # 指定されたformIdが存在しない場合
        if (not formdata):
            for element in response.xpath(f'//form/descendant::*[self::input or self::select]'): 
                id    = element.xpath('@id').get() 
                value = element.xpath('@value').get()
                value = value if (value is not None) else ''
                if (id is not None):
                    formdata[id] = value
        return formdata

    # ダウンロードファイル名を取得
    def get_response_attachment(self, response):
        key = b'Content-Disposition'
        if (key in response.headers):
            attachment = response.headers[key].decode('utf-8')
            filename   = attachment.split('=')
            if (0 < len(filename)):
                return filename[1]
        return ''

    # formdata値の取得
    def get_formdata_value(self, formdata, name):
        if (name in formdata):
            return formdata[name]
        return ''

    # formdata値の物件総数の取得
    def get_formdata_totalCount(self, formdata):
        if ('totalCount' in formdata):
            return utils.to_int_def(formdata['totalCount'])
        return 0

    # formdata値の物件表示件数の取得
    def get_formdata_pageSize(self, formdata):
        if ('pageSize' in formdata):
            return utils.to_int_def(formdata['pageSize'])
        return 0

    # formdata値の物件ページIndexの取得
    def get_formdata_currentPage(self, formdata):
        if ('currPage' in formdata):
            return utils.to_int_def(formdata['currPage'])
        elif 'currentPage' in formdata:
            return utils.to_int_def(formdata['currentPage'])
        return 0

    # formdata値の物件パラメータの取得
    def get_formdata_resultList(self, formdata, key, index):
        listKey = f'resultList[{index}].{key}'
        if (listKey in formdata):
            return formdata[listKey]
        result  = []
        listKey = f'resultList[{index}].{key}[{len(result)}]'
        while (listKey in formdata):
            result.append(formdata[listKey])
            listKey = f'resultList[{index}].{key}[{len(result)}]'    
        if (0 < len(result)):
            return result
        return ''
