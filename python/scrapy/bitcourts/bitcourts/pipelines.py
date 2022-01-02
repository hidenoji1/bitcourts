# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import scrapy
import logging
import sys
import json
import mojimoji
from items import *
from tables import *
from utils import utils
from itemadapter import ItemAdapter
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime

def to_str(values, default=None, delimiter=''):
    if (values is None):
        return default
    return delimiter.join(values)

def to_datetime(values, default=None):
    try:
        result = datetime.strptime(''.join(values), '%Y-%m-%d %H:%M:%S') 
    except ValueError:
        result = default
    return result

class BitCourtsBasePipeline(object):
    # メンバ変数
    session   = None    # セッション
    bulkLimit = 10      # 保持数 
    caches    = []      # キャッシュリスト
    
    # データベースセッション開始
    def open_spider(self, spider):
        try:
            self.session = Session(bind=spider.engine, autocommit=False, autoflush=True)    
            self.caches  = [] 
        except:
            errorList = sys.exc_info()
            for error in errorList:  
                print(error)          
                
    # データベースセッション終了
    def close_spider(self, spider):
        try:
            if (0 < len(self.caches)):
                self.session.commit()
                self.caches.clear()
        except:
            errorList = sys.exc_info()
            for error in errorList:            
                print(error)
            self.session.rollback()
        finally:
            self.session.close()

    # コミット
    def cache_commit(self, item, spider):
        # キャッシュ作成
        cache = json.dumps(dict(item), sort_keys=True, ensure_ascii=False)
        self.caches.append(cache)
        # コミット
        if (self.bulkLimit <= len(self.caches)):
            self.session.commit()
            self.caches.clear()

    # ロールバック
    def cache_rollback(self, item, spider):
        # コミット失敗、キャッシュ保存
        errorList = sys.exc_info()
        for error in errorList:            
            print(error)
        self.session.rollback()
        self.caches.clear()

#
class BitCourtsValidations(object):
    #
    def process_item(self, item, spider):
        if isinstance(item, BitPropertyItem):
            for key in item.fields.keys():
                if (key not in item):
                    item[key] = None
        elif isinstance(item, BitPropertyHeaderItem):
            for key in item.fields.keys():
                if (key not in item):
                    item[key] = None                    
        elif isinstance(item, BitPropertyDetailItem):
            for key in item.fields.keys():
                if (key not in item):
                    item[key] = ''
                elif (item[key] is None):
                    item[key] = ''
        elif isinstance(item, BitPropertyPDF):
            for key in item.fields.keys():
                if (key not in item):
                    item[key] = None
        elif isinstance(item, BitResultItem):
            for key in item.fields.keys():
                if (key not in item):
                    item[key] = None
        return item

