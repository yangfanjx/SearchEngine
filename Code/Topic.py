#!/usr/bin/python
# -*- coding: utf-8 -*-

'''主题词提取'''

import jieba.analyse
import csv
import os
import re
from textrank4zh import TextRank4Sentence
from SearchEngine.Code.Wapper import wapper
from SearchEngine.Code.Base_Function import get_del_filter

@wapper
class Get_Topic(object):
    def __init__(self, _debug=False):
        self.df = get_del_filter()
        self.re_set = zip(self.df['content'], self.df['name'])

        if not _debug:
            from django.conf import settings
            self._folder = settings.SAVE_FILE
        else:
            self._folder = "./Files/"


    # 主题词
    def topic_words(self, _file_path):
        data_handle = ""
        with open(_file_path,encoding="utf-8") as f1:
            for text in f1.readlines():
                if text.split():
                    data_handle += text

        # data_handle = data
        for _re, _name in self.re_set:
            data_handle = re.sub(_re, _name, data_handle)

        data_handle = re.sub(r"数字", "", data_handle)
        # data = re.sub(r"[^\u4e00-\u9fa5]", " ", data)
        # data = re.sub(r"\s+", " ", data)

        # 使用TF-idf方式提取关键词和权重，并且依次显示出来。如果你不做特殊指定的话，默认显示数量为20个关键词。
        # for keyword, weight in extract_tags(data, withWeight=True):
        #     print('%s %s' % (keyword, weight))
        # print('\t')
        #
        # for keyword, weight in extract_tags(data, topK=10, withWeight=True):
        #     print('%s %s' % (keyword, weight))
        # print('\t')
        #
        get_topic = jieba.analyse.textrank(data_handle, topK=5, withWeight=True)
        return_msg = [{keyword: weight} for keyword, weight in get_topic]
        return return_msg
        # for keyword, weight in self_jieba.analyse.textrank(data, topK=5, withWeight=True):
        #     print('%s %s' % (keyword, weight))


    # 主题段落
    def topic_paragraph(self):
        with open('./1.txt') as f:
            data = f.read()

        # print(data)
        tr4s = TextRank4Sentence()
        tr4s.analyze(text=data, lower=True, source="all_filters")
        abstract = []
        for item in tr4s.get_key_sentences(num=100):
            if len(item.sentence) < 300:
                abstract.append([item.index, item.sentence])

        abstract = sorted(abstract[:1], key=lambda x: x[0])
        abstract = ["(%i) %s \n" % (i, x[i]) for i, x in enumerate(abstract, 1)]

        # print("".join(abstract))


    # 遍历文件夹——写入文件
    def file_write(self):
        with open('./topic_run.csv', 'w')as f:
            f_csv = csv.writer(f)
            f_csv.writerow(["标题", "主题", "内容"])

            # 文件夹位置
            for root, dirs, files in os.walk(self._folder):
                # print(root) #当前目录路径
                # print(dirs) #当前路径下所有子目录
                # print(files) #当前路径下所有非目录子文件
                for _file in files:
                    if _file.endswith(".txt"):
                        print("File: " + root + "/" + _file)
                        get_topic, data = self.topic_words(root + "/" + _file)
                        f_csv.writerow([_file, str(get_topic), data])


    # 遍历文件夹——返回信息
    def file_return(self):
        return_list = []
        # 文件夹位置
        for root, dirs, files in os.walk(self._folder):
            # print(root) #当前目录路径
            # print(dirs) #当前路径下所有子目录
            # print(files) #当前路径下所有非目录子文件
            for _file in files:
                if _file.endswith(".txt"):
                    # print("File: " + root + "/" + _file)
                    get_topic, data = self.topic_words(root + "/" + _file)
                    return_list.append([str(get_topic), root + "/" + _file])

        return return_list


if __name__ == "__main__":
    a = Get_Topic(True)
    print(a.topic_words('/Users/yf/PycharmProjects/Search/Search/Files/HeiLongJiang/关于推迟我省上半年高等教育自学考试新生注册报名工作的公告.txt'))
    # b = Get_Topic(True)
    #
    # print(a is b)
    # print(a.file_return())
