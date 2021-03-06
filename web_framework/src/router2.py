# -*- coding: UTF-8 -*-
# @author youerning
# @email 673125641@qq.com
# 主要参考于: https://github.com/sirMackk/diy_framework/blob/master/diy_framework/application.py

import re
from collections import namedtuple
from functools import partial


Route = namedtuple("Route", ["methods", "pattern", "handler"])


def home():
    return "home"

def item(name):
    return name

def not_found():
    return "not found"


class Router(object):
    def __init__(self):
        self._routes = []

    @classmethod
    def build_route_regex(self, regexp_str):
        # 路由的路径有两种格式
        # 1. /home 这种格式没有动态变量, 返回^/home$这样的正则表达式
        # 2. /item/{name} 这种格式用动态变量,  将其处理成^/item/(?P<name>[a-zA-Z0-9_-]+)$这种格式
        def named_groups(matchobj):
            return '(?P<{0}>[a-zA-Z0-9_-]+)'.format(matchobj.group(1))

        re_str = re.sub(r'{([a-zA-Z0-9_-]+)}', named_groups, regexp_str)
        re_str = ''.join(('^', re_str, '$',))
        return re.compile(re_str)


    @classmethod
    def match_path(self, pattern, path):
        match = pattern.match(path)
        try:
            return match.groupdict()
        except AttributeError:
            return None

    def add(self, path, handler, methods=None):
        if methods is None:
            methods = {"GET"}
        else:
            methods = set(methods)
        pattern = self.__class__.build_route_regex(path)
        route = Route(methods, pattern, handler)
        
        if route in self._routes:
            raise Exception("路由重复了: {}".format(path))
        self._routes.append(route)

    def get_handler(self, method, path):
        for route in self._routes:
            if method in route.methods:
                params = self.match_path(route.pattern, path)

                if params is not None:
                    return partial(route.handler, **params)

        return not_found


route = Router()
route.add("/home", home)
route.add("/item/{name}", item, methods=["GET", "POST"])
print(route.get_handler("GET", "/home")())
print(route.get_handler("POST", "/home")())
print(route.get_handler("GET", "/item/item1")())
print(route.get_handler("POST", "/item/item1")())
print(route.get_handler("GET", "/xxxxxx")())