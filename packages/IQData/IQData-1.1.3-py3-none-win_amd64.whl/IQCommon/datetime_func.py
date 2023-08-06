# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c)2018, 恒生电子股份有限公司
# All rights reserved.
#
# 文件名称：datetime_func.py
# 摘    要：时间相关工具函数
#
# 当前版本：V1.0.0
# 作    者：qianmx21829
# 完成日期：2018-10-11
# 备    注：时间相关工具函数
###############################################################################
import time
import datetime
from collections import namedtuple
import numpy as np
import pandas as pd

from IQCommon.pycompatibility import lru_cache
from IQCommon.const import Frequency

TimeRange = namedtuple('TimeRange', ['start', 'end'])


def int_convert_date(dt):
    """
    把int类型的日期转化为datetime.date
    :param dt: 传进来的int类型的日期
    :return: datetime.date
    """
    time = pd.to_datetime(str(dt)).to_pydatetime()
    date = datetime.date(time.year, time.month, time.day)
    return date

def get_month_begin_time(time=None):
    if time is None:
        time = datetime.datetime.now()
    return time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def get_month_end_time(time=None):
    try:
        return time.replace(month=time.month + 1, day=1, hour=23, minute=59, second=59,
                            microsecond=999) - datetime.timedelta(days=1)
    except ValueError:
        return time.replace(year=time.year + 1, month=1, day=1, hour=23, minute=59, second=59,
                            microsecond=999) - datetime.timedelta(days=1)


def get_last_date(trading_calendar, dt):
    idx = trading_calendar.searchsorted(dt)
    return trading_calendar[idx - 1]


def convert_date_to_date_int(dt):
    t = dt.year
    for i in [dt.month, dt.day]:
        t *= 100
        t += i
    return t


def convert_date_to_int(dt):
    return convert_date_to_date_int(dt) * 1000000


def convert_dt_to_int(dt):
    t = convert_date_to_date_int(dt)
    for i in [dt.hour, dt.minute, dt.second]:
        t *= 100
        t += i
    return t


def convert_int_to_date(dt_int):
    dt_int = int(dt_int)
    if dt_int > 100000000:
        dt_int //= 1000000
    return _convert_int_to_date(dt_int)


@lru_cache(20480)
def _convert_int_to_date(dt_int):
    year, r = divmod(dt_int, 10000)
    month, day = divmod(r, 100)
    return datetime.datetime(year, month, day)


@lru_cache(20480)
def convert_int_to_datetime(dt_int):
    dt_int = int(dt_int)
    args = []
    while dt_int >= 10000:
        dt_int, i = divmod(dt_int, 100)
        args.append(i)
    args.append(dt_int)
    return datetime.datetime(*reversed(args))


def convert_ms_int_to_datetime(ms_dt_int):
    dt_int, ms_int = divmod(ms_dt_int, 1000)
    dt = convert_int_to_datetime(dt_int).replace(microsecond=ms_int * 1000)
    return dt


def convert_date_time_ms_int_to_datetime(date_int, time_int):
    date_int, time_int = int(date_int), int(time_int)
    dt = _convert_int_to_date(date_int)

    hours, r = divmod(time_int, 10000000)
    minutes, r = divmod(r, 100000)
    seconds, millisecond = divmod(r, 1000)

    return dt.replace(hour=hours, minute=minutes, second=seconds,
                      microsecond=millisecond * 1000)


def to_timestamp(date_time):
    if isinstance(date_time, (int, np.int64)):
        date_time = convert_int_to_datetime(date_time)
    return pd.Timestamp(date_time)


def to_timestamp_date(value):
    return to_timestamp(value).date()


def to_timestamp_dt_date(value):
    return to_timestamp(value).replace(hour=0, minute=0, second=0, microsecond=0)


# zhudf17747 2018-12-20 add
def convert_int14_to_int(dt_int, frequency):
    """
    int类型时间转string类型
    param dt_int:14位int类型数据
                 例如20180101123000 或者 20180101000000
    type dt_int: : int
    
    return value: str类型的格式时间，分为年月日和年月日时分格式
                 例如201801011230 或者 20180101
    type value: : int
    """
    # 20180101000000格式
    if frequency == Frequency.DAILY.value:
        # 去掉6个0后, 并返回
        # 返回值是年月日格式
        dt_int = dt_int // 1000000
        return dt_int
    # 20180101123000格式
    elif frequency[-1] == Frequency.MINUTE.value[-1]:
        # 去掉2个0, 并返回
        # 返回值是年月日时分格式
        dt_int = dt_int // 100
        return dt_int
    elif frequency == Frequency.TICK.value:
        return dt_int
    else:
        return dt_int // 1000000


