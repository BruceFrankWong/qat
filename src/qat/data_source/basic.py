# -*- coding: utf-8 -*-

"""
Database initialize module.
"""

import datetime
import csv
import os.path

from sqlalchemy import inspect

from qat.config import logger
from qat.database import db_engine, db_inspect, db_metadata, db_session, ModelBase
from qat.database import is_table_exist, create_table
from qat.database.model import (Currency,
                                Location,
                                Exchange,
                                Board,
                                SecurityStatus,
                                IndustryBase,
                                IndustryNBS,
                                IndustryCSRC,
                                IndustryCSIC)


def _initialize_from_value_list(instance: ModelBase,
                                value_list: list,
                                fields: list,
                                create: bool = False
                                ) -> None:
    query_fields = list([getattr(instance, x) for x in fields])
    duplicates_avoid_existed_element_list = db_session.query(*query_fields).all()

    if not is_table_exist(instance) and create:
        create_table(instance)

    item: dict
    for item in value_list:
        duplicates_avoid_new_element = (item[x] for x in fields)
        if duplicates_avoid_new_element not in duplicates_avoid_existed_element_list:
            parameter_dictionary = {x: item[x] for x in item.keys()}
            db_session.add(instance(**parameter_dictionary))
            duplicates_avoid_existed_element_list.append(list([item[x] for x in fields]))
    db_session.commit()


def initialize_table_currency() -> None:
    """
    Initialize the data table <currency>.
    :return:
    """
    instance = Currency
    duplicated_check_fields = ['name_zh', 'name_en', 'abbr', ]
    logger.debug('Initialize table <{table_name}>.'.format(table_name=Currency.__tablename__))

    item_list = [
        {'name_zh': '未知货币', 'name_en': 'Unknown Currency', 'abbr': '---'},
        {'name_zh': '人民币', 'name_en': 'Renminbi', 'abbr': 'CNY'},
        {'name_zh': '美元', 'name_en': 'U.S.Dollar', 'abbr': 'USD'},
        {'name_zh': '日圆', 'name_en': 'Japanese Yen', 'abbr': 'JPY'},
        {'name_zh': '澳大利亚元', 'name_en': 'Australian Dollar', 'abbr': 'AUD'},
        {'name_zh': '欧元', 'name_en': 'Euro', 'abbr': 'EUR'},
        {'name_zh': '英镑', 'name_en': 'Pound', 'abbr': 'GBP'},
        {'name_zh': '港币', 'name_en': 'Hong Kong Dollars', 'abbr': 'HKD'},
    ]

    _initialize_from_value_list(instance, item_list, duplicated_check_fields)


def initialize_table_location() -> None:
    """
    Initialize the data table <location>.
    :return:
    """
    instance = Location
    duplicated_check_fields = ['code', 'name', ]
    logger.debug('Initialize table <{table_name}>.'.format(table_name=instance.__tablename__))

    item_list = [
        {'code': '000000', 'name': '未知'},
        {'code': '110000', 'name': '北京'},
        {'code': '120000', 'name': '天津'},
        {'code': '130000', 'name': '河北'},
        {'code': '140000', 'name': '山西'},
        {'code': '150000', 'name': '内蒙古'},
        {'code': '210000', 'name': '辽宁'},
        {'code': '220000', 'name': '吉林'},
        {'code': '230000', 'name': '黑龙江'},
        {'code': '310000', 'name': '上海'},
        {'code': '320000', 'name': '江苏'},
        {'code': '330000', 'name': '浙江'},
        {'code': '340000', 'name': '安徽'},
        {'code': '350000', 'name': '福建'},
        {'code': '360000', 'name': '江西'},
        {'code': '370000', 'name': '山东'},
        {'code': '410000', 'name': '河南'},
        {'code': '420000', 'name': '湖北'},
        {'code': '430000', 'name': '湖南'},
        {'code': '440000', 'name': '广东'},
        {'code': '450000', 'name': '广西'},
        {'code': '460000', 'name': '海南'},
        {'code': '500000', 'name': '重庆'},
        {'code': '510000', 'name': '四川'},
        {'code': '520000', 'name': '贵州'},
        {'code': '530000', 'name': '云南'},
        {'code': '540000', 'name': '西藏'},
        {'code': '610000', 'name': '陕西'},
        {'code': '620000', 'name': '甘肃'},
        {'code': '630000', 'name': '青海'},
        {'code': '640000', 'name': '宁夏'},
        {'code': '650000', 'name': '新疆'},
        {'code': '710000', 'name': '台湾'},
        {'code': '810000', 'name': '香港'},
        {'code': '820000', 'name': '澳门'},
    ]

    _initialize_from_value_list(instance, item_list, duplicated_check_fields)


