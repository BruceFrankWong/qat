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


def get_table_name(instance: ModelBase) -> str:
    """
    Return the table name of an ORM instance.
    :param instance: the ORM instance, type of <qat.database.ModelBase>.
    :return: the table name,  type of Python <str>.
    """
    return instance.__tablename__


def get_table_instance(table_name: str) -> ModelBase:
    """
    Return the ORM instance of a table name.
    :param table_name: the table name,  type of Python <str>.
    :return: the ORM instance, type of <qat.database.ModelBase>.
    """
    return db_metadata.tables.get(table_name)


def is_database_empty() -> bool:
    """
    Is the database empty?
    :return: True if the database has no tables, otherwise False.
    """
    table_names = db_inspect.get_table_names()
    return table_names == []


def is_table_exist(table: ModelBase or str) -> bool:
    """
    Is a table exist?
    :param table: An ORM instance, or the name of a table.
    :return: True if the table existed, otherwise False.
    """
    table_name: str
    if isinstance(table, ModelBase):
        table_name = get_table_name(table)
    else:
        table_name = table
    return table_name in db_metadata.tables.keys()


def is_table_empty(table: ModelBase or str) -> bool:
    """
    Is a table empty?
    :param table: An ORM instance, or the name of a table.
    :return: True if the table has no record, otherwise False.
    """
    instance: ModelBase
    if isinstance(table, ModelBase):
        instance = table
    else:
        instance = get_table_instance(table)
    return False if db_session.query(instance).first() else True


def drop_table(table: ModelBase or str) -> None:
    """
    Drop table.
    :param table: An ORM instance, or the name of a table.
    :return:
    """
    instance: ModelBase
    if isinstance(table, ModelBase):
        instance = table
    else:
        instance = get_table_instance(table)

    logger.debug('Drop table <{}>.'.format(instance.__tablename__))
    ModelBase.metadata.drop_all(db_engine, [instance], checkfirst=True)
    db_metadata.remove(instance)
    db_metadata.reflect(db_engine)


def drop_all_tables() -> None:
    """
    Drop all tables.
    :return:
    """
    logger.debug('Drop all tables.')
    ModelBase.metadata.drop_all(db_engine)
    db_metadata.reflect(db_engine)


def create_table(table: ModelBase or str, drop: bool = False) -> bool:
    """
    Create table via orm instance (object).
    :param table: An ORM instance, or the name of a table.
    :param drop: True if drop the existed table before create, otherwise False.
    :return: True if create succeed, otherwise False.
    """
    instance: ModelBase
    table_name: str
    if isinstance(table, ModelBase):
        instance = table
        table_name = get_table_name(table)
    else:
        instance = get_table_instance(table)
        table_name = table

    logger.debug('Create table <{}> for object <{}>.'.format(table_name, instance))
    if is_table_exist(instance):
        if drop:
            logger.debug('Table {} already existed, drop it...'.format(table_name))
            instance.__table__.drop()
        else:
            logger.debug('Table <{}> already existed, do nothing without <drop=True>'.format(table_name))
            return False
    logger.debug('Table <{}> created.'.format(table_name))
    instance.__table__.create(db_engine)
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
