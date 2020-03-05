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


from .table import (quote_table_minutely_base,
                    quote_table_daily_base,
                    quote_table_weekly_base,
                    quote_table_monthly_base
                    )
from .model import (Currency,
                    Location,
                    Exchange,
                    Board,
                    SecurityStatus,
                    )
from .initialize import (initialize_table_currency,
                         initialize_table_location,
                         initialize_table_exchange,
                         initialize_table_board,
                         initialize_table_security_status
                         )
