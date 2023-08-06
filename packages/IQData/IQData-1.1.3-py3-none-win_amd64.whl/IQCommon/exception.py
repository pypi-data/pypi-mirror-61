# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c)2018, 恒生电子股份有限公司
# All rights reserved.
#
# 文件名称：exception.py
# 摘    要：exception模块
#
# 当前版本：V1.0.0
# 作    者：qianmx21829
# 完成日期：2018-10-08
# 备    注：IQEngine的异常类型定义和异常处理
###############################################################################
import traceback

import six
import sys

from IQCommon import const
from IQCommon.logger import (
    system_log,
    strategy_log
    )
from IQCommon.i18n import get_local_text as _


class ContextError(object):
    # 上下文错误
    def __init__(self):
        self.stacks = []
        self.msg = None
        self.exc_type = None
        self.exc_val = None
        self.exc_tb = None
        self.error_type = const.ExcType.NOTSET
        self.max_exc_var_len = 160

    def set_exc(self, exc_type, exc_val, exc_tb):
        """
        设置 exc_type, exc_val, exc_tb 对应sys.exc_info()的返回值
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return: None
        """
        self.exc_type = exc_type
        self.exc_val = exc_val
        self.exc_tb = exc_tb

    def set_msg(self, msg):
        """
        设置 msg属性信息
        :param msg: str
        :return: None
        """
        self.msg = msg

    def add_stack_info(self, filename, lineno, func_name, code, local_variables=None):
        if local_variables is None:
            local_variables = {}
        self.stacks.append((filename, lineno, func_name, code, local_variables))

    @property
    def stacks_length(self):
        return len(self.stacks)

    def _repr(self, value):
        # noinspection PyBroadException
        try:
            var_str = repr(value)
            if len(var_str) > self.max_exc_var_len:
                var_str = var_str[:self.max_exc_var_len] + " ..."
            return var_str
        except Exception:
            return 'UNREPRESENTABLE VALUE'

    def __repr__(self):
        if len(self.stacks) == 0:
            return self.msg

        content = ["Exception: Traceback (most recent call last):"]
        for filename, line_no, func_name, code, local_variables in self.stacks:
            content.append('  File %s, line %s in %s' % (filename, line_no, func_name))
            content.append('    %s' % (code, ))
            for k, v in six.iteritems(local_variables):
                content.append('    --> %s = %s' % (k, self._repr(v)))
            content.append('')
        content.append("%s: %s" % (self.exc_type.__name__, self.msg))

        return "\n".join(content)


class IQUserError(Exception):
    iq_exec = const.ExcType.USER_EXC
    pass


class IQInvalidArgument(IQUserError):
    pass


class IQTypeError(TypeError):
    pass

class ParamsError(Exception):
    pass
    

class RequestException(Exception):
    pass

class CustomException(Exception):
    def __init__(self, error):
        self.error = error


class ModifyExceptionFromType(object):
    def __init__(self, exc_from_type, force=False):
        self.exc_from_type = exc_from_type
        self.force = force

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            exc_from_type = getattr(exc_val, const.EXC_EXT_NAME, const.ExcType.NOTSET)
            if self.force or exc_from_type == const.ExcType.NOTSET:
                setattr(exc_val, const.EXC_EXT_NAME, self.exc_from_type)


class IQETimeoutError(Exception):
    pass


class ThreadInterrupt(Exception, KeyboardInterrupt):
    pass


def get_func_exc_ext_name_value(exc_val):
    return getattr(exc_val, const.NEED_EXCEPTION_HANDLE, const.DEFAULT_EXC_TYPE)


def set_func_exc_ext_name_value(exc_val, value):
    setattr(exc_val, const.NEED_EXCEPTION_HANDLE, value)


def user_exc(exc_val, force=False):
    """
    向异常对象中添加属性const.EXC_EXT_NAME，并设置值为NOTSET
    :param exc_val: 异常对象
    :param force: 是否强制性
    :return: 异常对象
    """
    exc_from_type = get_func_exc_ext_name_value(exc_val)
    if exc_from_type == const.ExcType.NOTSET or force:
        set_func_exc_ext_name_value(exc_val, const.EXC_EXT_NAME)
    return exc_val


def system_exc(exc_val, force=False):
    """
    向异常对象中添加属性const.EXC_EXT_NAME，并设置值为NOTSET
    :param exc_val: 异常对象
    :param force: 是否强制性
    :return: 异常对象
    """
    exc_from_type = get_func_exc_ext_name_value(exc_val)
    if exc_from_type == const.ExcType.NOTSET or force:
        set_func_exc_ext_name_value(exc_val, const.ExcType.SYSTEM_EXC)
    return exc_val


def get_exc_from_type(exc_val):
    exc_from_type = getattr(exc_val, const.EXC_EXT_NAME, const.ExcType.NOTSET)
    return exc_from_type


def is_system_exc(exc_val):
    """
    是否系统执行报错
    """
    return get_exc_from_type(exc_val) == const.ExcType.SYSTEM_EXC


def is_user_exc(exc_val):
    """
    是否用户执行报错
    """
    return get_exc_from_type(exc_val) == const.ExcType.USER_EXC


def create_custom_exception(exc_type, exc_val, exc_tb, strategy_filename):
    # noinspection PyBroadException
    try:
        msg = str(exc_val)
    except Exception:
        msg = ""

    error = ContextError()
    error.set_msg(msg)
    error.set_exc(exc_type, exc_val, exc_tb)

    import linecache

    filename = ''
    tb = exc_tb
    while tb:
        co = tb.tb_frame.f_code
        filename = co.co_filename
        if filename != strategy_filename:
            tb = tb.tb_next
            continue
        lineno = tb.tb_lineno
        func_name = co.co_name
        code = linecache.getline(filename, lineno).strip()
        error.add_stack_info(filename, lineno, func_name, code, tb.tb_frame.f_locals)
        tb = tb.tb_next

    if filename == strategy_filename:
        error.error_type = const.ExcType.USER_EXC

    user_exc_error = CustomException(error)
    return user_exc_error


def parse_exception(exception_info):
    """
    解析内部抛出的异常信息
    """
    try:
        sys.excepthook(
            exception_info.error.exc_type,
            exception_info.error.exc_val,
            exception_info.error.exc_tb
        )
    except Exception as ex:
        system_log.exception("解析异常信息错误，异常信息:%s" % ex)

    if not is_user_exc(exception_info.error.exc_val):
        code = const.ExitCode.EXIT_INTERNAL_ERROR
        system_log.error(_(u"IQEngine 内部执行异常"))
        system_log.error(exception_info)
    else:
        code = const.ExitCode.EXIT_USER_ERROR
        strategy_log.error(_(u"用户策略执行异常"))
        strategy_log.error(exception_info)

    return code


def parse_system_exception(file_name):
    """
    解析外部抛出的异常信息
    """
    exc_type, exc_val, exc_tb = sys.exc_info()
    user_exc_error = create_custom_exception(exc_type, exc_val, exc_tb, file_name)

    return parse_exception(user_exc_error)


# noinspection PyPep8Naming
def IQE_assert(condition, e=None):
    """
    IQEngine定制化assert
    :param condition: 触发assert的条件
    :param e: 报错信息或错误类型
    :return: 无
    """
    if not condition:
        if not e:
            e = AssertionError()
        elif isinstance(e, six.string_types):
            e = AssertionError(e)
        elif not isinstance(e, Exception):
            e = AssertionError(str(e))
        raise e


def get_traceback_message():
    """
    用于获取异常信息字符串
    :return:str
    """
    return traceback.format_exc()
