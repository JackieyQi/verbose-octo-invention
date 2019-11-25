#! /usr/bin/python
# coding:utf8
"""
doc:
    http://www.geonames.org/countries/

requirement:
    geoip2==2.9.0

"""

from geoip2 import database as geoip_db
from geoip2.errors import AddressNotFoundError


class GeoIP(object):
    reader = None
    lang2locale = {
        "en_US": "en",
        "zh_Hans_CN": "zh-CN",
        "zh_Hant_HK": "zh-CN",
        "ja_JP": "ja",
    }

    def __init__(self, ip, lang=None):
        self.locales = GeoIP.decide_locales(lang or "en_US")
        self.reader = GeoIP.init_reader()
        self.ip = ip

    @staticmethod
    def decide_locales(lang):
        if not lang:
            return ["en"]

        locale = GeoIP.lang2locale.get(lang, "en")
        if locale == "en":
            return ["en"]
        return [locale, "en"]

    @staticmethod
    def init_reader():
        if GeoIP.reader is None:
            # GeoIP.reader = geoip2.database.Reader('/root/GeoLite2-City.mmdb')
            GeoIP.reader = geoip_db.Reader('/root/GeoLite2-City.mmdb')
        return GeoIP.reader

    @cached_property
    def response(self):
        try:
            return self.reader.city(self.ip)
        except AddressNotFoundError:
            return None
        except ValueError:
            return None

    @property
    @pick_name
    def country(self):
        return self.response.country if self.response else None

    @property
    @pick_name
    def region(self):
        return self.response.subdivisions.most_specific if self.response else None

    @property
    @pick_name
    def city(self):
        return self.response.city if self.response else None

    @property
    def location(self):
        entities = [entity for entity in [self.country, self.region, self.city] if entity]
        if not entities:
            return None
        return " ".join(entities)


def get_iso_code_by_ip(register_ip):
    try:
        iso_code = GeoIP(register_ip).response.country.iso_code
    except BaseException as e:
        return None
    return iso_code


