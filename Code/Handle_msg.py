#!/usr/bin/python
# -*- coding: utf-8 -*-

'''正则处理数据，停止词过滤'''

import re
from SearchEngine.Code.Wapper import wapper
from SearchEngine.Code.Base_Function import jieba_cut, get_del_filter, file_path
from django.conf import settings


# 删除信息
# 正则与停止词
@wapper
class File_Del_Class(object):
    def __init__(self):
        self.df = get_del_filter()
        with open(settings.USE_FILE+ "stop_words.txt", encoding="utf-8") as f:
            self.stop_list = [i.replace(u"\n", "") for i in f.readlines() if len(i) > 2]

            # 正则处理文本


    def filter_del(self, m_text):
        _data = m_text
        for _re, _name in zip(self.df['content'], self.df['name']):
            _data = re.sub(_re, _name, _data)

        _data = re.sub(r"数字", "", _data)
        return _data


    # 停止词过滤
    def del_stop_words(self, msgs):
        return [i for i in jieba_cut(msgs) if len(i) > 1 and i not in self.stop_list]
