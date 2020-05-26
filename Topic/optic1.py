'''
import jieba
import pandas as pd



def chinese_word_cut(mytext):
    return " ".join(jieba.cut(mytext))

if __name__ == "__main__":
    df = pd.read_csv("./datascience.csv", encoding='gb18030')
    print(df.head())
    print(df.shape)
    df["content_cutted"] = df.content.apply(chinese_word_cut)
'''


# 希拉里右键门，文档主题分类。LDA模型，数据读取还有点问题
# 数据来源:请联系公众号：湾区人工智能
import numpy as np
import re
import pandas as pd
import re
import jieba
import json


jieba.add_word("十三五")
# UnicodeEncodeError: 'mbcs' codec can't encode characters in position 0--1: invalid character
# df = pd.read_csv("./datascience.csv", encoding='gb18030')
df = pd.read_csv("./datascience.csv", encoding='utf-8')

# 原邮件数据中有很多Nan的值，直接扔了。
df = df[['content']].dropna()




def clean_email_text(_text):
    m_text = re.sub(r"[^\u4e00-\u9fa5]", "", _text)

    m_text_list = jieba.cut(m_text)

    # m_text = re.sub(r"-", " ", m_text)  # 把 "-" 的两个单词，分开。（比如：july-edu ==> july edu）
    # m_text = re.sub(r"\d+/\d+/\d+", " ", m_text)  # 日期，对主体模型没什么意义
    # m_text = re.sub(r"[0-2]?[0-9]:[0-6][0-9]", " ", m_text)  # 时间，没意义
    # m_text = re.sub(r"[\w]+@[\.\w]+", " ", m_text)  # 邮件地址，没意义
    # m_text = re.sub(r"/[a-zA-Z]*[:\//\]*[A-Za-z0-9\-_]+\.+[A-Za-z0-9\.\/%&=\?\-_]+/i", " ", m_text)  # 网址，没意义
    # pure_text = ''
    # 以防还有其他特殊字符（数字）等等，我们直接把他们loop一遍，过滤掉
    # for letter in m_text:
    #     # 只留下字母和空格
    #     if letter.isalpha() or letter == ' ':
    #         pure_text += letter
    # 再把那些去除特殊字符后落单的单词，直接排除。
    # 我们就只剩下有意义的单词了。
    use_text = ' '.join(word for word in m_text_list if len(word) > 1)
    return use_text
    # 新建一个colum


docs = df['content']
docs = docs.apply(lambda s: clean_email_text(s))
# docs.head(1).values

doclist = docs.values

from gensim import corpora, models, similarities
import gensim


with open('./stopword.txt',"r") as f:    #设置文件对象
    str = f.read()    #可以是随便对文件的操作
    stoplist = str.splitlines()



from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
cntVector = CountVectorizer(stop_words=stoplist)
cntTf = cntVector.fit_transform([doc for doc in doclist])

lda = LatentDirichletAllocation(n_topics=3,
                                learning_offset=10.,
                                random_state=0)
docres = lda.fit_transform(cntTf)
print(docres)
'''
texts = [[word for word in doc.split() if word not in stoplist] for doc in doclist]

# 用词袋的方法，把每个单词用一个数字index指代，并把我们的原文本变成一条长长的数组：
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
# 建立模型
lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=20)
# 第10号分类，其中最常出现的单词是
# lda.print_topic(10, topn=5)
# 所有的主题打印出来看看
print(lda.print_topics(num_topics=20, num_words=3))

#可以把新鲜的文本/单词，分类成20个主题中的一个。文本和单词，都必须得经过同样步骤的文本预处理+词袋化，也就是说，变成数字表示每个单词的形式。
lda.get_document_topics(bow)
'''