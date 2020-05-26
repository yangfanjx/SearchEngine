
#!/usr/bin/python
# -*- coding: utf-8 -*-

# 单例装饰器
def wapper(cls):
    instances = {}


    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]


    return _singleton