def convert_int14_to_string(dt_int, frequency):
    """
    int类型时间转int类型
    param dt_int:14位int类型数据
                 例如20180101123000 或者 20180101000000
    type dt_int: : int

    return value: str类型的格式时间，分为年月日和年月日时分格式
                 例如201801011230 或者 20180101
    type value: : str
    """
    return str(convert_int14_to_int(dt_int, frequency))


def change_2str_of_time_2_datetime(startttime, endtime):
    """
    返回数据时间切片，需转化时间格式(fly数据切片接口专用，可重写)
    :param startttime: 开始时间(年月日)
    :type startttime: : str
    
    :param endtime: 结束时间(年月日)
    :type endtime: : str
    
    :return value: 开始时间(年月日时分)，结束时间(年月日时分)
    :type value: : datetime, datetime
    
    """
    source_start = datetime.datetime.strptime(startttime[:8] + ((len(startttime[8:]) == 4 and startttime[8:]) or '0000'), '%Y%m%d%H%M')
    source_end = datetime.datetime.strptime(endtime[:8] + ((len(endtime[8:]) == 4 and endtime[8:]) or '1530'), '%Y%m%d%H%M')
    return source_start, source_end


def change_2int_of_time_2_datetime(startttime, endtime):
    """
    返回数据时间切片，需转化时间格式
    :param startttime: 开始时间(年月日或者年月日时分秒)
    :type startttime: : int

    :param endtime: 结束时间(年月日或者年月日时分秒)
    :type endtime: : int

    :return value: 开始时间(年月日时分)，结束时间(年月日时分)
    :type value: : datetime, datetime

    """
    startttime = convert_int_to_date(startttime)
    endtime = convert_int_to_date(endtime)
    return startttime, endtime


@lru_cache(100000)
def change_dt_2_int(dt, frequency):
    """
    日期类型datetime转化为整型int
    后续需要添加其他周期频率的枚举
    :param dt: 日期时间
    :type dt: : datetime
    
    :param frequency: 周期频率，`1d` 表示日周期, `1m` 表示分钟周期
    :type frequency: : str
    
    :return value: 日期时间
    :type value: : int 
    """
    if frequency  == Frequency.DAILY.value:
        return convert_date_to_date_int(dt)
    elif frequency[-1] == Frequency.MINUTE.value[-1]:
        return convert_dt_to_int(dt) // 100
    return dt


def change_dtlist_2_intlist(dtlist, frequency):
    """
    日期类型列表datetimelist转化为整型列表intlist
    :param dtlist: 日期时间列表
    :type dtlist: : datetime of list
    
    :param frequency: 周期频率，`1d` 表示日周期, `1m` 表示分钟周期
    :type frequency: : str
    
    :return value: 日期时间列表
    :type value: : intlist 
    """
    tmp = []
    for dt in dtlist:
        tmp.append(change_dt_2_int(dt, frequency))
    return tmp


def get_range_date(pstart, pend, gstart, gend):
    """
    用于时间切片时，采用有效时间段
    :param pstart: 数据开始时间点
    :type pstart: : datetime
    
    :param pend: 数据结束时间点
    :type pend: : datetime
    
    :param gstart: 指定时间段开始时间点
    :type gstart: : datetime
    
    :param gend: 指定时间段结束时间点
    :type gend: : datetime
    
    :return value: 切片用的有效时间段(tmpstart,tmpend)
    :type value: : datetime,datetime
    """
    tmpstart = pstart
    tmpend = pend
    if pstart <= gstart:
       tmpstart = gstart

    if pend >= gend:
       tmpend = gend

    return tmpstart, tmpend

def timestamp_to_time(timestamp):
    """
    把时间戳转化成"%Y-%m-%d %H:%M:%S"格式的字符串
    :param timestamp |float: 时间戳, 格式如1547383754.514801
    :return: 时间字符串,str, 格式如"2019-01-13 20:49:14"
    """
    struct_time = time.localtime(timestamp)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)
    return dt


def change_str_list_to_int_list(str_list):
    re_data = []
    for str_value in str_list:
        dt = to_timestamp_date(str_value)
        int_value = convert_date_to_date_int(dt)
        re_data.append(int_value)
    return re_data