#
class BitPropertyPipeline(BitCourtsBasePipeline):   
    #
    def process_item(self, item, spider):
        if isinstance(item, BitPropertyItem):
            self.process_in(item, spider)   
        return item
    #
    def process_in(self, item, spider):
        try:
            # データ存在チェック
            courtId    = utils.to_str(item['courtId'],    '')
            saleUnitId = utils.to_str(item['saleUnitId'], '')
            row = self.session.query(BitProperties).filter(
                and_(
                    BitProperties.courtId   ==courtId,
                    BitProperties.saleUnitId==saleUnitId,
                )
            ).one_or_none()
            # データ更新/追加
            if (row is not None):
                row = self.dumps(row, item) 
                row.updated = datetime.now()
            else:
                row = self.dumps(BitProperties(), item)
                self.session.add(row)
            self.cache_commit(item, spider)
        except:
            self.cache_rollback(item, spider)
    #
    def dumps(self, row, item):       
        row.saleUnitId = to_str(item['saleUnitId'])
        row.courtId = to_str(item['courtId'])
        row.courtNm = to_str(item['courtNm'])
        row.prefecturesId = to_str(item['prefecturesId'])
        row.prefecturesNm = to_str(item['prefecturesNm'])
        row.blockId = to_str(item['blockId'])
        row.blockNm = to_str(item['blockNm'])
        row.saleCls = to_str(item['saleCls'])
        row.kindAttributeCls = to_str(item['kindAttributeCls'])
        row.note = to_str(item['note'])
        row.caseNoText = to_str(item['caseNoText'])
        row.caseNoLink = to_str(item['caseNoLink'])
        row.caseNoList = to_str(item['caseNoList'], None, '<br>')
        row.perusalStartDate = to_datetime(item['perusalStartDate'])
        row.perusalStartDateDisp = to_str(item['perusalStartDateDisp'])
        row.bidStartDate = to_datetime(item['bidStartDate'])
        row.bidEndDate = to_datetime(item['bidEndDate'])
        row.bidPeriod = to_str(item['bidPeriod'])
        row.specialSaleStartDate = to_datetime(item['specialSaleStartDate'])
        row.specialSaleEndDate = to_datetime(item['specialSaleEndDate'])
        row.specialSalePeriod = to_str(item['specialSalePeriod'])
        row.specialSalePerusalStartDate = to_datetime(item['specialSalePerusalStartDate'])
        row.specialSalePerusalStartDateDisp = to_str(item['specialSalePerusalStartDateDisp'])
        row.listImageNm = to_str(item['listImageNm'])
        row.saleStandardAmount = to_str(item['saleStandardAmount'])
        row.saleStandardAmountDisp = to_str(item['saleStandardAmountDisp'])
        row.guaranteeAmount = to_str(item['guaranteeAmount'])
        row.guaranteeAmountDisp = to_str(item['guaranteeAmountDisp'])
        row.address = to_str(item['address'])
        row.streetNo = to_str(item['streetNo'])
        row.evaluationRoute1 = to_str(item['evaluationRoute1'])
        row.evaluationRoute2 = to_str(item['evaluationRoute2'])
        row.evaluationRoute3 = to_str(item['evaluationRoute3'])
        row.thingNo = to_str(item['thingNo'])
        row.thingCls = to_str(item['thingCls'])
        row.outOfSaleThingFlg = to_str(item['outOfSaleThingFlg'])
        row.outOfSaleThingInformation = to_str(item['outOfSaleThingInformation'])
        row.useArea1 = to_str(item['useArea1'])
        row.useArea1Information = to_str(item['useArea1Information'])
        row.useArea2 = to_str(item['useArea2'])
        row.useArea2Information = to_str(item['useArea2Information'])
        row.landArea = to_str(item['landArea'])
        row.landAreaDispFlg = to_str(item['landAreaDispFlg'])
        row.area = to_str(item['area'])
        row.areaFlg = to_str(item['areaFlg'])
        row.roomArrangement = to_str(item['roomArrangement'])
        row.roomArrangementDispFlg = to_str(item['roomArrangementDispFlg'])
        row.siteUseAuthority = to_str(item['siteUseAuthority'])
        row.stopInformation = to_str(item['stopInformation'])
        row.farmlandFlg = to_str(item['farmlandFlg'])
        row.farmlandInformation = to_str(item['farmlandInformation'])
        row.roofSaleFlg = to_str(item['roofSaleFlg'])
        row.roofSaleInformation = to_str(item['roofSaleInformation'])
        row.tempAreaFlg = to_str(item['tempAreaFlg'])
        row.tempAreaInformation = to_str(item['tempAreaInformation'])
        row.periodBidStatus = to_str(item['periodBidStatus'])
        row.specialSaleStatus = to_str(item['specialSaleStatus'])
        row.saleStatus = to_str(item['saleStatus'])
        row.saleStatusDisp = to_str(item['saleStatusDisp'])
        row.latitude = to_str(item['latitude'])
        row.longitude = to_str(item['longitude'])
        row.landKind = to_str(item['landKind'])
        row.landCls = to_str(item['landCls'])
        row.kindAttributeClsClass = to_str(item['kindAttributeClsClass'])
        row.surroundingMapDispFlg = to_str(item['surroundingMapDispFlg'])
        row.thingNoTypeList = to_str(item['thingNoTypeList'], None, '<br>')
        row.thingNoTypeProList = to_str(item['thingNoTypeProList'], None, '<br>')
        row.checkTenderDate = to_datetime(item['checkTenderDate'])
        row.checkTenderDateDisp = to_str(item['checkTenderDateDisp'])
        row.listImageFlg = to_str(item['listImageFlg'])
        row.saleGroupId = to_str(item['saleGroupId'])
        return row

