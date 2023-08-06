# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c)2018, 恒生电子股份有限公司
# All rights reserved.
#
# 文件名称：logger.py
# 摘    要：日志引擎
#
# 当前版本：V1.0.0
# 作    者：lishuai14461
# 完成日期：2018-10-08
# 备    注：
###############################################################################
import datetime
import logbook
from logbook import more as logbook_more

from IQCommon.const import DATETIME_FORMAT
from IQCommon.logger.handlers import ThreadedWrapperHandler

logbook.set_datetime_format("local")


class LogEngine(object):
    """
    日志引擎
    """

    # 日志级别
    LEVEL_DEBUG = logbook.DEBUG
    LEVEL_INFO = logbook.INFO
    LEVEL_WARNING = logbook.WARNING
    LEVEL_ERROR = logbook.ERROR
    LEVEL_CRITICAL = logbook.CRITICAL

    def __init__(self, log_name='default_logger', level=None, log_book_instance=None):
        if level is None:
            level = self.LEVEL_INFO
        if (
                log_book_instance is not None and
                isinstance(log_book_instance, logbook.Logger)
        ):
            self.logger = log_book_instance
        else:
            self.logger = logbook.Logger(log_name, level)

    def set_log_level(self, level):
        """设置日志级别"""
        self.logger.level = level

    def debug(self, msg, *args, **kwargs):
        """
        调试输出
        """
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        正常输出
        """
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        警告信息
        """
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        报错输出
        """
        self.logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        """
        报错输出+记录异常信息
        """
        self.logger.exception(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        影响程序运行的严重错误
        """
        self.logger.critical(msg, *args, **kwargs)

    def disable(self):
        self.logger.disable()

    # noinspection PyUnusedLocal
    @staticmethod
    def _wrapper_handler_log_formatter(record, handler):
        """
        提供handler使用的format方法
        :param record: Record 日志记录对象
        :param handler: handler 处理函数
        :return:
        """
        # noinspection PyBroadException
        dt = record.time
        message = "{dt} {level} {msg}".format(
            dt=dt,
            level=record.level_name,
            msg=record.message,
        )
        return message

    # noinspection PyUnusedLocal
    @staticmethod
    def _std_handler_log_formatter(record, handler):
        """
        提供handler使用的format方法
        :param record: Record 日志记录对象
        :param handler: handler 处理函数
        :return:
        """
        # noinspection PyBroadException
        try:
            from IQEngine.core.engine import engine
            dt = engine.Engine.instance().trading_dt.strftime(DATETIME_FORMAT)
        except Exception:
            dt = datetime.datetime.now().strftime(DATETIME_FORMAT)

        message = "{dt} {level} {msg}".format(
            dt=dt,
            level=record.level_name,
            msg=record.message,
        )
        return message

    @property
    def handlers(self):
        return self.logger.handlers

    def add_handler(self, log_handler, with_log_formatter=False, is_async=False, maxsize=0):

        if with_log_formatter:
            if is_async:
                self.add_wrapper_handler_log_formatter(log_handler)
                log_handler = self.add_async(log_handler, maxsize)
            else:
                self.add_std_handler_log_formatter(log_handler)
        else:
            if is_async:
                log_handler = self.add_async(log_handler, maxsize)
        self.handlers.append(log_handler)
        return log_handler

    @staticmethod
    def add_async(handler, maxsize=0):
        return ThreadedWrapperHandler(handler, maxsize=maxsize)

    @classmethod
    def add_std_handler_log_formatter(cls, handler):
        """
        添加日志格式format的LogEngine._user_std_handler_log_formatter
        :return: None
        """
        handler.formatter = cls._std_handler_log_formatter

    @classmethod
    def add_wrapper_handler_log_formatter(cls, handler):
        """
        添加日志格式format的LogEngine._user_std_handler_log_formatter
        :return: None
        """
        handler.formatter = cls._wrapper_handler_log_formatter


# 用户代码logger日志
user_log = LogEngine("user_log")

# 系统日志
system_log = LogEngine("system_log", level=LogEngine.LEVEL_DEBUG)

# 策略日志
strategy_log = LogEngine("strategy_log")


# noinspection PyUnusedLocal
def user_print(*args, sep=' ', end='', file=None, flush=None):
    """
    用于覆盖用户使用的print函数，用法与buildins.print一致
    print(value, ..., sep=' ', end='\n', file=sys.stdout, flush=False)

    Prints the values to a stream, or to sys.stdout by default.
    Optional keyword arguments:
    file:  a file-like object (stream); defaults to the current sys.stdout.
    sep:   string inserted between values, default a space.
    end:   string appended after the last value, default a newline.
    flush: whether to forcibly flush the stream.
    """
    message = sep.join(map(str, args)) + end
    user_log.info(message)


DEFAULT_HANDLER = logbook_more.ColorizedStderrHandler(bubble=True)
LogEngine.add_std_handler_log_formatter(DEFAULT_HANDLER)


def log_refresh():
    for log_obj in [user_log, strategy_log, system_log]:
        for handler in log_obj.handlers:
            if isinstance(handler, ThreadedWrapperHandler):
                handler.shutdown()
        log_obj.handlers.clear()

    user_log.add_handler(
        DEFAULT_HANDLER
    )

    strategy_log.add_handler(
        DEFAULT_HANDLER
    )

    system_log.add_handler(
        DEFAULT_HANDLER
    )


LOG_LEVEL = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}


def get_logger_level(level):
    """
    获取日志等级
    :param level: str
    :return:
    """
    level = level.upper()
    if level not in  LOG_LEVEL:
        level = 'INFO'
    return getattr(logbook, level)


log_refresh()
