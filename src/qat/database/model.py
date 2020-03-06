# -*- coding: utf-8 -*-

"""
Database model orm module.
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy import (String,
                        Unicode,
                        Boolean,
                        Integer,
                        Float,
                        Date,
                        Time)
from sqlalchemy.orm import relationship

from . import ModelBase


class QuoteDailyBase(ModelBase):
    """
    行情（日线）基类。

    到 2019 年底，沪深 A 股共计不到 4000 只股票。
    每年去除周末和节假日，A 股约250个交易日。
    全部按照 从 1992-01-01 开始，按 30 年计算：
        250 * 30 * 4000 = 3千万
    感觉要分表。
    日线数据量：
        250 * 30 = 7500 条
    1分钟（2001年起）：
        60 * 4 * 250 * 20 = 120（万）
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, comment='主键')
    date = Column(Date, nullable=False, unique=True, comment='日期')
    # time = Column(Time, nullable=True, unique=True)           # 行情的时间，分钟线才需要
    open = Column(Float, nullable=False, comment='开盘价')     # 相对于这一行情的时间段来说，可能是日线
    high = Column(Float, nullable=False, comment='最高价')
    low = Column(Float, nullable=False, comment='最低价')
    close = Column(Float, nullable=False, comment='收盘价')
    volume = Column(Float, nullable=False, comment='成交量')
    amount = Column(Float, nullable=False, comment='成交额')

    def __str__(self):
        return 'QuoteDailyBase'


class Location(ModelBase):
    """
    区位。
    """
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True, comment='主键')
    code = Column(String, nullable=True, comment='代码')
    name = Column(String, nullable=False, comment='名称')

    company_list = relationship('Company', back_populates='location')

    def __str__(self):
        return '位置(name="%s")' % self.name_zh


class Currency(ModelBase):
    """
    货币。
    """
    __tablename__ = 'currency'

    id = Column(Integer, primary_key=True, comment='主键')
    name_zh = Column(String, nullable=False, unique=True, comment='名称（中文）')
    name_en = Column(String, nullable=False, unique=True, comment='名称（英文）')
    abbr = Column(String, nullable=False, unique=True, comment='简写')

    board_list = relationship('Board', back_populates='currency')


class Exchange(ModelBase):
    """
    交易所。
    """
    __tablename__ = 'exchange'

    id = Column(Integer, primary_key=True, comment='主键')
    name_zh = Column(Unicode, unique=True, comment='中文名')
    abbr_zh = Column(String, unique=True, comment='缩写（中文）')
    name_en = Column(String, unique=True, comment='英文名')
    abbr_en = Column(String, unique=True, comment='缩写（英文）')
    url = Column(String, unique=True)
    google_prefix = Column(String, unique=True)
    location = Column(String)
    timezone = Column(Integer)

    security_list = relationship('Security', back_populates='exchange')
    stock_list = relationship('Stock', back_populates='exchange')
    board_list = relationship('Board', back_populates='exchange')

    def __str__(self):
        return 'Exchange(name_zh="%s", name_en="%s")' % (self.name_zh, self.name_en)


class Board(ModelBase):
    """
    市场板块。
    """
    __tablename__ = 'board'

    id = Column(Integer, primary_key=True, comment='主键')
    name = Column(String, nullable=False, comment='板块名称')
    opening_date = Column(Date, nullable=True, comment='开业日期')
    exchange_id = Column(Integer, ForeignKey('exchange.id'), nullable=False, comment='交易所')
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=False, comment='货币')
    # TODO: Add rules (including change limits, funding requirements nad etc.).

    currency = relationship('Currency', back_populates='board_list')
    exchange = relationship('Exchange', back_populates='board_list')
    stock_list = relationship('Stock', back_populates='board')

    def __str__(self):
        return 'Board(name="%s")' % self.name