#
class BitPropertyHeaderPipeline(BitCourtsBasePipeline):   
    #
    def process_item(self, item, spider):
        if isinstance(item, BitPropertyHeaderItem):
            self.process_in(item, spider)   
        return item
    #
    def process_in(self, item, spider):
        try:
            # データ存在チェック
            courtId    = utils.to_str(item['courtId'],    '')
            saleUnitId = utils.to_str(item['saleUnitId'], '')
            row = self.session.query(BitPropertyHeaders).filter(
                and_(
                    BitPropertyHeaders.courtId   ==courtId,
                    BitPropertyHeaders.saleUnitId==saleUnitId,
                )
            ).one_or_none()
            # データ更新/追加
            if (row is not None):
                row = self.dumps(row, item) 
                row.updated = datetime.now()
            else:
                row = self.dumps(BitPropertyHeaders(), item)
                self.session.add(row)
            self.cache_commit(item, spider)
        except:
            self.cache_rollback(item, spider)
    #
    def dumps(self, row, item):       
        row.saleUnitId = utils.to_str(item['saleUnitId'])
        row.courtId = utils.to_str(item['courtId'])
        #row.saleStatus = ''
        row.saleStatusDisp = utils.to_str(item['saleStatusDisp'])
        row.caseNoLink = utils.to_str(item['caseNoLink'])
        row.saleStandardAmountDisp = utils.to_str(item['saleStandardAmountDisp'])
        #row.saleStandardAmount = utils.to_amount(item['saleStandardAmountDisp'])
        row.guaranteeAmountDisp = utils.to_str(item['guaranteeAmountDisp'])
        #row.guaranteeAmount = utils.to_amount(item['guaranteeAmountDisp'])
        row.purchaseableAmountDisp = utils.to_str(item['purchaseableAmountDisp'])
        #row.purchaseableAmount = utils.to_str(item['purchaseableAmountDisp'])
        row.announcementStartDateDisp = utils.to_str(item['announcementStartDateDisp'])
        #row.announcementStartDate = None
        row.perusalStartDateDisp = utils.to_str(item['perusalStartDateDisp'])
        #row.perusalStartDate = None
        row.bidPeriod = utils.to_str(item['bidPeriod'])
        row.checkTenderDateDisp = utils.to_str(item['checkTenderDateDisp'])
        #row.checkTenderDate = None
        row.saleDecisionDateDisp = utils.to_str(item['saleDecisionDateDisp'])
        #row.saleDecisionDate = None
        row.specialSalePerusalStartDateDisp = utils.to_str(item['specialSalePerusalStartDateDisp'])
        #row.specialSalePerusalStartDate = None
        row.specialSalePeriod = utils.to_str(item['specialSalePeriod'])
        row.referenceRoute1 = utils.to_str(item['referenceRoute1'])
        row.referenceRoute2 = utils.to_str(item['referenceRoute2'])
        row.referenceRoute3 = utils.to_str(item['referenceRoute3'])
        row.referenceRoute4 = utils.to_str(item['referenceRoute4'])
        row.referenceRoute5 = utils.to_str(item['referenceRoute5'])
        return row