def initialize_table_exchange() -> None:
    """
    Initialize the data table  <exchange>.
    :return: None.
    """
    instance = Exchange
    duplicated_check_fields = ['name_zh', 'name_en', 'abbr_zh', 'abbr_en', 'url', 'google_prefix', ]
    logger.debug('Initialize table <{table_name}>.'.format(table_name=instance.__tablename__))

    item_list = [
        # 为 T000018.sh 专门留的。
        {'name_zh': '未知',
         'name_en': 'Unknown',
         'abbr_zh': '未知',
         'abbr_en': 'Unknown',
         'url': '',
         'google_prefix': '',
         'location': '',
         'timezone': 0,
         },
        {'name_zh': '上海证券交易所',
         'name_en': 'Shanghai Stock Exchange',
         'abbr_zh': '上交所',
         'abbr_en': 'SSE',
         'url': 'http://www.sse.com.cn/',
         'google_prefix': 'SHA',
         'location': '中国，上海',
         'timezone': 480,
         },
        {'name_zh': '深圳证券交易所',
         'name_en': 'Shenzhen Stock Exchange',
         'abbr_zh': '深交所',
         'abbr_en': 'SZSE',
         'url': 'http://www.szse.cn/',
         'google_prefix': 'SHE',
         'location': '中国，深圳',
         'timezone': 480,
         },
        {'name_zh': '香港交易及结算所有限公司',
         'name_en': 'Hong Kong Exchanges and Clearing Limited',
         'abbr_zh': '港交所',
         'abbr_en': 'HKEX',
         'url': 'https://www.hkex.com.hk/',
         'google_prefix': 'HKEX',
         'location': '中国，香港',
         'timezone': 480,
         },
        {'name_zh': '纽约证券交易所',
         'name_en': 'New York Stock Exchange',
         'abbr_zh': '纽交所',
         'abbr_en': 'NYSE',
         'url': 'https://www.nyse.com/',
         'google_prefix': 'NYSE',
         'location': '美国，纽约',
         'timezone': -300,
         # 交易时间（北京时间）：
         # 夏令时间 21:30 - （次日）03:30
         # 冬令时间 22:30 - （次日）04:30
         },
        {'name_zh': '全美证券交易商协会自动报价系统',
         'name_en': 'National Association of Securities Dealers Automated Quotations',
         'abbr_zh': '纳斯达克',
         'abbr_en': 'NASDAQ',
         'url': 'https://www.nasdaq.com/',
         'google_prefix': 'NASDAQ',
         'location': '美国，纽约',
         'timezone': -300,
         },
        {'name_zh': '伦敦证券交易所',
         'name_en': 'London Stock Exchange',
         'abbr_zh': '伦敦证交所',
         'abbr_en': 'LSE',
         'url': 'http://www.londonstockexchange.com/',
         'google_prefix': 'LON',
         'location': '英国，伦敦',
         'timezone': 0,
         },
        {'name_zh': '东京证券交易所',
         'name_en': 'Tokyo Stock Exchange',
         'abbr_zh': '东证',
         'abbr_en': 'TSE',
         'url': 'http://www.jpx.co.jp/',
         'google_prefix': 'TYO',
         'location': '日本，东京',
         'timezone': 540,
         },
        {'name_zh': '新加坡交易所',
         'name_en': 'Singapore Exchange Limited',
         'abbr_zh': '新交所',
         'abbr_en': 'SGX',
         'url': 'http://www.sgx.com/',
         'google_prefix': 'SGX',
         'location': '新加坡',
         'timezone': 480,
         },
    ]

    _initialize_from_value_list(instance, item_list, duplicated_check_fields)


