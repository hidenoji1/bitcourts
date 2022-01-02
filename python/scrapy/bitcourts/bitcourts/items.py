# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# 競売物件
class BitPropertyItem(scrapy.Item):
    document = scrapy.Field() 
    saleCls = scrapy.Field()                            # 売却種別(1:土地,2:戸建て,3:マンション,4:その他)
    saleUnitId = scrapy.Field()                         # 物件識別コード(PK)
    kindAttributeCls = scrapy.Field()                   # 売却種別属性(1:ゴルフ場,2:宿泊施設,3:工場)
    note = scrapy.Field()                               # 備考
    blockId = scrapy.Field()                            # 地域コード
    blockNm = scrapy.Field()                            # 地域名
    prefecturesId = scrapy.Field()                      # 都道府県コード
    prefecturesNm = scrapy.Field()                      # 都道府県名
    courtId = scrapy.Field()                            # 裁判所コード(PK)
    courtNm = scrapy.Field()                            # 裁判所名
    caseNoText = scrapy.Field()                         # 事件番号
    caseNoLink = scrapy.Field()                         # 事件番号(リンクテキスト)
    caseNoList = scrapy.Field()                         # 事件番号(リスト)
    perusalStartDate = scrapy.Field()                   # 閲覧開始日
    perusalStartDateDisp = scrapy.Field()               # 閲覧開始日(表示)
    bidStartDate = scrapy.Field()                       # 入札期間(開始日)
    bidEndDate = scrapy.Field()                         # 入札期間(終了日)
    bidPeriod = scrapy.Field()                          # 入札期間
    specialSaleStartDate = scrapy.Field()               # 特別売却期間(開始日)
    specialSaleEndDate = scrapy.Field()                 # 特別売却期間(終了日)
    specialSalePeriod = scrapy.Field()                  # 特別売却期間
    specialSalePerusalStartDate = scrapy.Field()        # 特別売却、閲覧開始日
    specialSalePerusalStartDateDisp = scrapy.Field()    # 特別売却、閲覧開始日(表示)
    listImageNm = scrapy.Field()                        # サムネイル
    saleStandardAmount = scrapy.Field()                 # 売却基準価額
    saleStandardAmountDisp = scrapy.Field()             # 売却基準価額(表示)
    guaranteeAmount = scrapy.Field()                    # 買受申出保証金
    guaranteeAmountDisp = scrapy.Field()                # 買受申出保証金(表示)
    address = scrapy.Field()                            # 住所
    streetNo = scrapy.Field()                           # 丁目、番地、枝番
    evaluationRoute1 = scrapy.Field()                   # 評価書上の交通１
    evaluationRoute2 = scrapy.Field()                   # 評価書上の交通２
    evaluationRoute3 = scrapy.Field()                   # 評価書上の交通３
    thingNo = scrapy.Field()                            # 物件番号
    thingCls = scrapy.Field()                           # 物件種別
    outOfSaleThingFlg = scrapy.Field()                  # 売却外物件フラグ
    outOfSaleThingInformation = scrapy.Field()          # 売却外物件
    useArea1 = scrapy.Field()                           # 用途地域１フラグ
    useArea1Information = scrapy.Field()                # 用途地域１
    useArea2 = scrapy.Field()                           # 用途地域２フラグ
    useArea2Information = scrapy.Field()                # 用途地域２
    landArea = scrapy.Field()                           
    landAreaDispFlg = scrapy.Field()
    area = scrapy.Field()
    areaFlg = scrapy.Field()
    roomArrangement = scrapy.Field()
    roomArrangementDispFlg = scrapy.Field()
    siteUseAuthority = scrapy.Field()
    stopInformation = scrapy.Field()
    farmlandFlg = scrapy.Field()
    farmlandInformation = scrapy.Field()
    roofSaleFlg = scrapy.Field()
    roofSaleInformation = scrapy.Field()
    tempAreaFlg = scrapy.Field()
    tempAreaInformation = scrapy.Field()
    periodBidStatus = scrapy.Field()
    specialSaleStatus = scrapy.Field()
    saleStatus = scrapy.Field()                         # 売却区分(1:期間入札,2:特別売却)
    saleStatusDisp = scrapy.Field()                     # 売却区分(テキスト)
    latitude = scrapy.Field()                           # 緯度
    longitude = scrapy.Field()                          # 経度
    landKind = scrapy.Field()
    landCls = scrapy.Field()
    kindAttributeClsClass = scrapy.Field()
    surroundingMapDispFlg = scrapy.Field()
    thingNoTypeList = scrapy.Field()                    # 物件番号、種別
    thingNoTypeProList = scrapy.Field()                 # 物件番号、種別(詳細)
    checkTenderDate = scrapy.Field()                    # 開札期日
    checkTenderDateDisp = scrapy.Field()                # 開札期日(表示)
    listImageFlg = scrapy.Field()
    saleGroupId = scrapy.Field()