#
class BitPropertyItemPipeline(object):
    #
    def __init__(self, settings):
        self.settings = settings
    #
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)

    def process_item(self, item, spider):
        if isinstance(item, BitPropertyItem):
            self.process_in(item, spider)   
        return item
    #
    def open_spider(self, spider):
        # データベースセッション開始
        self.session = Session(bind=spider.engine, autocommit=False, autoflush=True)    
        self.caches = [] 
    #
    def close_spider(self, spider):
        # データベースセッション終了
        try:
            self.session.commit()
            self.caches = [] 
        except:
            errorList = sys.exc_info()
            for error in errorList:
                print(error)
            self.session.rollback()
        finally:
            self.session.close()
    #
    def process_in(self, item, spider):
        try:
            # データ存在チェック
            courtId    = to_str(item['courtId'],    '')
            saleUnitId = to_str(item['saleUnitId'], '')
            row = self.session.query(BitProperties).filter(
                and_(
                    BitProperties.courtId   ==courtId,
                    BitProperties.saleUnitId==saleUnitId,
                )
            ).one_or_none()
            # データ更新/追加
            if (row is not None):
                row = self.dumps(row, item) 
                row.updated = datetime.now()
            else:
                row = self.dumps(BitProperties(), item)
                self.session.add(row)
            # キャッシュ作成
            cache = json.dumps(dict(item), sort_keys=True, ensure_ascii=False)
            self.caches.append(cache)
        except:
            errorList = sys.exc_info()
            for error in errorList:            
                print(error)
        # コミット
        try:
            if (10 <= len(self.caches) ):
                self.session.commit()
                self.caches.clear()
        except:
            errorList = sys.exc_info()
            for error in errorList:            
                print(error)
            self.session.rollback()
            self.caches.clear()
    #
    def dumps(self, row, item):       
        row.saleUnitId = to_str(item['saleUnitId'])
        row.courtId = to_str(item['courtId'])
        row.courtNm = to_str(item['courtNm'])
        row.prefecturesId = to_str(item['prefecturesId'])
        row.prefecturesNm = to_str(item['prefecturesNm'])
        row.blockId = to_str(item['blockId'])
        row.blockNm = to_str(item['blockNm'])
        row.saleCls = to_str(item['saleCls'])
        row.kindAttributeCls = to_str(item['kindAttributeCls'])
        row.note = to_str(item['note'])
        row.caseNoText = to_str(item['caseNoText'])
        row.caseNoLink = to_str(item['caseNoLink'])
        row.caseNoList = to_str(item['caseNoList'], None, '<br>')
        row.perusalStartDate = to_datetime(item['perusalStartDate'])
        row.perusalStartDateDisp = to_str(item['perusalStartDateDisp'])
        row.bidStartDate = to_datetime(item['bidStartDate'])
        row.bidEndDate = to_datetime(item['bidEndDate'])
        row.bidPeriod = to_str(item['bidPeriod'])
        row.specialSaleStartDate = to_datetime(item['specialSaleStartDate'])
        row.specialSaleEndDate = to_datetime(item['specialSaleEndDate'])
        row.specialSalePeriod = to_str(item['specialSalePeriod'])
        row.specialSalePerusalStartDate = to_datetime(item['specialSalePerusalStartDate'])
        row.specialSalePerusalStartDateDisp = to_str(item['specialSalePerusalStartDateDisp'])
        row.listImageNm = to_str(item['listImageNm'])
        row.saleStandardAmount = to_str(item['saleStandardAmount'])
        row.saleStandardAmountDisp = to_str(item['saleStandardAmountDisp'])
        row.guaranteeAmount = to_str(item['guaranteeAmount'])
        row.guaranteeAmountDisp = to_str(item['guaranteeAmountDisp'])
        row.address = to_str(item['address'])
        row.streetNo = to_str(item['streetNo'])
        row.evaluationRoute1 = to_str(item['evaluationRoute1'])
        row.evaluationRoute2 = to_str(item['evaluationRoute2'])
        row.evaluationRoute3 = to_str(item['evaluationRoute3'])
        row.thingNo = to_str(item['thingNo'])
        row.thingCls = to_str(item['thingCls'])
        row.outOfSaleThingFlg = to_str(item['outOfSaleThingFlg'])
        row.outOfSaleThingInformation = to_str(item['outOfSaleThingInformation'])
        row.useArea1 = to_str(item['useArea1'])
        row.useArea1Information = to_str(item['useArea1Information'])
        row.useArea2 = to_str(item['useArea2'])
        row.useArea2Information = to_str(item['useArea2Information'])
        row.landArea = to_str(item['landArea'])
        row.landAreaDispFlg = to_str(item['landAreaDispFlg'])
        row.area = to_str(item['area'])
        row.areaFlg = to_str(item['areaFlg'])
        row.roomArrangement = to_str(item['roomArrangement'])
        row.roomArrangementDispFlg = to_str(item['roomArrangementDispFlg'])
        row.siteUseAuthority = to_str(item['siteUseAuthority'])
        row.stopInformation = to_str(item['stopInformation'])
        row.farmlandFlg = to_str(item['farmlandFlg'])
        row.farmlandInformation = to_str(item['farmlandInformation'])
        row.roofSaleFlg = to_str(item['roofSaleFlg'])
        row.roofSaleInformation = to_str(item['roofSaleInformation'])
        row.tempAreaFlg = to_str(item['tempAreaFlg'])
        row.tempAreaInformation = to_str(item['tempAreaInformation'])
        row.periodBidStatus = to_str(item['periodBidStatus'])
        row.specialSaleStatus = to_str(item['specialSaleStatus'])
        row.saleStatus = to_str(item['saleStatus'])
        row.saleStatusDisp = to_str(item['saleStatusDisp'])
        row.latitude = to_str(item['latitude'])
        row.longitude = to_str(item['longitude'])
        row.landKind = to_str(item['landKind'])
        row.landCls = to_str(item['landCls'])
        row.kindAttributeClsClass = to_str(item['kindAttributeClsClass'])
        row.surroundingMapDispFlg = to_str(item['surroundingMapDispFlg'])
        row.thingNoTypeList = to_str(item['thingNoTypeList'], None, '<br>')
        row.thingNoTypeProList = to_str(item['thingNoTypeProList'], None, '<br>')
        row.checkTenderDate = to_datetime(item['checkTenderDate'])
        row.checkTenderDateDisp = to_str(item['checkTenderDateDisp'])
        row.listImageFlg = to_str(item['listImageFlg'])
        row.saleGroupId = to_str(item['saleGroupId'])
        return row

