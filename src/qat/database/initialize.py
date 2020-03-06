# -*- coding: utf-8 -*-

"""
Database initialize module.
"""

import datetime
import csv
import os.path

from ..config import logger
from . import db_engine, db_inspect, db_metadata, db_session, ModelBase
from .model import (Currency,
                    Location,
                    Exchange,
                    Board,
                    SecurityStatus,
                    IndustryNBS)


def is_database_empty() -> bool:
    table_names = db_inspect.get_table_names()
    return table_names == []


def is_table_exist(table_name: str) -> bool:
    """
    Is table exist?
    :param table_name:
    :return:
    """
    return table_name in db_metadata.tables.keys()


def drop_table(table_name: str) -> None:
    """
    Drop table.
    :param table_name:
    :return:
    """
    logger.debug('Drop table <{}>.'.format(table_name))
    table = db_metadata.tables.get(table_name)
    ModelBase.metadata.drop_all(db_engine, [table], checkfirst=True)
    db_metadata.remove(table)


def drop_all_tables() -> None:
    """
    Drop all tables.
    :return:
    """
    logger.debug('Drop all tables.')
    ModelBase.metadata.drop_all(db_engine)


def create_table(orm_instance: ModelBase, drop: bool = False) -> bool:
    """
    Create table via orm instance (object).
    :param orm_instance:
    :param drop:
    :return:
    """
    table_name = orm_instance.__tablename__
    logger.debug('Create table <{}> for object <{}>.'.format(orm_instance.__tablename__, orm_instance))
    if is_table_exist(table_name):
        if drop:
            logger.debug('Table {} already existed, drop it...'.format(table_name))
            orm_instance.__table__.drop()
        else:
            logger.debug('Table <{}> already existed, do nothing without <drop=True>'.format(table_name))
            return False
    logger.debug('Table <{}> created.'.format(table_name))
    orm_instance.__table__.create(db_engine)
    return True


def create_all_tables() -> None:
    """
    Create all tables.
    :return:
    """
    logger.debug('Create all tables.')
    ModelBase.metadata.create_all(db_engine)


def initialize_table_currency() -> None:
    """
    Initialize the data table <currency>.
    :return:
    """
    table_name = 'currency'
    logger.debug('Initialize table <{table_name}>.'.format(table_name=table_name))

    item_list = [{'name_zh': '人民币', 'name_en': 'Renminbi', 'abbr': 'CNY'},
                 {'name_zh': '美元', 'name_en': 'U.S.Dollar', 'abbr': 'USD'},
                 {'name_zh': '日圆', 'name_en': 'Japanese Yen', 'abbr': 'JPY'},
                 {'name_zh': '澳大利亚元', 'name_en': 'Australian Dollar', 'abbr': 'AUD'},
                 {'name_zh': '欧元', 'name_en': 'Euro', 'abbr': 'EUR'},
                 {'name_zh': '英镑', 'name_en': 'Pound', 'abbr': 'GBP'},
                 {'name_zh': '港币', 'name_en': 'Hong Kong Dollars', 'abbr': 'HKD'},
                 ]

    if not is_table_exist(table_name):
        Currency.__table__.create(db_engine)

    existed_list = db_session.query(Currency.name_zh, Currency.name_en, Currency.abbr).all()
    for item in item_list:
        if (item['name_zh'], item['name_en'], item['abbr']) not in existed_list:
            db_session.add(
                Currency(name_zh=item['name_zh'],
                         name_en=item['name_en'],
                         abbr=item['abbr'])
            )
    db_session.commit()


def initialize_table_location() -> None:
    """
    Initialize the data table <location>.
    :return:
    """
    table_name = 'location'
    logger.debug('Initialize table <{table_name}>.'.format(table_name=table_name))

    item_list = [
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

    if not is_table_exist(table_name):
        Location.__table__.create(db_engine)

    existed_list = db_session.query(Location.code, Location.name).all()
    for item in item_list:
        if (item['code'], item['name']) not in existed_list:
            db_session.add(
                Location(code=item['code'], name=item['name'])
            )
    db_session.commit()


def initialize_table_exchange() -> None:
    """
    Initialize the data table  <exchange>.
    :return: None.
    """
    table_name = 'exchange'
    logger.debug('Initialize table <{table_name}>.'.format(table_name=table_name))

    item_list = [
        # 为 T000018.sh 专门留的。
        {'name_zh': '无',
         'name_en': 'None',
         'abbr_zh': '无',
         'abbr_en': 'None',
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
    if not is_table_exist(table_name):
        Exchange.__table__.create(db_engine)

    existed_list = db_session.query(Exchange.name_zh,
                                    Exchange.name_en,
                                    Exchange.abbr_zh,
                                    Exchange.abbr_en,
                                    Exchange.url,
                                    Exchange.google_prefix).all()
    for item in item_list:
        if (item['name_zh'], item['name_en'], item['abbr_zh'], item['abbr_en'], item['url'], item['google_prefix']) \
                not in existed_list:
            db_session.add(Exchange(name_zh=item['name_zh'],
                                    name_en=item['name_en'],
                                    abbr_zh=item['abbr_zh'],
                                    abbr_en=item['abbr_en'],
                                    url=item['url'],
                                    google_prefix=item['google_prefix'],
                                    location=item['location'],
                                    timezone=item['timezone'])
                           )
    db_session.commit()


def initialize_table_board() -> None:
    """
    Initialize the data table <board>.
    :return: None.
    """
    table_name = 'board'
    logger.debug('Initialize table <{table_name}>.'.format(table_name=table_name))

    item_list = [
        {'name': '无',
         'opening_date': None,
         'exchange': 'None',
         'currency': 'CNY', },
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

    if not is_table_exist(table_name):
        Board.__table__.create(db_engine)

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
    table_name = 'security_status'
    logger.debug('Initialize table <{table_name}>.'.format(table_name=table_name))

    item_list = [{'status': '未知'},
                 {'status': '股票-上市'},
                 {'status': '股票-终止上市'},
                 {'status': '股票-暂停上市'},
                 {'status': '股票-停牌'},
                 ]

    if not is_table_exist(table_name):
        SecurityStatus.__table__.create(db_engine)

    existed_list = db_session.query(SecurityStatus.status).all()
    for item in item_list:
        if (item['status'],) not in existed_list:
            db_session.add(
                SecurityStatus(status=item['status'])
            )
    db_session.commit()


def initialize_table_industry_nbs() -> None:
    """
    Initialize the data table <industry_nbs> （国家统计局行业分类）.
    :return:
    """
    table_name = 'industry_nbs'
    logger.debug('Initialize table <{table_name}>.'.format(table_name=table_name))

    if not is_table_exist(table_name):
        IndustryNBS.__table__.create(db_engine)

    existed_list = db_session.query(IndustryNBS.code, IndustryNBS.name).all()

    # icfnea means 'Industrial Classification For National Economic Activities'.
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icfnea.csv'), 'r', encoding='utf-8') as icfnea:
        item_list = csv.DictReader(icfnea)
        for item in item_list:
            if (item['code'], item['name']) not in existed_list:
                code = item['code'].ljust(5, '0')
                db_session.add(IndustryNBS(code=code,
                                           name=item['name'],
                                           comment=item['comment'])
                               )
    db_session.commit()


def initialize_all_tables() -> None:
    initialize_table_currency()
    initialize_table_location()
    initialize_table_exchange()
    initialize_table_board()
    initialize_table_security_status()
    initialize_table_industry_nbs()
