# -*- coding: utf-8 -*-

"""
Database module - utility.
"""


from . import (db_engine,
               db_session,
               db_inspect,
               db_metadata,
               ModelBase)
from ..config import logger


def is_database_empty() -> bool:
    """
    Is the database empty?
    :return: True if the database has no tables, otherwise False.
    """
    table_names = db_inspect.get_table_names()
    return table_names == []


def is_table_exist(table_name: str) -> bool:
    """
    Is a table exist?
    :param table_name: Name of a table.
    :return: True if the table existed, otherwise False.
    """
    return table_name in db_metadata.tables.keys()


def is_table_empty(table_name: str) -> bool:
    """
    Is a table empty?
    :param table_name: Name of a table.
    :return: True if the table has no record, otherwise False.
    """
    return db_session.query(table_name).first()


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
    db_metadata.reflect(db_engine)


def drop_all_tables() -> None:
    """
    Drop all tables.
    :return:
    """
    logger.debug('Drop all tables.')
    ModelBase.metadata.drop_all(db_engine)
    db_metadata.reflect(db_engine)


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
    db_metadata.reflect(db_engine)
    return True


def create_all_tables() -> None:
    """
    Create all tables.
    :return:
    """
    logger.debug('Create all tables.')
    ModelBase.metadata.create_all(db_engine)
    db_metadata.reflect(db_engine)