#
class BitPropertyHeaderItemPipeline(object):
    #
    def process_item(self, item, spider):
        if isinstance(item, BitPropertyHeaderItem):
            self.process_in(item, spider)   
        return item
    #
    def open_spider(self, spider):
        # データベースセッション開始
        self.session = Session(bind=spider.engine, autocommit=False, autoflush=True)    
        self.count = 0 
    #
    def close_spider(self, spider):
        # データベースセッション終了
        try:
            self.session.commit()
        except:
            self.session.rollback()
        finally:
            self.session.close()
    #
    def process_in(self, item, spider):
        try:
            # データ存在チェック
            courtId    = to_str(item['courtId'],    '')
            saleUnitId = to_str(item['saleUnitId'], '')
            row = self.session.query(BitPropertyHeaders).filter(
                and_(
                    BitPropertyHeaders.courtId   ==courtId,
                    BitPropertyHeaders.saleUnitId==saleUnitId,
                )
            ).one_or_none()
            # データ更新/追加
            if (row is not None):
                row = self.dumps(row, item) 
                row.updated = datetime.now()
            else:
                row = self.dumps(BitPropertyHeaders(), item)
                self.session.add(row)
            # キャッシュ作成
            cache = json.dumps(dict(item), sort_keys=True, ensure_ascii=False)
            self.caches.append(cache)
        except:
            errorList = sys.exc_info()
            for error in errorList:            
                print(error)
        # コミット
        try:
            if (10 <= len(self.caches) ):
                self.session.commit()
                self.caches.clear()
        except:
            errorList = sys.exc_info()
            for error in errorList:            
                print(error)
            self.session.rollback()
            self.count = 0  
    #
    def dumps(self, row, item):  
        return row     

