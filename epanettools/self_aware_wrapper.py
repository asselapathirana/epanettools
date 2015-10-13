# -*- coding: utf-8 -*-
# String for doctests and  example:
"""
from: http://stackoverflow.com/a/9874974
            >>> a = NotifierList()
            >>> flag.has_changed
            False
            >>> a.append(NotifierDict())
            >>> flag.has_changed
            True
            >>> flag.clear()
            >>> flag.has_changed
            False
            >>> a[0]["status"]="new"
            >>> flag.has_changed
            True
            >>> 

"""


changer_methods = set("__setitem__ __setslice__ __delitem__ update append extend add insert pop popitem remove setdefault __iadd__".split())


def callback_getter(obj):
    def callback(name):
        obj.has_changed = True
    return callback

def proxy_decorator(func, callback):
    def wrapper(*args, **kw):
        callback(func.__name__)
        return func(*args, **kw)
    wrapper.__name__ = func.__name__
    return wrapper

def proxy_class_factory(cls, obj):
    new_dct = cls.__dict__.copy()
    for key, value in new_dct.items():
        if key in changer_methods:
            new_dct[key] = proxy_decorator(value, callback_getter(obj))
    return type("proxy_"+ cls.__name__, (cls,), new_dct)


class Flag(object):
    def __init__(self):
        self.clear()
    def clear(self):
        self.has_changed = False

if __name__ == "__main__":

    flag = Flag()
    
    NotifierList = proxy_class_factory(list, flag)
    NotifierDict = proxy_class_factory(dict, flag)