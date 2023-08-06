import codecs
import collections
import configparser
import csv
import datetime
import json
import os
import urllib.parse
from pickle import UnpicklingError

import pandas as pd
import yaml
from pandas.errors import (
    ParserError,
    EmptyDataError
)

from IQCommon.exception import get_traceback_message
from IQCommon.logger import system_log
from IQCommon.i18n import get_local_text as _

DEFAULT = object


INI_FORMAT = ['.ini', '.conf']
YML_FORMAT = ['.yml', '.yaml']
JSON_FORMAT = ['.json']


def full_update(src_dict, drt_dict):
    """
    完全字典更新，支持所有类字典类型
    :param src_dict: collections.Mapping 源字典
    :param drt_dict: collections.Mapping 目标字典
    :return: None
    """
    for key, value in src_dict.items():
        if (key in drt_dict and
                isinstance(drt_dict[key], collections.Mapping) and
                isinstance(value, collections.Mapping)):
            full_update(value, drt_dict[key])
        else:
            drt_dict[key] = value


def load_ini(path):
    config = configparser.ConfigParser()
    config.read(path)
    return {
        section.name: {
            option: value
            for option, value in section.items()
        }
        for section in config.values()
    }


def load_yaml(path):
    with codecs.open(path, encoding='utf-8') as f:
        loader = yaml.Loader(f)
        loader.anchors = collections.OrderedDict()
        try:
            return loader.get_single_data()
        finally:
            loader.dispose()


def load_json(path):
    with codecs.open(path, encoding='utf-8') as f:
        return json.loads(f.read())


PARSE_CONFIG_LIST = (
    (YML_FORMAT, load_yaml),
    (JSON_FORMAT, load_json),
    (INI_FORMAT, load_ini)
)


class ObjectDict(object):
    _base = None

    def __init__(self, base_dict=None):
        if base_dict is None:
            base_dict = {}
        super(ObjectDict, self).__setattr__('_base', base_dict)

    def __getattr__(self, item):
        try:
            value = self._base[item]
        except (TypeError, KeyError):
            raise AttributeError(item)
        if isinstance(value, dict):
            value = self._base[item] = self.__class__(value)
        return value

    def update(self, other_one):
        # noinspection PyProtectedMember
        full_update(other_one._base, self._base)

    def __setattr__(self, key, value):
        self._base[key] = value

    def __repr__(self):
        return self._base.__repr__()

    def to_dict(self):
        return {
            k: v.to_dict() if isinstance(v, ObjectDict) else v
            for k, v in self._base.items()
        }


def read_config(config_path):
    if not os.path.exists(config_path):
        raise FileExistsError(config_path)

    for format_list, parse_config_func in PARSE_CONFIG_LIST:
        for format_type in format_list:
            if config_path.endswith(format_type):
                return parse_config_func(config_path)

    for format_list, parse_config_func in PARSE_CONFIG_LIST:
        try:
            return parse_config_func(config_path)
        except (yaml.YAMLError, json.JSONDecodeError, configparser.ParsingError):
            pass

    raise TypeError('Unsupport File Type: {}'.format(config_path))


# 默认数据库驱动
DB_DEFAULT_DRIVER = {
    "mysql": 'pymysql'
}


def parse_db_url(config):
    """
    将连接信息转化为 name_or_url参数
    :param config: dict
    :return: str
    """
    dialect = config.pop('dialect', 'mysql')
    driver = config.pop('driver', None) or DB_DEFAULT_DRIVER.get(dialect)
    if driver is None:
        agreement = dialect
    else:
        agreement = '{}+{}'.format(dialect, driver)
    user_name = config.pop('user', None)
    if user_name is not None:
        user_name = urllib.parse.quote_plus(user_name)
        passwd = config.pop('passwd', None)
        if passwd is None:
            user_name_password = user_name
        else:
            passwd = urllib.parse.quote_plus(passwd)
            user_name_password = '{}:{}'.format(user_name, passwd)
        user_name_password += '@'
    else:
        user_name_password = ''
    host = config.pop('host', '127.0.0.1')
    port = config.pop('port', 3306)
    db = config.pop('db', 'iqe_data')
    db = urllib.parse.quote_plus(db)
    charset = config.pop('charset', None)
    if charset is None:
        charset = ''
    else:
        charset = '?charset={}'.format(charset)
    return '{}://{}{}:{}/{}{}'.format(
        agreement, user_name_password, host, port, db, charset
    )


def get_original_function(func):
    """
    获取装饰器所装饰函数的原函数
    :param func: function 装饰器所装饰函数
    :return: function 原函数
    """
    func_wrapped = getattr(func, "__wrapped__", None)
    while func_wrapped:
        func = func_wrapped
        func_wrapped = getattr(func, "__wrapped__", None)
    return func


READ_ERROR_MESSAGE_TEMPLATE = '获取数据异常: {traceback_message}'


class FileReader(object):

    _base_method = None
    _exceptions = ()

    def __init__(
            self,
            default=DEFAULT,
            error_message_template=READ_ERROR_MESSAGE_TEMPLATE,
            error_message_dict=None,
            logger=system_log,
            level='error'
    ):
        if error_message_dict is None:
            self.error_message_dict = {}
        else:
            self.error_message_dict = error_message_dict
        self.logger_method = getattr(logger, level, system_log.error)
        self.default = default
        self.error_message_template = error_message_template
        self.logger = logger
        self.level = level

    def __call__(self, file_path, *args, **kwargs):
        try:
            return self._base_method(file_path, *args, **kwargs)
        except self._exceptions:
            self.logger_method(
                _(
                    self.error_message_template.format(
                        **dict(
                            self.error_message_dict,
                            datetime=datetime.datetime.now(),
                            traceback_message=get_traceback_message()
                        )
                    )
                )
            )
            return self.default

    def get_default(self):
        if hasattr(self.default, 'copy'):
            try:
                # noinspection PyUnresolvedReferences
                return self.default.copy()
            except (AttributeError, TypeError):
                pass
        return self.default

    def __repr__(self):
        return (
            '<{method_name}: '
            'default: {default}, '
            'error_message_template:{error_message_template}, '
            'error_message_dict:{error_message_dict}, '
            'logger: {logger}, '
            'level: {level}'
            '>'.format(
                method_name=self._base_method.__name__,
                default=self.default,
                error_message_template=self.error_message_template,
                error_message_dict=self.error_message_dict,
                logger=self.logger,
                level=self.level
            )
        )


class PickleReader(FileReader):
    _base_method = staticmethod(pd.read_pickle)

    _exceptions = (
        FileNotFoundError,
        UnpicklingError,
        ImportError,
        AttributeError
    )


class CsvReader(FileReader):
    _base_method = pd.read_csv
    _exceptions = (
        FileNotFoundError,
        ParserError,
        EmptyDataError,
        csv.Error
    )


def import_plugin(plugin_name):
    """
    封装导入函数
    :param plugin_name: str
    :return: model 导入的对象
    """
    from importlib import import_module
    try:
        return import_module(plugin_name)
    except Exception as e:
        system_log.error("*" * 30)
        system_log.error("Mod Import Error: {}, error: {}", plugin_name, e)
        system_log.error("*" * 30)
        raise e
