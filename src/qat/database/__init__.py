# -*- coding: utf-8 -*-

"""
Database interface module.
"""

from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .. import config

ModelBase = declarative_base()

db_engine = create_engine(config.database_url, echo=False)
db_inspect = inspect(db_engine)
db_session = sessionmaker(bind=db_engine)()
db_metadata = MetaData(bind=db_engine)
db_metadata.reflect(db_engine)


from .table import (
    quote_table_minutely_base,
    quote_table_daily_base,
    quote_table_weekly_base,
    quote_table_monthly_base
)

from .model import (
    Currency,
    Location,
    Exchange,
    Board,
    SecurityStatus,
    Security,
    Stock
)

from .utility import (
    is_database_empty,
    is_table_empty,
    is_table_exist,
    create_all_tables,
    create_table,
    drop_all_tables,
    drop_table
)


# 证券行情表的命名规则
# quote_<exchange>_<product>_<code>_<frequency>_<>
#   exchange:   交易所简称
#   product:    证券品种
#   code:       证券代码
#   frequency:  行情频次
#
security_quote_table_name_template = 'quote_{exchange}_{product}_{code}_{frequency}'