# 競売物件、ヘッダー
class BitPropertyHeaderItem(scrapy.Item):
    saleUnitId = scrapy.Field()                         # 物件識別コード(PK)
    courtId = scrapy.Field()                            # 裁判所コード(PK)
    saleStatusDisp = scrapy.Field()                     # 売却区分(テキスト)
    caseNoLink = scrapy.Field()                         # 事件番号(リンクテキスト)   
    saleStandardAmountDisp = scrapy.Field()             # 売却基準価額(表示)
    guaranteeAmountDisp = scrapy.Field()                # 買受申出保証金(表示)    
    purchaseableAmountDisp = scrapy.Field()             # 買取可能価格(表示)    
    announcementStartDateDisp = scrapy.Field()          # 公示開始日(表示)
    perusalStartDateDisp = scrapy.Field()               # 閲覧開始日(表示)
    bidPeriod = scrapy.Field()                          # 入札期間
    checkTenderDateDisp = scrapy.Field()                # 開札期日(表示)
    saleDecisionDateDisp = scrapy.Field()               # 売却決定期日(表示)
    specialSalePerusalStartDateDisp = scrapy.Field()    # 特別売却、閲覧開始日(表示)
    specialSalePeriod = scrapy.Field()                  # 特別売却期間
    referenceRoute1 = scrapy.Field()                    # 参考交通１
    referenceRoute2 = scrapy.Field()                    # 参考交通２
    referenceRoute3 = scrapy.Field()                    # 参考交通３
    referenceRoute4 = scrapy.Field()                    # 参考交通４
    referenceRoute5 = scrapy.Field()                    # 参考交通５