COUNTRY_ISO_CODE = {'BD': 'BGD', 'BE': 'BEL', 'BF': 'BFA', 'BG': 'BGR', 'BA': 'BIH', 'BB': 'BRB', 'WF': 'WLF',
                    'BL': 'BLM', 'BM': 'BMU', 'BN': 'BRN', 'BO': 'BOL', 'BH': 'BHR', 'BI': 'BDI', 'BJ': 'BEN',
                    'BT': 'BTN', 'JM': 'JAM', 'BV': 'BVT', 'BW': 'BWA', 'WS': 'WSM', 'BQ': 'BES', 'BR': 'BRA',
                    'BS': 'BHS', 'JE': 'JEY', 'BY': 'BLR', 'BZ': 'BLZ', 'RU': 'RUS', 'RW': 'RWA', 'RS': 'SRB',
                    'TL': 'TLS', 'RE': 'REU', 'TM': 'TKM', 'TJ': 'TJK', 'RO': 'ROU', 'TK': 'TKL', 'GW': 'GNB',
                    'GU': 'GUM', 'GT': 'GTM', 'GS': 'SGS', 'GR': 'GRC', 'GQ': 'GNQ', 'GP': 'GLP', 'JP': 'JPN',
                    'GY': 'GUY', 'GG': 'GGY', 'GF': 'GUF', 'GE': 'GEO', 'GD': 'GRD', 'GB': 'GBR', 'GA': 'GAB',
                    'SV': 'SLV', 'GN': 'GIN', 'GM': 'GMB', 'GL': 'GRL', 'GI': 'GIB', 'GH': 'GHA', 'OM': 'OMN',
                    'TN': 'TUN', 'JO': 'JOR', 'HR': 'HRV', 'HT': 'HTI', 'HU': 'HUN', 'HK': 'HKG', 'HN': 'HND',
                    'HM': 'HMD', 'VE': 'VEN', 'PR': 'PRI', 'PS': 'PSE', 'PW': 'PLW', 'PT': 'PRT', 'SJ': 'SJM',
                    'PY': 'PRY', 'IQ': 'IRQ', 'PA': 'PAN', 'PF': 'PYF', 'PG': 'PNG', 'PE': 'PER', 'PK': 'PAK',
                    'PH': 'PHL', 'PN': 'PCN', 'PL': 'POL', 'PM': 'SPM', 'ZM': 'ZMB', 'EH': 'ESH', 'EE': 'EST',
                    'EG': 'EGY', 'ZA': 'ZAF', 'EC': 'ECU', 'IT': 'ITA', 'VN': 'VNM', 'SB': 'SLB', 'ET': 'ETH',
                    'SO': 'SOM', 'ZW': 'ZWE', 'SA': 'SAU', 'ES': 'ESP', 'ER': 'ERI', 'ME': 'MNE', 'MD': 'MDA',
                    'MG': 'MDG', 'MF': 'MAF', 'MA': 'MAR', 'MC': 'MCO', 'UZ': 'UZB', 'MM': 'MMR', 'ML': 'MLI',
                    'MO': 'MAC', 'MN': 'MNG', 'MH': 'MHL', 'MK': 'MKD', 'MU': 'MUS', 'MT': 'MLT', 'MW': 'MWI',
                    'MV': 'MDV', 'MQ': 'MTQ', 'MP': 'MNP', 'MS': 'MSR', 'MR': 'MRT', 'IM': 'IMN', 'UG': 'UGA',
                    'TZ': 'TZA', 'MY': 'MYS', 'MX': 'MEX', 'IL': 'ISR', 'FR': 'FRA', 'IO': 'IOT', 'SH': 'SHN',
                    'FI': 'FIN', 'FJ': 'FJI', 'FK': 'FLK', 'FM': 'FSM', 'FO': 'FRO', 'NI': 'NIC', 'NL': 'NLD',
                    'NO': 'NOR', 'NA': 'NAM', 'VU': 'VUT', 'NC': 'NCL', 'NE': 'NER', 'NF': 'NFK', 'NG': 'NGA',
                    'NZ': 'NZL', 'NP': 'NPL', 'NR': 'NRU', 'NU': 'NIU', 'CK': 'COK', 'XK': 'XKX', 'CI': 'CIV',
                    'CH': 'CHE', 'CO': 'COL', 'CN': 'CHN', 'CM': 'CMR', 'CL': 'CHL', 'CC': 'CCK', 'CA': 'CAN',
                    'CG': 'COG', 'CF': 'CAF', 'CD': 'COD', 'CZ': 'CZE', 'CY': 'CYP', 'CX': 'CXR', 'CS': 'SCG',
                    'CR': 'CRI', 'CW': 'CUW', 'CV': 'CPV', 'CU': 'CUB', 'SZ': 'SWZ', 'SY': 'SYR', 'SX': 'SXM',
                    'KG': 'KGZ', 'KE': 'KEN', 'SS': 'SSD', 'SR': 'SUR', 'KI': 'KIR', 'KH': 'KHM', 'KN': 'KNA',
                    'KM': 'COM', 'ST': 'STP', 'SK': 'SVK', 'KR': 'KOR', 'SI': 'SVN', 'KP': 'PRK', 'KW': 'KWT',
                    'SN': 'SEN', 'SM': 'SMR', 'SL': 'SLE', 'SC': 'SYC', 'KZ': 'KAZ', 'KY': 'CYM', 'SG': 'SGP',
                    'SE': 'SWE', 'SD': 'SDN', 'DO': 'DOM', 'DM': 'DMA', 'DJ': 'DJI', 'DK': 'DNK', 'VG': 'VGB',
                    'DE': 'DEU', 'YE': 'YEM', 'DZ': 'DZA', 'US': 'USA', 'UY': 'URY', 'YT': 'MYT', 'UM': 'UMI',
                    'LB': 'LBN', 'LC': 'LCA', 'LA': 'LAO', 'TV': 'TUV', 'TW': 'TWN', 'TT': 'TTO', 'TR': 'TUR',
                    'LK': 'LKA', 'LI': 'LIE', 'LV': 'LVA', 'TO': 'TON', 'LT': 'LTU', 'LU': 'LUX', 'LR': 'LBR',
                    'LS': 'LSO', 'TH': 'THA', 'TF': 'ATF', 'TG': 'TGO', 'TD': 'TCD', 'TC': 'TCA', 'LY': 'LBY',
                    'VA': 'VAT', 'VC': 'VCT', 'AE': 'ARE', 'AD': 'AND', 'AG': 'ATG', 'AF': 'AFG', 'AI': 'AIA',
                    'VI': 'VIR', 'IS': 'ISL', 'IR': 'IRN', 'AM': 'ARM', 'AL': 'ALB', 'AO': 'AGO', 'AN': 'ANT',
                    'AQ': 'ATA', 'AS': 'ASM', 'AR': 'ARG', 'AU': 'AUS', 'AT': 'AUT', 'AW': 'ABW', 'IN': 'IND',
                    'AX': 'ALA', 'AZ': 'AZE', 'IE': 'IRL', 'ID': 'IDN', 'UA': 'UKR', 'QA': 'QAT', 'MZ': 'MOZ'}