#
class BitPropertyDetailItemPipeline(object):
    #
    def process_item(self, item, spider):
        if isinstance(item, BitPropertyDetailItem):
            self.process_in(item, spider)   
        return item
    #
    def process_in(self, item, spider):
        # データベースセッション開始
        self.session = Session(bind=spider.engine, autocommit=False, autoflush=True)    
        # ユニークキー取得
        prefecturesId = ''.join(item['prefecturesId'])
        courtId       = ''.join(item['courtId'])
        saleUnitId    = ''.join(item['saleUnitId'])
        thingCls      = ''.join(item['thingCls'])
        # テータ存在チェック
        row = None
        # row = spider.session.query(BitPropertyDetails.id).filter(
        #         and_(
        #             BitPropertyDetails.courtId   ==courtId, 
        #             BitPropertyDetails.saleUnitId==saleUnitId,
        #         )
        #     ).one_or_none()
        # テータ登録
        if row is not None:
            return
        else:
            row = BitPropertyDetails()
            row.prefecturesId = prefecturesId
            row.courtId = courtId
            row.saleUnitId = saleUnitId
            row.document = ''.join(item['document'])
            row.thingCls = ''.join(item['thingCls'])
            row.thingNo = ''.join(item['thingNo'])
            row.thingType = ''.join(item['thingType'])
            row.thingKindAttribute1 = to_str(item['thingKindAttribute1'])
            row.thingKindAttribute2 = to_str(item['thingKindAttribute2'])
            row.address = ''.join(item['address'])
            row.streetNo = ''.join(item['streetNo'])
            # 土地
            row.landCls = to_str(item['landCls'], '')
            row.landClsStatus = to_str(item['landClsStatus'], '')
            row.landConditionCls = to_str(item['landConditionCls'], '')
            row.landLandArea = to_str(item['landLandArea'], '')
            row.landLandAreaStatus = to_str(item['landLandAreaStatus'], '')
            row.landUseArea = to_str(item['landUseArea'], '')
            row.landBuildingCoverage = to_str(item['landBuildingCoverage'], '')
            row.landFloorArea = to_str(item['landFloorArea'], '')
            row.landEquity = to_str(item['landEquity'], '')
            # 戸建て
            row.detachedCls = ''.join(item['detachedCls'])
            row.detachedClsStatus = ''.join(item['detachedClsStatus'])
            row.detachedStructure = ''.join(item['detachedStructure'])
            row.detachedStructureStatus = ''.join(item['detachedStructureStatus'])
            row.detachedFloorArea = ''.join(item['detachedFloorArea'])
            row.detachedFloorAreaStatus = ''.join(item['detachedFloorAreaStatus'])
            row.detachedRoomArrangement = ''.join(item['detachedRoomArrangement'])
            row.detachedPossessor = ''.join(item['detachedPossessor'])
            row.detachedOthersSiteUse = ''.join(item['detachedOthersSiteUse'])
            row.detachedBuildingAge = ''.join(item['detachedBuildingAge'])
            row.detachedEquity = ''.join(item['detachedEquity'])
            # マンション
            row.mansionBuildingNo = ''.join(item['mansionBuildingNo'])
            row.mansionCls = ''.join(item['mansionCls'])
            row.mansionClsStatus = ''.join(item['mansionClsStatus'])
            row.mansionStructure = ''.join(item['mansionStructure'])
            row.mansionStructureStatus = ''.join(item['mansionStructureStatus'])
            row.mansionFloorArea = ''.join(item['mansionFloorArea'])
            row.mansionFloorAreaStatus = ''.join(item['mansionFloorAreaStatus'])
            row.mansionRoomArrangement = ''.join(item['mansionRoomArrangement'])
            row.mansionPossessor = ''.join(item['mansionPossessor'])
            row.mansionControlCost = ''.join(item['mansionControlCost'])
            row.mansionBalconyArea = ''.join(item['mansionBalconyArea'])
            row.mansionOthersSiteUse = ''.join(item['mansionOthersSiteUse'])
            row.mansionBuildingAge = ''.join(item['mansionBuildingAge'])
            row.mansionFloor = ''.join(item['mansionFloor'])
            row.mansionTotalUnits = ''.join(item['mansionTotalUnits'])
            row.mansionEquity = ''.join(item['mansionEquity'])
            # その他
            row.otherLandCls = ''.join(item['otherLandCls'])
            row.otherLandConditionClsList = ''.join(item['otherLandConditionClsList'])
            row.otherLandArea = ''.join(item['otherLandArea'])
            self.session.add(row)
        try:
            self.session.commit()
        except:
            self.session.rollback()
        finally:
            self.session.close()

