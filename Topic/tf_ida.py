import pandas as pd
import pandas.io.sql as sql
import jieba
import nltk
import jieba.posseg as pseg
from gensim import corpora, models, similarities
import re

if __name__ == '__main__':
    cont = ["标签：洗衣机不错操作简单全自动不错心得：洗衣机很满意！洗宝宝衣服的！小巧方便！！",
            "标签：洗衣时间短脱水声音小脱水很好噪音很小操作简单心得：比超市便宜，挺好用的，床单也可以洗。",
            "标签：脱水很好脱水声音小洗衣效果好心得：质量、设计都非常好，外观也很漂亮。很满意。要注意这款...",
            "标签：洗衣干净动力足洗衣效果好心得：比较小巧，非常不错，大品牌有保障！！！",
            "心得：很适合家庭使用小件的衣物及时就洗出来了方便",
            "标签：洗衣机不错操作简单心得：非常不错的洗衣机，价格也还不错，支持京东！",
            "标签：脱水很好操作简单心得：给儿子买的脱水用，还不错",
            "心得：很好的烘干机，已经用了",
            "标签：操作简单心得：说是防缠绕，不知道是怎么个防缠绕法，脱水声音超大，像是在撞墙一样版本：6...",
            "标签：全自动不错心得：买来送长辈的，还没用，看起来还可以版本：6.5公斤"]

    # 用户词典导入
    # jieba.load_userdict("F:\userdict.txt")

    # 1. 读取数据
    # conn = MySQLdb.connect(host='', port=3306, charset='utf8',user='', passwd='', db='')
    # df = sql.read_sql('select * from test',conn)
    # conn.close()
    # cont = df['commcont']

    pattern = r'标签：|心得：'
    regx = re.compile(pattern)
    r = lambda x: regx.sub('', x)
    filtercont = map(r, cont)
    # print([i for i in filtercont])
    # 分词+选词
    nwordall = []
    for t in filtercont:
        words = pseg.cut(t)
        nword = ['']
        for w in words:
            # if ((w.flag == 'n' or w.flag == 'v' or w.flag == 'a') and len(w.word) > 1)
            if len(w.word) > 1:
                nword.append(w.word)

    nwordall.append(nword)

    print(nwordall)
    # 3. 选择后的词生成字典
    dictionary = corpora.Dictionary(nwordall)
    print(dictionary.token2id)
    # 生成语料库
    corpus = [dictionary.doc2bow(text) for text in nwordall]
    print(corpus)
    # tfidf加权
    tfidf = models.TfidfModel(corpus)
    # print(tfidf.idfs)
    # print(tfidf.idx)
    corpus_tfidf = tfidf[corpus]
    for doc in corpus_tfidf:
        print(doc)

    # 4. 主题模型lda，可用于降维
    # lda流式数据建模计算，每块10000条记录，提取50个主题
    lda = models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=5, update_every=1,
                                   chunksize=3, passes=1)
    for i in range(0, 3):
        print(lda.print_topics(i)[0])
    # lda全部数据建模，提取100个主题
    # lda = models.ldamodel.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=100, update_every=0, passes=20)
    # 利用原模型预测新文本主题
    # doc_lda = lda[corpus_tfidf]

    # 5. word2vec 词向量化，可用于比较词相似度，寻找对应关系，词聚类
    # sentences = models.word2vec.LineSentence(nwordall)
    # size为词向量维度数,windows窗口范围,min_count频数小于5的词忽略,workers是线程数
    model = models.word2vec.Word2Vec(nwordall, size=100, window=5, min_count=5, workers=4)
    # model.save("F:\word2vecmodels") 建模速度慢，建议保存，后续直接调用
    # model = models.word2vec.Word2Vec.load("F:\word2vecmodels")
    print(model[u'洗衣'])
    # 向量表示
    sim = model.most_similar(positive=[u'洗衣', u'方便'])
    # 相近词
    for s in sim:
        print("word:%s,similar:%s " % (s[0], s[1]))