class SecurityStatus(ModelBase):
    """
    证券状态。
    已上市，暂停上市，已退市，停牌。
    """
    __tablename__ = 'security_status'

    id = Column(Integer, primary_key=True, comment='主键')
    status = Column(String, nullable=False, unique=True, comment='状态')

    security_list = relationship('Security', back_populates='status')

    def __str__(self):
        return 'SecurityStatus(status="%s")' % self.status


class ExchangeTradingCalendar(ModelBase):
    """
    交易所交易日历。
    """
    __tablename__ = 'exchange_trading_calendar'

    id = Column(Integer, primary_key=True, comment='主键')
    exchange = Column(Unicode, unique=True, comment='休市')


class Broker(ModelBase):
    """
    券商。
    """
    __tablename__ = 'broker'

    id = Column(Integer, primary_key=True, comment='主键')
    name_zh = Column(String, nullable=False, unique=True, comment='名称（中文）')
    abbr_zh = Column(String, nullable=False, unique=True, comment='简称（中文）')
    name_en = Column(String, comment='名称（英文）')
    abbr_en = Column(String, comment='简称（英文）')
    url = Column(String, comment='网站')

    def __str__(self):
        return 'Broker(name="%s")' % self.name


class Security(ModelBase):
    """
    证券。
    """
    __tablename__ = 'security'

    id = Column(Integer, primary_key=True, comment='主键')
    type = Column(String, nullable=False, comment='类别')
    code = Column(String, nullable=False, comment='代码')
    exchange_id = Column(Integer, ForeignKey('exchange.id'), nullable=False, comment='表<exchange>的<id>字段')
    name_id = Column(Integer,
                     ForeignKey('security_used_name.id'),
                     nullable=False,
                     comment='表<security_used_name>的<id>字段')
    status_id = Column(Integer, ForeignKey('security_status.id'), nullable=False, comment='证券状态')

    exchange = relationship('Exchange', back_populates='security_list')
    status = relationship('SecurityStatus', back_populates='security_list')
    name_list = relationship('SecurityUsedName', back_populates='security')

    __mapper_args__ = {'polymorphic_on': type,
                       'polymorphic_identity': 'Security'}

    def __str__(self):
        return 'Security(code="%s")' % self.code


class Stock(Security):
    """
    股票。
    """
    __tablename__ = 'stock'

    id = Column(Integer, ForeignKey('security.id'), primary_key=True, comment='表<security>的<id>字段')
    list_date = Column(Date, nullable=False, comment='上市时间')
    delist_date = Column(Date, nullable=True, comment='退市时间')  # Null means not delist.

    board_id = Column(Integer, ForeignKey('board.id'), nullable=False, comment='表<board>的<id>字段')
    company_id = Column(Integer, ForeignKey('company.id'), nullable=False, comment='表<company>的<id>字段')

    board = relationship('Board', back_populates='stock_list')
    company = relationship('Company', back_populates='stock')

    __mapper_args__ = {'polymorphic_identity': 'Stock'}

    def __str__(self):
        return 'Stock(code="%s")' % self.code


class Fund(Security):
    """
    基金。
    """
    __tablename__ = 'Fund'

    id = Column(Integer, ForeignKey('security.id'), primary_key=True, comment='表<security>的<id>字段')

    __mapper_args__ = {'polymorphic_identity': 'Fund'}

    def __str__(self):
        return 'Fund(code="%s")' % self.code


class UsedName(ModelBase):
    """
    曾用名历史。
    """
    __tablename__ = 'used_name'

    id = Column(Integer, primary_key=True, comment='主键')
    type = Column(String, nullable=False, comment='类别')
    name = Column(String, nullable=False, comment='名称')
    begin_date = Column(Date, nullable=False, comment='开始日期')
    end_date = Column(Date, nullable=True, comment='结束日期')

    __mapper_args__ = {'polymorphic_on': type,
                       'polymorphic_identity': 'Common'}

    def __str__(self):
        return '曾用名(name="%s")' % self.name