#
class BitPropertyPdfPipeline(object):
    #
    def process_item(self, item, spider):
        if isinstance(item, BitPropertyPDF):
            self.process_in(item, spider)   
        return item
    #
    def process_in(self, item, spider):
        # ユニークキー取得
        prefecturesId = ''.join(item['prefecturesId'])
        courtId       = ''.join(item['courtId'])
        saleUnitId    = ''.join(item['saleUnitId'])
        # テータ存在チェック
        row = spider.session.query(BitPropertyPDFs.id).filter(
                and_(
                    BitPropertyPDFs.courtId   ==courtId, 
                    BitPropertyPDFs.saleUnitId==saleUnitId,
                )
            ).one_or_none()
        # テータ登録
        if row is not None:
            return
        else:
            row = BitPropertyPDFs()
            row.courtId = courtId
            row.saleUnitId = saleUnitId
            row.prefecturesId = prefecturesId
            row.savedRoot = ''.join(item['savedRoot'])
            row.savedPath = ''.join(item['savedPath'])
            row.savedFile = ''.join(item['savedFile'])
            row.savedSize = ''.join(item['savedSize'])
            spider.session.add(row)
            spider.session.flush()
        spider.session.commit()

#
class BitResultPipeline(BitCourtsBasePipeline):
    #
    def process_item(self, item, spider):
        if isinstance(item, BitResultItem):
            self.process_in(item, spider)   
        return item
    #
    def process_in(self, item, spider):
        try:
            # データ存在チェック
            courtId    = utils.to_str(item['courtId'])
            caseNoText = utils.to_str(item['caseNoText'])
            thingNos   = self.to_thingNos(item['thingNoList'])
            row = self.session.query(BitResults).filter(
                and_(
                    BitResults.courtId   ==courtId,
                    BitResults.caseNoText==caseNoText,
                    BitResults.thingNos  ==thingNos,
                )
            ).one_or_none()
            # データ更新/追加
            if (row is not None):
                row = self.dumps(row, item) 
                row.updated = datetime.now()
            else:
                row = self.dumps(BitResults(), item)
                self.session.add(row)
            self.cache_commit(item, spider)
        except:
            self.cache_rollback(item, spider)
    #
    def dumps(self, row, item):  
        row.document = utils.to_str(item['document'])
        row.prefecturesId = utils.to_str(item['prefecturesId'])
        row.courtId = utils.to_str(item['courtId'])
        row.saleType = utils.to_str(item['saleType'])
        row.saleClsDisp = utils.to_str(item['saleClsDisp'])
        row.caseNoText = utils.to_str(item['caseNoText'])
        row.saleStandardAmountDisp = utils.to_str(item['saleStandardAmountDisp'])
        row.saleStandardAmount = utils.to_amount(item['saleStandardAmountDisp'])
        row.saleAmountDisp = utils.to_str(item['saleAmountDisp'])
        row.saleAmount = utils.to_amount(item['saleAmountDisp'])
        row.address = utils.to_str(item['address'])
        row.thingNoList = utils.to_str(item['thingNoList'])
        row.thingNos = self.to_thingNos(item['thingNoList'])
        row.saleStatusDisp = utils.to_str(item['saleStatusDisp'])
        row.bitUsers = utils.to_str(item['bitUsers'])
        row.bitUserClsDisp = utils.to_str(item['bitUserClsDisp'])
        return row     

    #
    def to_thingNos(self, value):
        result = utils.to_str(value)
        result = mojimoji.zen_to_han(result)
        result = result.replace(' ', '')
        return result