# 競売物件、詳細
class BitPropertyDetailItem(scrapy.Item):
    document = scrapy.Field()                           # HTMLドキュメント
    prefecturesId = scrapy.Field()                      # 都道府県コード
    courtId = scrapy.Field()                            # 裁判所コード
    saleUnitId = scrapy.Field()                         # 物件識別コード  
    thingCls = scrapy.Field()                           # 物件種別
    thingNo = scrapy.Field()                            # 物件番号
    thingType = scrapy.Field()                          # 売却種別
    thingKindAttribute1 = scrapy.Field()
    thingKindAttribute2 = scrapy.Field()
    address = scrapy.Field()                            # 所在地
    streetNo = scrapy.Field()                           # 丁目、番地、枝番、家屋番号
    # 土地
    landCls = scrapy.Field()                            # 土地の地目
    landClsStatus = scrapy.Field()                      # 土地の地目(現況)
    landConditionCls = scrapy.Field()                   # 土地の利用状況
    landLandArea = scrapy.Field()                       # 土地の面積
    landLandAreaStatus = scrapy.Field()                 # 土地の面積(現況)
    landUseArea = scrapy.Field()                        # 土地の用途地域
    landBuildingCoverage = scrapy.Field()               # 土地の建ぺい率
    landFloorArea = scrapy.Field()                      # 土地の容積率
    landEquity = scrapy.Field()                         # 土地の持分
    # 戸建て
    detachedCls = scrapy.Field()                        # 建物の種類
    detachedClsStatus = scrapy.Field()                  # 建物の種類(現況)
    detachedStructure = scrapy.Field()                  # 建物の構造
    detachedStructureStatus = scrapy.Field()            # 建物の構造(現況)
    detachedFloorArea = scrapy.Field()                  # 建物の床面積
    detachedFloorAreaStatus = scrapy.Field()            # 建物の床面積(現況)
    detachedRoomArrangement = scrapy.Field()            # 建物の間取り
    detachedPossessor = scrapy.Field()                  # 建物の敷地利用権    
    detachedOthersSiteUse = scrapy.Field()              # 建物の占有者
    detachedBuildingAge = scrapy.Field()                # 建物の築年月
    detachedEquity = scrapy.Field()                     # 建物の持分
    # マンション
    mansionBuildingNo = scrapy.Field()                  # マンションの建物番号
    mansionCls = scrapy.Field()                         # マンションの種類
    mansionClsStatus = scrapy.Field()                   # マンションの種類(現況)
    mansionStructure = scrapy.Field()                   # マンションの構造
    mansionStructureStatus = scrapy.Field()             # マンションの構造(現況)
    mansionFloorArea = scrapy.Field()                   # マンションの専有面積
    mansionFloorAreaStatus = scrapy.Field()             # マンションの専有面積(現況)
    mansionRoomArrangement = scrapy.Field()             # マンションの間取り
    mansionPossessor = scrapy.Field()                   # マンションの敷地利用権    
    mansionControlCost = scrapy.Field()                 # マンションの管理費
    mansionBalconyArea = scrapy.Field()                 # マンションのバルコニー面積
    mansionOthersSiteUse = scrapy.Field()               # マンションの占有者
    mansionBuildingAge = scrapy.Field()                 # マンションの築年月
    mansionFloor = scrapy.Field()                       # マンションの階
    mansionTotalUnits = scrapy.Field()                  # マンションの総戸数
    mansionEquity = scrapy.Field()                      # マンションの持分
    # その他
    otherLandCls = scrapy.Field()
    otherLandConditionClsList = scrapy.Field()
    otherLandArea = scrapy.Field()

# 3点セット（物件明細書，現況調査報告書及び評価書等）PDFファイル
class BitPropertyPDF(scrapy.Item):
    prefecturesId = scrapy.Field()              # 都道府県コード
    courtId = scrapy.Field()                    # 裁判所コード
    saleUnitId = scrapy.Field()                 # 物件識別コード 
    savedRoot = scrapy.Field()                  # 保存先ルート
    savedPath = scrapy.Field()                  # 保存先パス
    savedFile = scrapy.Field()                  # ファイル名
    savedSize = scrapy.Field()                  # ファイルサイズ    

# 売却結果
class BitResultItem(scrapy.Item):
    document = scrapy.Field()                   # HTMLドキュメント
    prefecturesId = scrapy.Field()              # 都道府県コード
    courtId = scrapy.Field()                    # 裁判所コード
    saleScdId = scrapy.Field()
    saleType = scrapy.Field()                   # 売却区分(1:期間入札,2:特別売却)
    saleClsDisp = scrapy.Field()                # 売却種別
    caseNoText = scrapy.Field()                 # 事件番号           
    saleStandardAmountDisp = scrapy.Field()     # 売却基準価額
    saleAmountDisp = scrapy.Field()             # 売却価額
    address = scrapy.Field()                    # 所在地
    thingNoList = scrapy.Field()                # 物件番号   
    saleStatusDisp = scrapy.Field()             # 落札結果
    bitUsers = scrapy.Field()                   # 入札者数（人）
    bitUserClsDisp = scrapy.Field()             # 落札者資格

