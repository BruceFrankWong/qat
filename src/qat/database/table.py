# -*- coding: utf-8 -*-

"""
Database model orm module.
"""

from sqlalchemy import Table, Column
from sqlalchemy import (Integer,
                        Float,
                        Date,
                        Time)

from . import db_metadata

# Quote for minute.
quote_table_minutely_base = Table('quote_minutely_base', db_metadata,
                                  Column('id', Integer, primary_key=True, comment='主键'),
                                  Column('date', Date, nullable=False, unique=True, comment='行情日期'),
                                  Column('time', Time, nullable=False, comment='行情时间'),
                                  Column('open', Float, nullable=False, comment='开盘价'),
                                  Column('high', Float, nullable=False, comment='最高价'),
                                  Column('low', Float, nullable=False, comment='最低价'),
                                  Column('close', Float, nullable=False, comment='收盘价'),
                                  Column('volume', Float, nullable=False, comment='成交量'),
                                  Column('amount', Float, nullable=False, comment='成交额')
                                  )

# Quote for daily.
quote_table_daily_base = Table('quote_daily_base', db_metadata,
                               Column('id', Integer, primary_key=True, comment='主键'),
                               Column('date', Date, nullable=False, unique=True, comment='行情日期'),
                               Column('open', Float, nullable=False, comment='开盘价'),
                               Column('high', Float, nullable=False, comment='最高价'),
                               Column('low', Float, nullable=False, comment='最低价'),
                               Column('close', Float, nullable=False, comment='收盘价'),
                               Column('volume', Float, nullable=False, comment='成交量'),
                               Column('amount', Float, nullable=False, comment='成交额')
                               )

# Quote for weekly.
quote_table_weekly_base = Table('quote_weekly_base', db_metadata,
                                Column('id', Integer, primary_key=True, comment='主键'),
                                Column('begin', Date, nullable=False, unique=True, comment='行情日期（周一）'),
                                Column('end', Date, nullable=False, unique=True, comment='行情日期（周五）'),
                                Column('open', Float, nullable=False, comment='开盘价'),
                                Column('high', Float, nullable=False, comment='最高价'),
                                Column('low', Float, nullable=False, comment='最低价'),
                                Column('close', Float, nullable=False, comment='收盘价'),
                                Column('volume', Float, nullable=False, comment='成交量'),
                                Column('amount', Float, nullable=False, comment='成交额')
                                )

# Quote for monthly.
quote_table_monthly_base = Table('quote_monthly_base', db_metadata,
                                 Column('id', Integer, primary_key=True, comment='主键'),
                                 Column('begin', Date, nullable=False, unique=True, comment='行情日期（周一）'),
                                 Column('end', Date, nullable=False, unique=True, comment='行情日期（周五）'),
                                 Column('open', Float, nullable=False, comment='开盘价'),
                                 Column('high', Float, nullable=False, comment='最高价'),
                                 Column('low', Float, nullable=False, comment='最低价'),
                                 Column('close', Float, nullable=False, comment='收盘价'),
                                 Column('volume', Float, nullable=False, comment='成交量'),
                                 Column('amount', Float, nullable=False, comment='成交额')
                                 )
