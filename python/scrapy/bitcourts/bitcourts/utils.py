import re
from datetime import datetime
from japanera import Japanera, EraDate

# 文字列を整数にする
def to_int_def(value, default=0):
    try:
        result = int(value)
    except ValueError:
        return default
    return result

class utils:
    @classmethod
    def to_int_def(cls, value, default=0):
        try:
            result = int(value)
        except:
            return default
        return result

    @classmethod
    def to_str(cls, values, default=None, delimiter=''):
        if (values is None):
            return default
        return delimiter.join(values)

    @classmethod
    def to_datetime(cls, values, default=None):
        try:
            result = datetime.strptime(''.join(values), '%Y-%m-%d %H:%M:%S') 
        except ValueError:
            result = default
        return result

    @classmethod
    def to_amount(cls, value, default=None):
        result = re.sub(r'\D', '', cls.to_str(value))
        return cls.to_int_def(result, default)

    @classmethod
    def to_thingNos(cls, values, default=None):
        return default
    
# end of class utils

COURTS = [
    # 北海道
    { 'courtId':'38111','courtNm':'札幌地方裁判所本庁','prefecturesId':'01','prefecturesNm':'北海道','blockId':'01','blockNm':'北海道',},
    { 'courtId':'38211','courtNm':'函館地方裁判所本庁','prefecturesId':'01','prefecturesNm':'北海道','blockId':'01','blockNm':'北海道',},
    { 'courtId':'38311','courtNm':'旭川地方裁判所本庁','prefecturesId':'01','prefecturesNm':'北海道','blockId':'01','blockNm':'北海道',},
    { 'courtId':'38411','courtNm':'釧路地方裁判所本庁','prefecturesId':'01','prefecturesNm':'北海道','blockId':'01','blockNm':'北海道',},
    { 'courtId':'38431','courtNm':'釧路地方裁判所帯広支部','prefecturesId':'01','prefecturesNm':'北海道','blockId':'01','blockNm':'北海道',},
    { 'courtId':'38441','courtNm':'釧路地方裁判所北見支部','prefecturesId':'01','prefecturesNm':'北海道','blockId':'01','blockNm':'北海道',},
    # 青森県
    { 'courtId':'37611','courtNm':'青森地方裁判所本庁','prefecturesId':'02','prefecturesNm':'青森県','blockId':'02','blockNm':'東北',},
    { 'courtId':'37631','courtNm':'青森地方裁判所弘前支部','prefecturesId':'02','prefecturesNm':'青森県','blockId':'02','blockNm':'東北',},
    { 'courtId':'37632','courtNm':'青森地方裁判所八戸支部','prefecturesId':'02','prefecturesNm':'青森県','blockId':'02','blockNm':'東北',},
    # 岩手県
    { 'courtId':'37411','courtNm':'盛岡地方裁判所本庁','prefecturesId':'03','prefecturesNm':'岩手県','blockId':'02','blockNm':'東北',},
    { 'courtId':'37431','courtNm':'盛岡地方裁判所一関支部','prefecturesId':'03','prefecturesNm':'岩手県','blockId':'02','blockNm':'東北',},
    { 'courtId':'37441','courtNm':'盛岡地方裁判所花巻支部','prefecturesId':'03','prefecturesNm':'岩手県','blockId':'02','blockNm':'東北',},
    { 'courtId':'37443','courtNm':'盛岡地方裁判所遠野支部','prefecturesId':'03','prefecturesNm':'岩手県','blockId':'02','blockNm':'東北',},
    { 'courtId':'37444','courtNm':'盛岡地方裁判所宮古支部','prefecturesId':'03','prefecturesNm':'岩手県','blockId':'02','blockNm':'東北',},
    # 宮城県
    { 'courtId':'37111','courtNm':'仙台地方裁判所本庁','prefecturesId':'04','prefecturesNm':'宮城県','blockId':'02','blockNm':'東北',},
    # 秋田県
    { 'courtId':'37511','courtNm':'秋田地方裁判所本庁','prefecturesId':'05','prefecturesNm':'秋田県','blockId':'02','blockNm':'東北',},
    { 'courtId':'37531','courtNm':'秋田地方裁判所大館支部','prefecturesId':'05','prefecturesNm':'秋田県','blockId':'02','blockNm':'東北',},
    { 'courtId':'37532','courtNm':'秋田地方裁判所横手支部','prefecturesId':'05','prefecturesNm':'秋田県','blockId':'02','blockNm':'東北',},
    { 'courtId':'37533','courtNm':'秋田地方裁判所大曲支部','prefecturesId':'05','prefecturesNm':'秋田県','blockId':'02','blockNm':'東北',},
    { 'courtId':'37541','courtNm':'秋田地方裁判所能代支部','prefecturesId':'05','prefecturesNm':'秋田県','blockId':'02','blockNm':'東北',},
    # 山形県
    { 'courtId':'37311','courtNm':'山形地方裁判所本庁','prefecturesId':'06','prefecturesNm':'山形県','blockId':'02','blockNm':'東北',},
    { 'courtId':'37332','courtNm':'山形地方裁判所鶴岡支部','prefecturesId':'06','prefecturesNm':'山形県','blockId':'02','blockNm':'東北',},
    { 'courtId':'37333','courtNm':'山形地方裁判所酒田支部','prefecturesId':'06','prefecturesNm':'山形県','blockId':'02','blockNm':'東北',},
    # 福島県
    { 'courtId':'37211','courtNm':'福島地方裁判所本庁','prefecturesId':'07','prefecturesNm':'福島県','blockId':'02','blockNm':'東北',},
    { 'courtId':'37231','courtNm':'福島地方裁判所郡山支部','prefecturesId':'07','prefecturesNm':'福島県','blockId':'02','blockNm':'東北',},
    { 'courtId':'37233','courtNm':'福島地方裁判所会津若松支部','prefecturesId':'07','prefecturesNm':'福島県','blockId':'02','blockNm':'東北',},
    { 'courtId':'37234','courtNm':'福島地方裁判所いわき支部','prefecturesId':'07','prefecturesNm':'福島県','blockId':'02','blockNm':'東北',},
    { 'courtId':'37241','courtNm':'福島地方裁判所相馬支部','prefecturesId':'07','prefecturesNm':'福島県','blockId':'02','blockNm':'東北',},
    # 茨城県
    { 'courtId':'31511','courtNm':'水戸地方裁判所本庁','prefecturesId':'08','prefecturesNm':'茨城県','blockId':'03','blockNm':'関東',},
    { 'courtId':'31531','courtNm':'水戸地方裁判所土浦支部','prefecturesId':'08','prefecturesNm':'茨城県','blockId':'03','blockNm':'関東',},
    { 'courtId':'31532','courtNm':'水戸地方裁判所下妻支部','prefecturesId':'08','prefecturesNm':'茨城県','blockId':'03','blockNm':'関東',},
    { 'courtId':'31543','courtNm':'水戸地方裁判所龍ケ崎支部','prefecturesId':'08','prefecturesNm':'茨城県','blockId':'03','blockNm':'関東',},
    # 栃木県
    { 'courtId':'31611','courtNm':'宇都宮地方裁判所本庁','prefecturesId':'09','prefecturesNm':'栃木県','blockId':'03','blockNm':'関東',},
    { 'courtId':'31632','courtNm':'宇都宮地方裁判所足利支部','prefecturesId':'09','prefecturesNm':'栃木県','blockId':'03','blockNm':'関東',},
    { 'courtId':'31642','courtNm':'宇都宮地方裁判所大田原支部','prefecturesId':'09','prefecturesNm':'栃木県','blockId':'03','blockNm':'関東',},
    # 群馬県
    { 'courtId':'31711','courtNm':'前橋地方裁判所本庁','prefecturesId':'10','prefecturesNm':'群馬県','blockId':'03','blockNm':'関東',},
    { 'courtId':'31731','courtNm':'前橋地方裁判所桐生支部','prefecturesId':'10','prefecturesNm':'群馬県','blockId':'03','blockNm':'関東',},
    { 'courtId':'31732','courtNm':'前橋地方裁判所高崎支部','prefecturesId':'10','prefecturesNm':'群馬県','blockId':'03','blockNm':'関東',},
    { 'courtId':'31741','courtNm':'前橋地方裁判所沼田支部','prefecturesId':'10','prefecturesNm':'群馬県','blockId':'03','blockNm':'関東',},
    { 'courtId':'31742','courtNm':'前橋地方裁判所太田支部','prefecturesId':'10','prefecturesNm':'群馬県','blockId':'03','blockNm':'関東',},
    # 埼玉県
    { 'courtId':'31311','courtNm':'さいたま地方裁判所本庁','prefecturesId':'11','prefecturesNm':'埼玉県','blockId':'03','blockNm':'関東',},
    { 'courtId':'31331','courtNm':'さいたま地方裁判所川越支部','prefecturesId':'11','prefecturesNm':'埼玉県','blockId':'03','blockNm':'関東',},
    { 'courtId':'31332','courtNm':'さいたま地方裁判所熊谷支部','prefecturesId':'11','prefecturesNm':'埼玉県','blockId':'03','blockNm':'関東',},
    { 'courtId':'31341','courtNm':'さいたま地方裁判所越谷支部','prefecturesId':'11','prefecturesNm':'埼玉県','blockId':'03','blockNm':'関東',},
    # 千葉県
    { 'courtId':'31411','courtNm':'千葉地方裁判所本庁','prefecturesId':'12','prefecturesNm':'千葉県','blockId':'03','blockNm':'関東',},
    { 'courtId':'31431','courtNm':'千葉地方裁判所松戸支部','prefecturesId':'12','prefecturesNm':'千葉県','blockId':'03','blockNm':'関東',},
    # 東京都
    { 'courtId':'31111','courtNm':'東京地方裁判所本庁','prefecturesId':'13','prefecturesNm':'東京都','blockId':'03','blockNm':'関東',},
    { 'courtId':'31131','courtNm':'東京地方裁判所立川支部','prefecturesId':'13','prefecturesNm':'東京都','blockId':'03','blockNm':'関東',},
    # 神奈川県
    { 'courtId':'31211','courtNm':'横浜地方裁判所本庁','prefecturesId':'14','prefecturesNm':'神奈川県','blockId':'03','blockNm':'関東',},
    { 'courtId':'31231','courtNm':'横浜地方裁判所川崎支部','prefecturesId':'14','prefecturesNm':'神奈川県','blockId':'03','blockNm':'関東',},
    { 'courtId':'31232','courtNm':'横浜地方裁判所横須賀支部','prefecturesId':'14','prefecturesNm':'神奈川県','blockId':'03','blockNm':'関東',},
    { 'courtId':'31233','courtNm':'横浜地方裁判所小田原支部','prefecturesId':'14','prefecturesNm':'神奈川県','blockId':'03','blockNm':'関東',},
    { 'courtId':'31234','courtNm':'横浜地方裁判所相模原支部','prefecturesId':'14','prefecturesNm':'神奈川県','blockId':'03','blockNm':'関東',},
    # 新潟県
    { 'courtId':'32111','courtNm':'新潟地方裁判所本庁','prefecturesId':'15','prefecturesNm':'新潟県','blockId':'04','blockNm':'北陸・甲信越',},
    { 'courtId':'32132','courtNm':'新潟地方裁判所長岡支部','prefecturesId':'15','prefecturesNm':'新潟県','blockId':'04','blockNm':'北陸・甲信越',},
    { 'courtId':'32133','courtNm':'新潟地方裁判所高田支部','prefecturesId':'15','prefecturesNm':'新潟県','blockId':'04','blockNm':'北陸・甲信越',},
    { 'courtId':'32141','courtNm':'新潟地方裁判所三条支部','prefecturesId':'15','prefecturesNm':'新潟県','blockId':'04','blockNm':'北陸・甲信越',},
    { 'courtId':'32146','courtNm':'新潟地方裁判所佐渡支部','prefecturesId':'15','prefecturesNm':'新潟県','blockId':'04','blockNm':'北陸・甲信越',},
    # 富山県
    { 'courtId':'34611','courtNm':'富山地方裁判所本庁','prefecturesId':'16','prefecturesNm':'富山県','blockId':'04','blockNm':'北陸・甲信越',},
    { 'courtId':'34631','courtNm':'富山地方裁判所高岡支部','prefecturesId':'16','prefecturesNm':'富山県','blockId':'04','blockNm':'北陸・甲信越',},
    # 石川県
    { 'courtId':'34511','courtNm':'金沢地方裁判所本庁','prefecturesId':'17','prefecturesNm':'石川県','blockId':'04','blockNm':'北陸・甲信越',},
    { 'courtId':'34531','courtNm':'金沢地方裁判所七尾支部','prefecturesId':'17','prefecturesNm':'石川県','blockId':'04','blockNm':'北陸・甲信越',},
    # 福井県
    { 'courtId':'34411','courtNm':'福井地方裁判所本庁','prefecturesId':'18','prefecturesNm':'福井県','blockId':'04','blockNm':'北陸・甲信越',},
    { 'courtId':'34443','courtNm':'福井地方裁判所敦賀支部','prefecturesId':'18','prefecturesNm':'福井県','blockId':'04','blockNm':'北陸・甲信越',},
    # 山梨県
    { 'courtId':'31911','courtNm':'甲府地方裁判所本庁','prefecturesId':'19','prefecturesNm':'山梨県','blockId':'04','blockNm':'北陸・甲信越',},
    # 長野県
    { 'courtId':'32011','courtNm':'長野地方裁判所本庁','prefecturesId':'20','prefecturesNm':'長野県','blockId':'04','blockNm':'北陸・甲信越',},
    { 'courtId':'32031','courtNm':'長野地方裁判所上田支部','prefecturesId':'20','prefecturesNm':'長野県','blockId':'04','blockNm':'北陸・甲信越',},
    { 'courtId':'32032','courtNm':'長野地方裁判所松本支部','prefecturesId':'20','prefecturesNm':'長野県','blockId':'04','blockNm':'北陸・甲信越',},
    { 'courtId':'32033','courtNm':'長野地方裁判所諏訪支部','prefecturesId':'20','prefecturesNm':'長野県','blockId':'04','blockNm':'北陸・甲信越',},
    { 'courtId':'32034','courtNm':'長野地方裁判所飯田支部','prefecturesId':'20','prefecturesNm':'長野県','blockId':'04','blockNm':'北陸・甲信越',},
    { 'courtId':'32042','courtNm':'長野地方裁判所佐久支部','prefecturesId':'20','prefecturesNm':'長野県','blockId':'04','blockNm':'北陸・甲信越',},
    { 'courtId':'32045','courtNm':'長野地方裁判所伊那支部','prefecturesId':'20','prefecturesNm':'長野県','blockId':'04','blockNm':'北陸・甲信越',},
    # 岐阜県
    { 'courtId':'34311','courtNm':'岐阜地方裁判所本庁','prefecturesId':'21','prefecturesNm':'岐阜県','blockId':'05','blockNm':'東海',},
    { 'courtId':'34332','courtNm':'岐阜地方裁判所高山支部','prefecturesId':'21','prefecturesNm':'岐阜県','blockId':'05','blockNm':'東海',},
    { 'courtId':'34342','courtNm':'岐阜地方裁判所多治見支部','prefecturesId':'21','prefecturesNm':'岐阜県','blockId':'05','blockNm':'東海',},
    { 'courtId':'34343','courtNm':'岐阜地方裁判所御嵩支部','prefecturesId':'21','prefecturesNm':'岐阜県','blockId':'05','blockNm':'東海',},
    # 静岡県
    { 'courtId':'31811','courtNm':'静岡地方裁判所本庁','prefecturesId':'22','prefecturesNm':'静岡県','blockId':'05','blockNm':'東海',},
    { 'courtId':'31831','courtNm':'静岡地方裁判所沼津支部','prefecturesId':'22','prefecturesNm':'静岡県','blockId':'05','blockNm':'東海',},
    { 'courtId':'31832','courtNm':'静岡地方裁判所浜松支部','prefecturesId':'22','prefecturesNm':'静岡県','blockId':'05','blockNm':'東海',},
    { 'courtId':'31841','courtNm':'静岡地方裁判所富士支部','prefecturesId':'22','prefecturesNm':'静岡県','blockId':'05','blockNm':'東海',},
    # 愛知県
    { 'courtId':'34111','courtNm':'名古屋地方裁判所本庁','prefecturesId':'23','prefecturesNm':'愛知県','blockId':'05','blockNm':'東海',},
    { 'courtId':'34131','courtNm':'名古屋地方裁判所一宮支部','prefecturesId':'23','prefecturesNm':'愛知県','blockId':'05','blockNm':'東海',},
    { 'courtId':'34132','courtNm':'名古屋地方裁判所岡崎支部','prefecturesId':'23','prefecturesNm':'愛知県','blockId':'05','blockNm':'東海',},
    { 'courtId':'34133','courtNm':'名古屋地方裁判所豊橋支部','prefecturesId':'23','prefecturesNm':'愛知県','blockId':'05','blockNm':'東海',},
    # 三重県
    { 'courtId':'34211','courtNm':'津地方裁判所本庁','prefecturesId':'24','prefecturesNm':'三重県','blockId':'05','blockNm':'東海',},
    { 'courtId':'34231','courtNm':'津地方裁判所四日市支部','prefecturesId':'24','prefecturesNm':'三重県','blockId':'05','blockNm':'東海',},
    { 'courtId':'34242','courtNm':'津地方裁判所伊賀支部','prefecturesId':'24','prefecturesNm':'三重県','blockId':'05','blockNm':'東海',},
    { 'courtId':'34243','courtNm':'津地方裁判所伊勢支部','prefecturesId':'24','prefecturesNm':'三重県','blockId':'05','blockNm':'東海',},
    # 滋賀県
    { 'courtId':'33511','courtNm':'大津地方裁判所本庁','prefecturesId':'25','prefecturesNm':'滋賀県','blockId':'06','blockNm':'近畿',},
    { 'courtId':'33542','courtNm':'大津地方裁判所彦根支部','prefecturesId':'25','prefecturesNm':'滋賀県','blockId':'06','blockNm':'近畿',},
    { 'courtId':'33543','courtNm':'大津地方裁判所長浜支部','prefecturesId':'25','prefecturesNm':'滋賀県','blockId':'06','blockNm':'近畿',},
    # 京都府
    { 'courtId':'33211','courtNm':'京都地方裁判所本庁','prefecturesId':'26','prefecturesNm':'京都府','blockId':'06','blockNm':'近畿',},
    { 'courtId':'33231','courtNm':'京都地方裁判所舞鶴支部','prefecturesId':'26','prefecturesNm':'京都府','blockId':'06','blockNm':'近畿',},
    { 'courtId':'33242','courtNm':'京都地方裁判所宮津支部','prefecturesId':'26','prefecturesNm':'京都府','blockId':'06','blockNm':'近畿',},
    { 'courtId':'33244','courtNm':'京都地方裁判所福知山支部','prefecturesId':'26','prefecturesNm':'京都府','blockId':'06','blockNm':'近畿',},
    # 大阪府
    { 'courtId':'33111','courtNm':'大阪地方裁判所本庁','prefecturesId':'27','prefecturesNm':'大阪府','blockId':'06','blockNm':'近畿',},
    { 'courtId':'33131','courtNm':'大阪地方裁判所堺支部','prefecturesId':'27','prefecturesNm':'大阪府','blockId':'06','blockNm':'近畿',},
    { 'courtId':'33141','courtNm':'大阪地方裁判所岸和田支部','prefecturesId':'27','prefecturesNm':'大阪府','blockId':'06','blockNm':'近畿',},
    # 兵庫県
    { 'courtId':'33311','courtNm':'神戸地方裁判所本庁','prefecturesId':'28','prefecturesNm':'兵庫県','blockId':'06','blockNm':'近畿',},
    { 'courtId':'33331','courtNm':'神戸地方裁判所尼崎支部','prefecturesId':'28','prefecturesNm':'兵庫県','blockId':'06','blockNm':'近畿',},
    { 'courtId':'33332','courtNm':'神戸地方裁判所姫路支部','prefecturesId':'28','prefecturesNm':'兵庫県','blockId':'06','blockNm':'近畿',},
    { 'courtId':'33333','courtNm':'神戸地方裁判所豊岡支部','prefecturesId':'28','prefecturesNm':'兵庫県','blockId':'06','blockNm':'近畿',},
    # 奈良県
    { 'courtId':'33411','courtNm':'奈良地方裁判所本庁','prefecturesId':'29','prefecturesNm':'奈良県','blockId':'06','blockNm':'近畿',},
    { 'courtId':'33431','courtNm':'奈良地方裁判所葛城支部','prefecturesId':'29','prefecturesNm':'奈良県','blockId':'06','blockNm':'近畿',},
    # 和歌山県
    { 'courtId':'33611','courtNm':'和歌山地方裁判所本庁','prefecturesId':'30','prefecturesNm':'和歌山県','blockId':'06','blockNm':'近畿',},
    { 'courtId':'33631','courtNm':'和歌山地方裁判所田辺支部','prefecturesId':'30','prefecturesNm':'和歌山県','blockId':'06','blockNm':'近畿',},
    { 'courtId':'33642','courtNm':'和歌山地方裁判所御坊支部','prefecturesId':'30','prefecturesNm':'和歌山県','blockId':'06','blockNm':'近畿',},
    { 'courtId':'33643','courtNm':'和歌山地方裁判所新宮支部','prefecturesId':'30','prefecturesNm':'和歌山県','blockId':'06','blockNm':'近畿',},
    # 鳥取県
    { 'courtId':'35411','courtNm':'鳥取地方裁判所本庁','prefecturesId':'31','prefecturesNm':'鳥取県','blockId':'07','blockNm':'中国',},
    { 'courtId':'35431','courtNm':'鳥取地方裁判所米子支部','prefecturesId':'31','prefecturesNm':'鳥取県','blockId':'07','blockNm':'中国',},
    # 島根県
    { 'courtId':'35511','courtNm':'松江地方裁判所本庁','prefecturesId':'32','prefecturesNm':'島根県','blockId':'07','blockNm':'中国',},
    { 'courtId':'35543','courtNm':'松江地方裁判所浜田支部','prefecturesId':'32','prefecturesNm':'島根県','blockId':'07','blockNm':'中国',},
    { 'courtId':'35545','courtNm':'松江地方裁判所西郷支部','prefecturesId':'32','prefecturesNm':'島根県','blockId':'07','blockNm':'中国',},
    # 岡山県
    { 'courtId':'35311','courtNm':'岡山地方裁判所本庁','prefecturesId':'33','prefecturesNm':'岡山県','blockId':'07','blockNm':'中国',},
    { 'courtId':'35331','courtNm':'岡山地方裁判所津山支部','prefecturesId':'33','prefecturesNm':'岡山県','blockId':'07','blockNm':'中国',},
    # 広島県
    { 'courtId':'35111','courtNm':'広島地方裁判所本庁','prefecturesId':'34','prefecturesNm':'広島県','blockId':'07','blockNm':'中国',},
    { 'courtId':'35133','courtNm':'広島地方裁判所福山支部','prefecturesId':'34','prefecturesNm':'広島県','blockId':'07','blockNm':'中国',},
    # 山口県
    { 'courtId':'35211','courtNm':'山口地方裁判所本庁','prefecturesId':'35','prefecturesNm':'山口県','blockId':'07','blockNm':'中国',},
    { 'courtId':'35231','courtNm':'山口地方裁判所岩国支部','prefecturesId':'35','prefecturesNm':'山口県','blockId':'07','blockNm':'中国',},
    { 'courtId':'35232','courtNm':'山口地方裁判所下関支部','prefecturesId':'35','prefecturesNm':'山口県','blockId':'07','blockNm':'中国',},
    { 'courtId':'35241','courtNm':'山口地方裁判所周南支部','prefecturesId':'35','prefecturesNm':'山口県','blockId':'07','blockNm':'中国',},
    # 徳島県
    { 'courtId':'39211','courtNm':'徳島地方裁判所本庁','prefecturesId':'36','prefecturesNm':'徳島県','blockId':'08','blockNm':'四国',},
    # 香川県
    { 'courtId':'39111','courtNm':'高松地方裁判所本庁','prefecturesId':'37','prefecturesNm':'香川県','blockId':'08','blockNm':'四国',},
    # 愛媛県
    { 'courtId':'39411','courtNm':'松山地方裁判所本庁','prefecturesId':'38','prefecturesNm':'愛媛県','blockId':'08','blockNm':'四国',},
    # 高知県
    { 'courtId':'39311','courtNm':'高知地方裁判所本庁','prefecturesId':'39','prefecturesNm':'高知県','blockId':'08','blockNm':'四国',},
    # 福岡県
    { 'courtId':'36111','courtNm':'福岡地方裁判所本庁','prefecturesId':'40','prefecturesNm':'福岡県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36131','courtNm':'福岡地方裁判所飯塚支部','prefecturesId':'40','prefecturesNm':'福岡県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36132','courtNm':'福岡地方裁判所久留米支部','prefecturesId':'40','prefecturesNm':'福岡県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36133','courtNm':'福岡地方裁判所小倉支部','prefecturesId':'40','prefecturesNm':'福岡県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36142','courtNm':'福岡地方裁判所直方支部','prefecturesId':'40','prefecturesNm':'福岡県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36144','courtNm':'福岡地方裁判所柳川支部','prefecturesId':'40','prefecturesNm':'福岡県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36145','courtNm':'福岡地方裁判所大牟田支部','prefecturesId':'40','prefecturesNm':'福岡県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36146','courtNm':'福岡地方裁判所八女支部','prefecturesId':'40','prefecturesNm':'福岡県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36147','courtNm':'福岡地方裁判所行橋支部','prefecturesId':'40','prefecturesNm':'福岡県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36148','courtNm':'福岡地方裁判所田川支部','prefecturesId':'40','prefecturesNm':'福岡県','blockId':'09','blockNm':'九州・沖縄',},
    # 佐賀県
    { 'courtId':'36211','courtNm':'佐賀地方裁判所本庁','prefecturesId':'41','prefecturesNm':'佐賀県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36231','courtNm':'佐賀地方裁判所唐津支部','prefecturesId':'41','prefecturesNm':'佐賀県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36241','courtNm':'佐賀地方裁判所武雄支部','prefecturesId':'41','prefecturesNm':'佐賀県','blockId':'09','blockNm':'九州・沖縄',},
    # 長崎県
    { 'courtId':'36311','courtNm':'長崎地方裁判所本庁','prefecturesId':'42','prefecturesNm':'長崎県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36331','courtNm':'長崎地方裁判所佐世保支部','prefecturesId':'42','prefecturesNm':'長崎県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36341','courtNm':'長崎地方裁判所大村支部','prefecturesId':'42','prefecturesNm':'長崎県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36342','courtNm':'長崎地方裁判所島原支部','prefecturesId':'42','prefecturesNm':'長崎県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36343','courtNm':'長崎地方裁判所平戸支部','prefecturesId':'42','prefecturesNm':'長崎県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36344','courtNm':'長崎地方裁判所壱岐支部','prefecturesId':'42','prefecturesNm':'長崎県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36345','courtNm':'長崎地方裁判所五島支部','prefecturesId':'42','prefecturesNm':'長崎県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36346','courtNm':'長崎地方裁判所厳原支部','prefecturesId':'42','prefecturesNm':'長崎県','blockId':'09','blockNm':'九州・沖縄',},
    # 熊本県
    { 'courtId':'36511','courtNm':'熊本地方裁判所本庁','prefecturesId':'43','prefecturesNm':'熊本県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36531','courtNm':'熊本地方裁判所八代支部','prefecturesId':'43','prefecturesNm':'熊本県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36546','courtNm':'熊本地方裁判所人吉支部','prefecturesId':'43','prefecturesNm':'熊本県','blockId':'09','blockNm':'九州・沖縄',},
    # 大分県
    { 'courtId':'36411','courtNm':'大分地方裁判所本庁','prefecturesId':'44','prefecturesNm':'大分県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36431','courtNm':'大分地方裁判所中津支部','prefecturesId':'44','prefecturesNm':'大分県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36441','courtNm':'大分地方裁判所杵築支部','prefecturesId':'44','prefecturesNm':'大分県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36443','courtNm':'大分地方裁判所佐伯支部','prefecturesId':'44','prefecturesNm':'大分県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36444','courtNm':'大分地方裁判所竹田支部','prefecturesId':'44','prefecturesNm':'大分県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36446','courtNm':'大分地方裁判所日田支部','prefecturesId':'44','prefecturesNm':'大分県','blockId':'09','blockNm':'九州・沖縄',},
    # 宮崎県
    { 'courtId':'36711','courtNm':'宮崎地方裁判所本庁','prefecturesId':'45','prefecturesNm':'宮崎県','blockId':'09','blockNm':'九州・沖縄',},
    # 鹿児島県
    { 'courtId':'36611','courtNm':'鹿児島地方裁判所本庁','prefecturesId':'46','prefecturesNm':'鹿児島県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36631','courtNm':'鹿児島地方裁判所名瀬支部','prefecturesId':'46','prefecturesNm':'鹿児島県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36644','courtNm':'鹿児島地方裁判所鹿屋支部','prefecturesId':'46','prefecturesNm':'鹿児島県','blockId':'09','blockNm':'九州・沖縄',},
    # 沖縄県
    { 'courtId':'36811','courtNm':'那覇地方裁判所本庁','prefecturesId':'47','prefecturesNm':'沖縄県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36831','courtNm':'那覇地方裁判所沖縄支部','prefecturesId':'47','prefecturesNm':'沖縄県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36832','courtNm':'那覇地方裁判所平良支部','prefecturesId':'47','prefecturesNm':'沖縄県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36833','courtNm':'那覇地方裁判所石垣支部','prefecturesId':'47','prefecturesNm':'沖縄県','blockId':'09','blockNm':'九州・沖縄',},
    { 'courtId':'36841','courtNm':'那覇地方裁判所名護支部','prefecturesId':'47','prefecturesNm':'沖縄県','blockId':'09','blockNm':'九州・沖縄',},
]

BLOCKS= [
    { 'blockCls':'01', 'blockNm':'北海道', 'blockId':'hokkaidou', },
    { 'blockCls':'02', 'blockNm':'東北', 'blockId':'touhoku', },
    { 'blockCls':'03', 'blockNm':'関東', 'blockId':'kantou', },
    { 'blockCls':'04', 'blockNm':'北陸・甲信越', 'blockId':'hokurikukoushinetsu', },
    { 'blockCls':'05', 'blockNm':'東海', 'blockId':'toukai', },
    { 'blockCls':'06', 'blockNm':'近畿', 'blockId':'kinki', },
    { 'blockCls':'07', 'blockNm':'中国', 'blockId':'chugoku', },
    { 'blockCls':'08', 'blockNm':'四国', 'blockId':'shikoku', },
    { 'blockCls':'09', 'blockNm':'九州・沖縄', 'blockId':'kyusyuokinawa', },
]