COUNTRY_CN_NAME = {
    "AND": u"安道尔共和国",
    "ARE": u"阿联酋",
    "AFG": u"阿富汗",
    "ATG": u"安提瓜和巴布达",
    "AIA": u"安圭拉岛",
    "ALB": u"阿尔巴尼亚",
    "ARM": u"亚美尼亚",
    "AGO": u"安哥拉",
    "ATA": u"南极洲",
    "ARG": u"阿根廷",
    "ASM": u"美属萨摩亚",
    "AUT": u"奥地利",
    "AUS": u"澳大利亚",
    "ABW": u"阿鲁巴",
    "ALA": u"奥兰",
    "AZE": u"阿塞拜疆",
    "BIH": u"波斯尼亚和黑塞哥维那",
    "BRB": u"巴巴多斯",
    "BGD": u"孟加拉国",
    "BEL": u"比利时",
    "BFA": u"布基纳法索",
    "BGR": u"保加利亚",
    "BHR": u"巴林",
    "BDI": u"布隆迪",
    "BEN": u"贝宁",
    "BLM": u"圣巴泰勒米",
    "BMU": u"百慕大群岛",
    "BRN": u"文莱",
    "BOL": u"玻利维亚",
    "BES": u"加勒比荷兰",
    "BRA": u"巴西",
    "BHS": u"巴哈马",
    "BTN": u"不丹",
    "BVT": u"布韦岛",
    "BWA": u"博茨瓦纳",
    "BLR": u"白俄罗斯",
    "BLZ": u"伯利兹",
    "CAN": u"加拿大",
    "CCK": u"科科斯（基林）群岛",
    "COD": u"刚果（金）",
    "CAF": u"中非共和国",
    "COG": u"刚果（布）",
    "CHE": u"瑞士",
    "CIV": u"科特迪瓦",
    "COK": u"库克群岛",
    "CHL": u"智利",
    "CMR": u"喀麦隆",
    "CHN": u"中国",
    "COL": u"哥伦比亚",
    "CRI": u"哥斯达黎加",
    "CUB": u"古巴",
    "CPV": u"佛得角",
    "CUW": u"库拉索",
    "CXR": u"圣诞岛",
    "CYP": u"塞浦路斯",
    "CZE": u"捷克",
    "DEU": u"德国",
    "DJI": u"吉布提",
    "DNK": u"丹麦",
    "DMA": u"多米尼克",
    "DOM": u"多米尼加共和国",
    "DZA": u"阿尔及利亚",
    "ECU": u"厄瓜多尔",
    "EST": u"爱沙尼亚",
    "EGY": u"埃及",
    "ESH": u"阿拉伯撒哈拉民主共和国",
    "ERI": u"厄立特里亚",
    "ESP": u"西班牙",
    "ETH": u"埃塞俄比亚",
    "FIN": u"芬兰",
    "FJI": u"斐济",
    "FLK": u"福克兰群岛",
    "FSM": u"密克罗尼西亚联邦",
    "FRO": u"法罗群岛",
    "FRA": u"法国",
    "GAB": u"加蓬",
    "GBR": u"英国",
    "GRD": u"格林纳达",
    "GEO": u"格鲁吉亚",
    "GUF": u"法属圭亚那",
    "GGY": u"根西",
    "GHA": u"加纳",
    "GIB": u"直布罗陀",
    "GRL": u"格陵兰",
    "GMB": u"冈比亚",
    "GIN": u"几内亚",
    "GLP": u"瓜德罗普",
    "GNQ": u"赤道几内亚",
    "GRC": u"希腊",
    "SGS": u"南乔治亚和南桑威奇群岛",
    "GTM": u"危地马拉",
    "GUM": u"关岛",
    "GNB": u"几内亚比绍",
    "GUY": u"圭亚那",
    "HKG": u"香港",
    "HMD": u"赫德岛和麦克唐纳群岛",
    "HND": u"洪都拉斯",
    "HRV": u"克罗地亚",
    "HTI": u"海地",
    "HUN": u"匈牙利",
    "IDN": u"印尼",
    "IRL": u"爱尔兰",
    "ISR": u"以色列",
    "IMN": u"曼岛",
    "IND": u"印度",
    "IOT": u"英属印度洋领地",
    "IRQ": u"伊拉克",
    "IRN": u"伊朗",
    "ISL": u"冰岛",
    "ITA": u"意大利",
    "JEY": u"泽西",
    "JAM": u"牙买加",
    "JOR": u"约旦",
    "JPN": u"日本",
    "KEN": u"肯尼亚",
    "KGZ": u"吉尔吉斯坦",
    "KHM": u"柬埔寨",
    "KIR": u"基里巴斯",
    "COM": u"科摩罗",
    "KNA": u"圣基茨和尼维斯",
    "PRK": u"朝鲜",
    "KOR": u"韩国",
    "KWT": u"科威特",
    "CYM": u"开曼群岛",
    "KAZ": u"哈萨克斯坦",
    "LAO": u"老挝",
    "LBN": u"黎巴嫩",
    "LCA": u"圣卢西亚",
    "LIE": u"列支敦士登",
    "LKA": u"斯里兰卡",
    "LBR": u"利比里亚",
    "LSO": u"莱索托",
    "LTU": u"立陶宛",
    "LUX": u"卢森堡",
    "LVA": u"拉脱维亚",
    "LBY": u"利比亚",
    "MAR": u"摩洛哥",
    "MCO": u"摩纳哥",
    "MDA": u"摩尔多瓦",
    "MNE": u"黑山共和国",
    "MAF": u"法属圣马丁",
    "MDG": u"马达加斯加",
    "MHL": u"马绍尔群岛",
    "MKD": u"马其顿",
    "MLI": u"马里",
    "MMR": u"缅甸",
    "MNG": u"蒙古",
    "MAC": u"澳门",
    "MNP": u"马里亚纳群岛",
    "MTQ": u"马提尼克",
    "MRT": u"毛里塔尼亚",
    "MSR": u"蒙特塞拉特岛",
    "MLT": u"马耳他",
    "MUS": u"毛里求斯",
    "MDV": u"马尔代夫",
    "MWI": u"马拉维",
    "MEX": u"墨西哥",
    "MYS": u"马来西亚",
    "MOZ": u"莫桑比克",
    "NAM": u"纳米比亚",
    "NCL": u"新喀里多尼亚",
    "NER": u"尼日尔",
    "NFK": u"诺福克岛",
    "NGA": u"尼日利亚",
    "NIC": u"尼加拉瓜",
    "NLD": u"荷兰",
    "NOR": u"挪威",
    "NPL": u"尼泊尔",
    "NRU": u"瑙鲁",
    "NIU": u"纽埃",
    "NZL": u"新西兰",
    "OMN": u"阿曼",
    "PAN": u"巴拿马",
    "PER": u"秘鲁",
    "PYF": u"法属玻利尼西亚",
    "PNG": u"巴布亚新几内亚",
    "PHL": u"菲律宾",
    "PAK": u"巴基斯坦",
    "POL": u"波兰",
    "SPM": u"圣皮埃尔和密克隆",
    "PCN": u"皮特凯恩群岛",
    "PRI": u"波多黎各",
    "PSE": u"巴勒斯坦",
    "PRT": u"葡萄牙",
    "PLW": u"帕劳",
    "PRY": u"巴拉圭",
    "QAT": u"卡塔尔",
    "REU": u"留尼旺",
    "ROU": u"罗马尼亚",
    "SRB": u"塞尔维亚",
    "RUS": u"俄罗斯",
    "RWA": u"卢旺达",
    "SAU": u"沙特阿拉伯",
    "SLB": u"所罗门群岛",
    "SYC": u"塞舌尔",
    "SDN": u"苏丹",
    "SWE": u"瑞典",
    "SGP": u"新加坡",
    "SHN": u"圣赫勒拿",
    "SVN": u"斯洛文尼亚",
    "SJM": u"挪威 斯瓦尔巴群岛和扬马延岛",
    "SVK": u"斯洛伐克",
    "SLE": u"塞拉利昂",
    "SMR": u"圣马力诺",
    "SEN": u"塞内加尔",
    "SOM": u"索马里",
    "SUR": u"苏里南",
    "SSD": u"南苏丹",
    "STP": u"圣多美和普林西比",
    "SLV": u"萨尔瓦多",
    "SXM": u"荷属圣马丁",
    "SYR": u"叙利亚",
    "SWZ": u"斯威士兰",
    "TCA": u"特克斯和凯科斯群岛",
    "TCD": u"乍得",
    "ATF": u"法属南部领地",
    "TGO": u"多哥",
    "THA": u"泰国",
    "TJK": u"塔吉克斯坦",
    "TKL": u"托克劳",
    "TLS": u"东帝汶",
    "TKM": u"土库曼斯坦",
    "TUN": u"突尼斯",
    "TON": u"汤加",
    "TUR": u"土耳其",
    "TTO": u"特立尼达和多巴哥",
    "TUV": u"图瓦卢",
    "TWN": u"台湾省",
    "TZA": u"坦桑尼亚",
    "UKR": u"乌克兰",
    "UGA": u"乌干达",
    "UMI": u"美国本土外小岛屿",
    "USA": u"美国",
    "URY": u"乌拉圭",
    "UZB": u"乌兹别克斯坦",
    "VAT": u"梵蒂冈",
    "VCT": u"圣文森特和格林纳丁斯",
    "VEN": u"委内瑞拉",
    "VGB": u"英属维尔京群岛",
    "VIR": u"美属维尔京群岛",
    "VNM": u"越南",
    "VUT": u"瓦努阿图",
    "WLF": u"瓦利斯和富图纳",
    "WSM": u"萨摩亚",
    "YEM": u"也门",
    "MYT": u"马约特",
    "ZAF": u"南非",
    "ZMB": u"赞比亚",
    "ZWE": u"津巴布韦",
}