def initialize_table_board() -> None:
    """
    Initialize the data table <board>.
    :return: None.
    """
    instance = Board
    duplicated_check_fields = ['name', ]
    logger.debug('Initialize table <{table_name}>.'.format(table_name=instance.__tablename__))

    item_list = [
        {'name': '未知',
         'opening_date': None,
         'exchange': 'Unknown',
         'currency': '---', },
        {'name': '主板',
         'opening_date': datetime.date(1990, 12, 19),
         'exchange': 'SSE',
         'currency': 'CNY', },
        {'name': '主板',
         'opening_date': datetime.date(1991, 7, 3),
         'exchange': 'SZSE',
         'currency': 'CNY', },
        {'name': 'B股',
         'opening_date': datetime.date(1992, 2, 21),
         'exchange': 'SSE',
         'currency': 'USD', },
        {'name': 'B股',
         'opening_date': datetime.date(1991, 10, 31),
         'exchange': 'SZSE',
         'currency': 'USD', },
        {'name': '中小板',
         'opening_date': datetime.date(2004, 6, 25),
         'exchange': 'SZSE',
         'currency': 'CNY', },
        {'name': '创业板',
         'opening_date': datetime.date(2009, 10, 23),
         'exchange': 'SZSE',
         'currency': 'CNY', },
        {'name': '科创板',
         'opening_date': datetime.date(2019, 7, 22),
         'exchange': 'SSE',
         'currency': 'CNY', },
    ]

    existed_list = db_session.query(Board.name).all()
    for item in item_list:
        if (item['name'],) not in existed_list:
            db_session.add(Board(name=item['name'],
                                 opening_date=item['opening_date'],
                                 exchange_id=db_session.query(Exchange).filter(
                                     Exchange.abbr_en == item['exchange']).first().id,
                                 currency_id=db_session.query(Currency).filter(
                                     Currency.abbr == item['currency']).first().id)
                           )
    db_session.commit()


def initialize_table_security_status() -> None:
    """
    Initialize the data table <security_status>.
    :return:
    """
    instance = SecurityStatus
    duplicated_check_fields = ['status']
    logger.debug('Initialize table <{table_name}>.'.format(table_name=instance.__tablename__))

    item_list = [{'status': '未知'},
                 {'status': '股票-上市'},
                 {'status': '股票-终止上市'},
                 {'status': '股票-暂停上市'},
                 {'status': '股票-停牌'},
                 ]

    _initialize_from_value_list(instance, item_list, duplicated_check_fields)


def initialize_table_industry_csrc() -> None:
    """
    Initialize the data table <industry_csrc> （中国证券监督管理委员会行业分类）.
    :return:
    """
    instance = IndustryCSRC
    duplicated_check_fields = ['code', 'name_zh', 'name_en']
    csv_file = 'industry_csrc.csv'
    logger.debug('Initialize table <{table_name}>.'.format(table_name=instance.__tablename__))

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), csv_file), 'r', encoding='utf-8') as data:
        item_list = csv.DictReader(data)
        _initialize_from_value_list(instance, list(item_list), duplicated_check_fields)


def initialize_table_industry_nbs() -> None:
    """
    Initialize the data table <industry_nbs> （国家统计局行业分类）.
    :return:
    """
    instance = IndustryNBS
    duplicated_check_fields = ['code', 'name_zh', 'name_en']
    csv_file = 'industry_nbs.csv'
    logger.debug('Initialize table <{table_name}>.'.format(table_name=instance.__tablename__))

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), csv_file), 'r', encoding='utf-8') as data:
        item_list = csv.DictReader(data)
        _initialize_from_value_list(instance, list(item_list), duplicated_check_fields)


def initialize_table_industry_csic() -> None:
    """
    Initialize the data table <industry_csic> （中证指数公司行业分类）.
    :return:
    """
    instance = IndustryCSIC
    duplicated_check_fields = ['code', 'name_zh', 'name_en']
    csv_file = 'industry_csic.csv'
    logger.debug('Initialize table <{table_name}>.'.format(table_name=instance.__tablename__))

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), csv_file), 'r', encoding='utf-8') as data:
        item_list = csv.DictReader(data)
        _initialize_from_value_list(instance, list(item_list), duplicated_check_fields)