class SecurityUsedName(UsedName):
    """
    股票曾用名。
    """
    __tablename__ = 'security_used_name'

    id = Column(Integer, ForeignKey('used_name.id'), primary_key=True, comment='表<used_name>的<id>字段')
    stock_id = Column(Integer, ForeignKey('stock.id'), nullable=False, comment='表<stock>的<id>字段')
    announcement_date = Column(Date, nullable=False, comment='公告日期')
    reason = Column(String, nullable=False, comment='更名原因')

    security = relationship('Security', back_populates='name_list')

    __mapper_args__ = {'polymorphic_identity': 'Stock'}

    def __str__(self):
        return 'StockUsedName(full_code="%s")' % self.full_code


class CompanyUsedName(UsedName):
    __tablename__ = 'company_used_name'

    id = Column(Integer, ForeignKey('used_name.id'), primary_key=True, comment='表<used_name>的<id>字段')
    stock_id = Column(Integer, ForeignKey('company.id'), nullable=False, comment='表<company>的<id>字段')

    company = relationship('Company', back_populates='name_list')

    __mapper_args__ = {'polymorphic_identity': 'Company'}

    def __str__(self):
        return 'CompanyUsedName(full_code="%s")' % self.full_code


class Company(ModelBase):
    """
    公司曾用名。
    """
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True, comment='主键')
    name = Column(String, nullable=False, comment='名称')
    abbr = Column(String, nullable=False, comment='简称')
    name_en = Column(String, nullable=True, comment='英文名称')
    url = Column(String, nullable=True, comment='网址')
    industry = Column(String, nullable=False, comment='行业')
    location_id = Column(Integer, ForeignKey('location.id'), nullable=False, comment='位置')
    registered_address = Column(String(512), nullable=False, comment='注册地址')
    main_business = Column(String(512), nullable=False, comment='主营业务')
    employee = Column(Integer, nullable=True, comment='员工人数')
    controlling_shareholders = Column(String(512), nullable=True, comment='控股股东')
    actual_controller = Column(String(512), nullable=True, comment='实际控制人')
    ultimate_controller = Column(String(512), nullable=True, comment='最终控制人')
    chairman = Column(String(64), nullable=True, comment='董事长')
    secretary = Column(String(64), nullable=True, comment='董事会秘书')
    legal_representative = Column(String(64), nullable=True, comment='法人代表')
    general_manager = Column(String(64), nullable=True, comment='总经理')
    registered_capital = Column(Integer, nullable=False, comment='注册资金')
    telephone = Column(String(32), nullable=True, comment='电话')
    fax = Column(String(32), nullable=True, comment='传真')
    postcode = Column(String(6), nullable=True, comment='邮政编码')
    address = Column(String(6), nullable=True, comment='办公地址')
    brief = Column(String(6), nullable=True, comment='公司简介')

    location = relationship('Location', back_populates='company_list')
    stock = relationship('Stock', back_populates='company')
    name_list = relationship('CompanyUsedName', back_populates='company')

    def __str__(self):
        return 'Company(name="%s")' % self.name


class StockInformation(ModelBase):
    __tablename__ = 'stock_information'

    id = Column(Integer, primary_key=True, comment='主键')


class SectorBase(ModelBase):
    """
    板块，概念
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, comment='主键')
    name = Column(String, nullable=False, comment='板块/概念/行业')  # 板块/概念/行业

    def __str__(self):
        return 'SectorBase'


class CSRCIndustry(SectorBase):
    __tablename__ = 'industry_scrc'

    id = Column(Integer, primary_key=True, comment='主键')
    name_1 = Column(String, nullable=False, comment='一级分类')
    name_2 = Column(String, nullable=False, comment='二级分类')
    name_3 = Column(String, nullable=False, comment='三级分类')

    def __str__(self):
        return '中国证监会行业分类(name="%s")' % self.name
