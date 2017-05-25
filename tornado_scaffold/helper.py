# encoding: utf-8

import ConfigParser
import os.path
import hashlib
import time
import datetime
from os import urandom
from tornado_json.routes import get_routes


# 根目录路径
__DIR__ = os.path.abspath(os.path.dirname(__file__))


# 获取绝对路径
def base_path(*p):
    return os.path.join(__DIR__, *p)


# 读取.env配置文件
def read_env():
    env_file = base_path(".env")
    env = ConfigParser.ConfigParser()
    env.read(env_file)
    return env


# 返回模块API路由
def get_module_api_routes(module):
    module_path = base_path("modules", module)
    if os.path.isdir(module_path):
        api_module = __import__(name=module, fromlist=["api"])
        routes = get_routes(api_module)
        return routes
    else:
        return []


def str_random(n):
    return (''.join(map(lambda xx:(hex(ord(xx))[2:]), urandom(n))))[0:n]


def time_fmt(t=time.localtime()):
    if isinstance(t,datetime.datetime):
        return t.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return time.strftime("%Y-%m-%d %H:%M:%S", t)
