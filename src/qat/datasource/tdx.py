# -*- coding: utf-8 -*-

"""
TDX (通达信) data reader module.
"""

import typing
import struct
import datetime
import os.path

import pandas as pd

from qat.config import logger


class QuoteReaderBase:
    """
    通达信行情数据文件读取器的基类。
    """

    def __init__(self, filename: str, pattern: str):
        self.filename = filename
        self.struct = struct.Struct(pattern)

    def raw(self) -> bytes:
        with open(self.filename, 'rb') as f:
            return f.read()

    def unpack(self) -> typing.Generator:
        raw = self.raw()
        return (self.struct.unpack_from(raw, offset)
                for offset in range(0, len(raw), self.struct.size)
                )

    def to_python(self) -> typing.Generator:
        raise NotImplementedError('This class is a abstract base class.')

    def to_pandas(self) -> pd.DataFrame:
        raise NotImplementedError('This class is a abstract base class.')


class DailyQuoteReader(QuoteReaderBase):
    """
    通达信行情日线数据文件读取器。

    通达信日线数据文件保存在 <通达信安装目录>/vipdoc/<交易所代码>/lday/<交易所代码><证券代码>.day
    其中：
        <交易所代码>：   上交所 <sh>，深交所 <sz>。
        <证券代码>：     一般 6 位数字。

    每 32 个字节为一天数据。
    每 4 个字节为一个字段，每个字段内低字节在前
    00 ~ 03 字节：int，年月日，
    04 ~ 07 字节：int，开盘价, 单位（分）。
    08 ~ 11 字节：int, 最高价, 单位（分）。
    12 ~ 15 字节：int, 最低价, 单位（分）。
    16 ~ 19 字节：int, 收盘价, 单位（分）。
    20 ~ 23 字节：float, 成交额, 单位（元）。
    24 ~ 27 字节：int, 成交量, 单位（股）。
    28 ~ 31 字节：int, 上日收盘，单位（分）。
    """

    def __init__(self, filename: str):
        super().__init__(filename, '<IIIIIfII')

    def to_python(self) -> typing.Generator:
        unpack = self.unpack()
        for item in unpack:
            yield (datetime.datetime.strptime(str(item[0]), "%Y%m%d").date(),
                   item[1] * 0.01,
                   item[2] * 0.01,
                   item[3] * 0.01,
                   item[4] * 0.01,
                   item[5],
                   item[6])

    def to_pandas(self) -> pd.DataFrame:
        return pd.DataFrame(
            self.to_python(),
            columns=['date', 'open', 'high', 'low', 'close', 'amount', 'volume']
        )


class MinuteQuoteReader(QuoteReaderBase):
    """
    网传秘籍...
    ...
    二、通达信5分钟线*.lc5文件和*.lc1文件
        文件名即股票代码
        每32个字节为一个5分钟数据，每字段内低字节在前
        00 ~ 01 字节：日期，整型，
            设其值为num，则日期计算方法为：
            year=floor(num/2048)+2004; month=floor(mod(num,2048)/100); day=mod(mod(num,2048),100);
        02 ~ 03 字节： 从0点开始至目前的分钟数，整型
        04 ~ 07 字节：开盘价，float型
        08 ~ 11 字节：最高价，float型
        12 ~ 15 字节：最低价，float型
        16 ~ 19 字节：收盘价，float型
        20 ~ 23 字节：成交额，float型
        24 ~ 27 字节：成交量（股），整型
        28 ~ 31 字节：（保留）
    """

    def __init__(self, filename: str):
        super().__init__(filename, '<HHfffffII')

    def to_python(self) -> typing.Generator:
        unpack = self.unpack()
        for item in unpack:
            # TODO: 有没有必要用 Decimal 类型？
            yield (datetime.date(year=(item[0] // 2048) + 2004,
                                 month=(item[0] % 2048) // 100,
                                 day=(item[0] % 2048) % 100),
                   datetime.time(hour=(item[1] // 60), minute=(item[1] % 60)),
                   # Decimal(item[3]).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
                   float(item[2]),
                   float(item[3]),
                   float(item[4]),
                   float(item[5]),
                   float(item[6]),
                   int(item[7]))

    def to_pandas(self,
                  date_as_object: bool = False,
                  time_as_object: bool = False
                  ) -> pd.DataFrame:
        return pd.DataFrame(
            self.to_python(),
            columns=['date', 'time', 'open', 'high', 'low', 'close', 'amount', 'volume']
        )
