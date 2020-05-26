import jieba.analyse
import csv
import os
import re
from textrank4zh import TextRank4Sentence
import pandas as pd


class Get_Topic(object):
    def __init__(self):
        df = pd.read_csv("./ai_filter_rule.csv", encoding='utf-8')
        self.re_set = zip(df['content'], df['name'])


    def run1(self, _file_path):
        data = ""
        with open(_file_path) as f1:
            for text in f1.readlines():
                if text.split():
                    data += text

        # with open('./1.txt') as f:
        #     data = f.read()
        # data = data.strip()
        data_handle = data
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
        a = jieba.analyse.textrank(data_handle, topK=5, withWeight=True)

        b = [{keyword: weight} for keyword, weight in a]

        return b
        # return [{keyword: weight} for keyword, weight in
        #         self_jieba.analyse.textrank(data_handle, topK=5, withWeight=True)]
        # for keyword, weight in self_jieba.analyse.textrank(data, topK=5, withWeight=True):
        #     print('%s %s' % (keyword, weight))


    def run2(self):
        with open('./1.txt') as f:
            data = f.read()

        print(data)
        tr4s = TextRank4Sentence()
        tr4s.analyze(text=data, lower=True, source="all_filters")
        abstract = []
        for item in tr4s.get_key_sentences(num=100):
            if len(item.sentence) < 300:
                abstract.append([item.index, item.sentence])

        abstract = sorted(abstract[:1], key=lambda x: x[0])
        abstract = ["(%i) %s \n" % (i, x[i]) for i, x in enumerate(abstract, 1)]

        print("".join(abstract))


    # 遍历文件夹
    def file_name(self):
        with open('./topic_run.csv', 'w')as f:
            f_csv = csv.writer(f)
            f_csv.writerow(["标题", "主题", "内容"])

            # 文件夹位置
            _folder = settings.READ_FILE
            for root, dirs, files in os.walk(_folder):
                # print(root) #当前目录路径
                # print(dirs) #当前路径下所有子目录
                # print(files) #当前路径下所有非目录子文件
                for _file in files:
                    if _file.endswith(".txt"):
                        print(root + "/" + _file)
                        get_topic, data = self.run1(root + "/" + _file)
                        f_csv.writerow([_file, str(get_topic), data])


if __name__ == "__main__":
    a = Get_Topic()
    print(a.run1("./1.txt"))
