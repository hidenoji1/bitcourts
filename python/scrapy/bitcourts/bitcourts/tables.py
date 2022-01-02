from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()
	
# 競売物件
class BitProperties(Base):
    # テーブル名定義
    __tablename__ = 'bit_properties'
    # インデックス定義
    __table_args__ = (
        Index(
            'index_court_id_sale_unit_id',
            'court_id', 'sale_unit_id', unique=True,
        ),
    )
    # カラム定義
    id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    saleUnitId = Column('sale_unit_id', String(12), nullable=False)
    courtId = Column('court_id', String(6), nullable=False)
    courtNm = Column('court_nm', Text, nullable=True)
    prefecturesId = Column('prefectures_id', String(3), nullable=False)
    prefecturesNm = Column('prefectures_nm', Text, nullable=True)
    blockId = Column('block_id', Text, nullable=True)
    blockNm = Column('block_nm', Text, nullable=True)
    saleCls = Column('sale_cls', Text, nullable=True)
    kindAttributeCls = Column('kind_attribute_cls', Text, nullable=True)
    note = Column('note', Text, nullable=True)
    caseNoText = Column('case_no_text', Text, nullable=True)
    caseNoLink = Column('case_no_link', Text, nullable=True)
    caseNoList = Column('case_no_list', Text, nullable=True)
    perusalStartDate = Column('perusal_startdate', DateTime, nullable=True)
    perusalStartDateDisp = Column('perusal_startdate_disp', Text, nullable=True)
    bidStartDate = Column('bid_startdate', DateTime, nullable=True)
    bidEndDate = Column('bid_enddate', DateTime, nullable=True)
    bidPeriod = Column('bid_period', Text, nullable=True)
    specialSaleStartDate = Column('special_sale_startdate', DateTime, nullable=True)
    specialSaleEndDate = Column('special_sale_enddate', DateTime, nullable=True)
    specialSalePeriod = Column('special_sale_period', Text, nullable=True)
    specialSalePerusalStartDate = Column('special_sale_perusal_startdate', DateTime, nullable=True)
    specialSalePerusalStartDateDisp = Column('special_sale_perusal_startdate_disp', Text, nullable=True)
    listImageNm = Column('list_image_nm', Text, nullable=True)
    saleStandardAmount = Column('sale_standard_amount', Numeric(24,0), nullable=True)
    saleStandardAmountDisp = Column('sale_standard_amount_disp', Text, nullable=True)
    guaranteeAmount = Column('guarantee_amount', Numeric(24,0), nullable=True)
    guaranteeAmountDisp = Column('guarantee_amount_disp', Text, nullable=True)
    address = Column('address', Text, nullable=True)
    streetNo = Column('street_no', Text, nullable=True)
    evaluationRoute1 = Column('evaluation_route1', Text, nullable=True)
    evaluationRoute2 = Column('evaluation_route2', Text, nullable=True)
    evaluationRoute3 = Column('evaluation_route3', Text, nullable=True)
    thingNo = Column('thing_no', Text, nullable=True)
    thingCls = Column('thing_cls', Text, nullable=True)
    outOfSaleThingFlg = Column('out_of_sale_thing_flg', Text, nullable=True)
    outOfSaleThingInformation = Column('out_of_sale_thing_information', Text, nullable=True)
    useArea1 = Column('use_area1', Text, nullable=True)
    useArea1Information = Column('use_area1_information', Text, nullable=True)
    useArea2 = Column('use_area2', Text, nullable=True)
    useArea2Information = Column('use_area2_information', Text, nullable=True)
    landArea = Column('land_area', Text, nullable=True)
    landAreaDispFlg = Column('land_area_disp_flg', Text, nullable=True)
    area = Column('area', Text, nullable=True)
    areaFlg = Column('area_flg', Text, nullable=True)
    roomArrangement = Column('room_arrangement', Text, nullable=True)
    roomArrangementDispFlg = Column('room_arrangement_disp_flg', Text, nullable=True)
    siteUseAuthority = Column('site_use_authority', Text, nullable=True)
    stopInformation = Column('stop_information', Text, nullable=True)
    farmlandFlg = Column('farmland_flg', Text, nullable=True)
    farmlandInformation = Column('farmland_information', Text, nullable=True)
    roofSaleFlg = Column('roof_sale_flg', Text, nullable=True)
    roofSaleInformation = Column('roof_sale_information', Text, nullable=True)
    tempAreaFlg = Column('temp_area_flg', Text, nullable=True)
    tempAreaInformation = Column('temp_area_information', Text, nullable=True)
    periodBidStatus = Column('period_bid_status', Text, nullable=True)
    specialSaleStatus = Column('special_sale_status', Text, nullable=True)
    saleStatus = Column('sale_status', Text, nullable=True)
    saleStatusDisp = Column('sale_status_disp', Text, nullable=True)
    latitude = Column('latitude', Text, nullable=True)
    longitude = Column('longitude', Text, nullable=True)
    landKind = Column('land_kind', Text, nullable=True)
    landCls = Column('land_cls', Text, nullable=True)
    kindAttributeClsClass = Column('kind_attribute_cls_class', Text, nullable=True)
    surroundingMapDispFlg = Column('surrounding_map_disp_flg', Text, nullable=True)
    thingNoTypeList = Column('thing_no_type_list', Text, nullable=True)
    thingNoTypeProList = Column('thing_no_type_pro_list', Text, nullable=True)
    checkTenderDate = Column('check_tender_date', DateTime, nullable=True)
    checkTenderDateDisp = Column('check_tender_date_disp', Text, nullable=True)
    listImageFlg = Column('list_image_flg', Text, nullable=True)
    saleGroupId = Column('sale_group_id', Text, nullable=True)
    created = Column('created_at', DateTime, default=datetime.now(), nullable=False)
    updated = Column('updated_at', DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

# 競売物件、ヘッダ
class BitPropertyHeaders(Base):
    # テーブル名定義
    __tablename__ = 'bit_property_headers'
    # インデックス定義
    __table_args__ = (
        Index(
            'index_court_id_sale_unit_id',
            'court_id', 'sale_unit_id', unique=True,
        ),
    )
    # カラム定義
    id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    saleUnitId = Column('sale_unit_id', String(12), nullable=False)
    courtId = Column('court_id', String(6), nullable=False)
    saleStatus = Column('sale_status', String(2), nullable=True)
    saleStatusDisp = Column('sale_status_disp', Text, nullable=True)
    caseNoLink = Column('case_no_link', Text, nullable=True)
    saleStandardAmount = Column('sale_standard_amount', Numeric(24,0), nullable=True)
    saleStandardAmountDisp = Column('sale_standard_amount_disp', Text, nullable=True)
    guaranteeAmount = Column('guarantee_amount', Numeric(24,0), nullable=True)
    guaranteeAmountDisp = Column('guarantee_amount_disp', Text, nullable=True)
    purchaseableAmount = Column('purchaseable_amount', Numeric(24,0), nullable=True)
    purchaseableAmountDisp = Column('purchaseable_amount_disp', Text, nullable=True)
    announcementStartDate = Column('announcement_startdate', DateTime, nullable=True)
    announcementStartDateDisp = Column('announcement_startdate_disp', Text, nullable=True)
    perusalStartDate = Column('perusal_startdate', DateTime, nullable=True)
    perusalStartDateDisp = Column('perusal_startdate_disp', Text, nullable=True)
    bidPeriod = Column('bid_period', Text, nullable=True)
    checkTenderDate = Column('check_tender_date', DateTime, nullable=True)
    checkTenderDateDisp = Column('check_tender_date_disp', Text, nullable=True)
    saleDecisionDate = Column('sale_decision_date', DateTime, nullable=True)
    saleDecisionDateDisp = Column('sale_decision_date_disp', Text, nullable=True)
    specialSalePerusalStartDate = Column('special_sale_perusal_startdate', DateTime, nullable=True)
    specialSalePerusalStartDateDisp = Column('special_sale_perusal_startdate_disp', Text, nullable=True)
    specialSalePeriod = Column('special_sale_period', Text, nullable=True)
    referenceRoute1 = Column('reference_route1', Text, nullable=True)
    referenceRoute2 = Column('reference_route2', Text, nullable=True)
    referenceRoute3 = Column('reference_route3', Text, nullable=True)
    referenceRoute4 = Column('reference_route4', Text, nullable=True)
    referenceRoute5 = Column('reference_route5', Text, nullable=True)
    created = Column('created_at', DateTime, default=datetime.now(), nullable=False)
    updated = Column('updated_at', DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

# 競売物件、詳細
class BitPropertyDetails(Base):
    # テーブル名定義
    __tablename__ = 'bit_property_details'
    __table_args__ = (
        Index(
            'index_court_id_sale_unit_id_thing_no',
            'court_id', 'sale_unit_id', 'thing_no', unique=True,
        ),
    )
    # カラム定義
    id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    prefecturesId = Column('prefectures_id', String(3), nullable=False)
    courtId = Column('court_id', String(6), nullable=False)
    saleUnitId = Column('sale_unit_id', String(12), nullable=False)
    thingCls = Column('thing_cls', String(64), nullable=True)
    thingNo = Column('thing_no', String(64), nullable=True)
    thingType = Column('thing_type', Text, nullable=True)
    thingKindAttribute1 = Column('thing_kind_attribute1', Text, nullable=True)
    thingKindAttribute2 = Column('thing_kind_attribute2', Text, nullable=True)
    address = Column('address', Text, nullable=True)
    streetNo = Column('street_no', Text, nullable=True)
    # 土地
    landCls = Column('land_cls', Text, nullable=True)
    landClsStatus = Column('land_cls_status', Text, nullable=True)
    landConditionCls = Column('land_condition_cls', Text, nullable=True)
    landLandArea = Column('land_land_area', Text, nullable=True)
    landLandAreaStatus = Column('land_land_area_status', Text, nullable=True)
    landUseArea = Column('land_use_area', Text, nullable=True)
    landBuildingCoverage = Column('land_building_coverage', Text, nullable=True)
    landFloorArea = Column('land_floor_area', Text, nullable=True)
    landEquity = Column('land_equity', Text, nullable=True)
    # 戸建て
    detachedCls = Column('detached_cls', Text, nullable=True)
    detachedClsStatus = Column('detached_cls_status', Text, nullable=True)
    detachedStructure = Column('detached_structure', Text, nullable=True)
    detachedStructureStatus = Column('detached_structure_status', Text, nullable=True)
    detachedFloorArea = Column('detached_floor_area', Text, nullable=True)
    detachedFloorAreaStatus = Column('detached_floor_area_status', Text, nullable=True)
    detachedRoomArrangement = Column('detached_room_arrangement', Text, nullable=True)
    detachedPossessor = Column('detached_possessor', Text, nullable=True)  
    detachedOthersSiteUse = Column('detached_others_siteuse', Text, nullable=True)
    detachedBuildingAge = Column('detached_building_age', Text, nullable=True)
    detachedEquity = Column('detached_equity', Text, nullable=True)
    # マンション
    mansionBuildingNo = Column('mansion_building_no', Text, nullable=True)
    mansionCls = Column('mansion_cls', Text, nullable=True)
    mansionClsStatus = Column('mansion_cls_status', Text, nullable=True)
    mansionStructure = Column('mansion_structure', Text, nullable=True)
    mansionStructureStatus = Column('mansion_structure_status', Text, nullable=True)
    mansionFloorArea = Column('mansion_floor_area', Text, nullable=True)
    mansionFloorAreaStatus = Column('mansion_floor_area_status', Text, nullable=True)
    mansionRoomArrangement = Column('mansion_room_arrangement', Text, nullable=True)
    mansionPossessor = Column('mansion_possessor', Text, nullable=True)   
    mansionControlCost = Column('mansion_control_cost', Text, nullable=True)
    mansionBalconyArea = Column('mansion_balcony_area', Text, nullable=True)
    mansionOthersSiteUse = Column('mansion_others_siteuse', Text, nullable=True)
    mansionBuildingAge = Column('mansion_building_age', Text, nullable=True)
    mansionFloor = Column('mansion_floor', Text, nullable=True)
    mansionTotalUnits = Column('mansion_total_units', Text, nullable=True)
    mansionEquity = Column('mansion_equity', Text, nullable=True)
    # その他
    otherLandCls = Column('other_land_cls', Text, nullable=True)
    otherLandConditionClsList = Column('other_land_condition_cls_list', Text, nullable=True)
    otherLandArea = Column('other_land_area', Text, nullable=True)
    # 更新情報
    document = Column('document', Text, nullable=True)
    created = Column('created_at', DateTime, default=datetime.now(), nullable=False)
    updated = Column('updated_at', DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

# 3点セット（物件明細書，現況調査報告書及び評価書等）PDFファイル
class BitPropertyPDFs(Base):
    # テーブル名定義
    __tablename__ = 'bit_property_pdfs'
    # インデックス定義
    # __table_args__ = (
    #     UniqueConstraint(
    #         'court_id', 'sale_unit_id', name='unique_court_id_sale_unit_id'
    #     ),
    # )
    # カラム定義
    id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    prefecturesId = Column('prefectures_id', String(3), nullable=False)
    courtId = Column('court_id', String(6), nullable=False)
    saleUnitId = Column('sale_unit_id', String(12), nullable=False)
    savedRoot = Column('saved_root', Text, nullable=True)
    savedPath = Column('saved_path', Text, nullable=True)
    savedFile = Column('saved_file', Text, nullable=True)
    savedSize = Column('saved_size', Numeric(12,0), nullable=True)    
    created = Column('created_at', DateTime, default=datetime.now(), nullable=False)
    updated = Column('updated_at', DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

# 売却結果
class BitResults(Base):
    # テーブル名定義
    __tablename__ = 'bit_results'
    # インデックス定義
    __table_args__ = (
        Index(
            'index1',
            'court_id', 'case_no_text', 'thing_nos',
        ),
    )
    # カラム定義
    id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    prefecturesId = Column('prefectures_id', String(3), nullable=False)
    courtId = Column('court_id', String(6), nullable=False)
    saleType = Column('sale_type', Text, nullable=True)
    saleClsDisp = Column('sale_cls_disp', Text, nullable=True)
    caseNoText = Column('case_no_text', String(64), nullable=False)       
    saleStandardAmountDisp = Column('sale_standard_amount_disp', Text, nullable=True)     
    saleStandardAmount = Column('sale_standard_amount', Numeric(24,0), nullable=True)     
    saleAmountDisp = Column('sale_amount_disp', Text, nullable=True)     
    saleAmount = Column('sale_amount', Numeric(24,0), nullable=True)     
    thingNoList = Column('thing_no_list', Text, nullable=False)
    thingNos = Column('thing_nos', String(512), nullable=False)
    address = Column('address', Text, nullable=True)
    saleStatusDisp = Column('sale_status_disp', Text, nullable=True)
    saleStatus = Column('sale_status', Text, nullable=True)
    bitUsers = Column('bit_users', Text, nullable=True)
    bitUserClsDisp = Column('bit_user_cls_disp', Text, nullable=True)
    document = Column('document', Text, nullable=True)
    created = Column('created_at', DateTime, default=datetime.now(), nullable=False)
    updated = Column('updated_at', DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

import datetime

def main():
    conn   = 'mysql://root:password@mysql/mydb?charset=utf8'
    engine = create_engine(conn, echo=True)
    # テーブル作成
    Base.metadata.create_all(engine)
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # pdf = session.query(BitPropertyPDFs).filter(BitPropertyPDFs.id==2).one_or_none()
    # if pdf is not None:
    #     pdf.savedRoot = '/download'  
    # session.commit()

    # pdf = session.query(BitPropertyPDFs.id).filter(
    #     and_(
    #         BitPropertyPDFs.courtId    == '31234', 
    #         BitPropertyPDFs.saleUnitId == '00000045892',
    #     )
    # ).one_or_none()
    # if pdf is not None:
    #     print(pdf.id)
    # レコード追加
    # pdf = BitPropertyPDFs()
    # pdf.prefecturesId = '01'
    # pdf.courtId = '31234'
    # pdf.saleUnitId = '00000045892'
    # pdf.savedRoot = '/ext01/dat'
    # pdf.savedPath = '/01/31234/01_31234_00000045891'
    # pdf.savedFile = 'SAP_31234.pdf'
    # pdf.savedSize = 24000000

    # session.add(pdf)
    # session.commit()



if __name__ == '__main__':
    main()