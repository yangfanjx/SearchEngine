#!/usr/bin/python
# -*- coding: utf-8 -*-

from SearchEngine.Code.Wapper import wapper
from pyltp import SentenceSplitter, Segmentor, Postagger, NamedEntityRecognizer, Parser, SementicRoleLabeller
import os


@wapper
class LTP_CLASS(object):
    def __init__(self):
        self.LTP_DATA_DIR = '/Users/yf/Downloads/ltp_data_v3.4.0'
        # 自定义分词表
        self.cut_file = '/Users/yf/Downloads/ltp_data_v3.4.0/cut.txt'
        # 分词结果
        self.cut_list = []
        # 依存关系
        self.arcs = None
        # 词性
        self.part_speech_list = []
        # 分词
        self.segmentor = Segmentor()
        self.segmentor.load_with_lexicon(os.path.join(self.LTP_DATA_DIR, 'cws.model'), self.cut_file)
        # 词性标注
        self.postagger = Postagger()
        self.postagger.load(os.path.join(self.LTP_DATA_DIR, 'pos.model'))
        # 命名实体识别
        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(os.path.join(self.LTP_DATA_DIR, 'ner.model'))
        # 依存句法分析
        self.parser = Parser()
        self.parser.load(os.path.join(self.LTP_DATA_DIR, 'parser.model'))
        # 语义角色标注
        self.labeller = SementicRoleLabeller()
        self.labeller.load(os.path.join(self.LTP_DATA_DIR, 'pisrl.model'))

        # 词性标注集
        self._dict = {"a": "形容词", "ni": "机构名称",
                      "b": "其他名词修饰语", "nl": "位置名词",
                      "c": "连词", "ns": "地名",
                      "d": "副词", "nt": "时态名词",
                      "e": "感叹", "nz": "其他专有名词",
                      "g": "词素", "o": "拟声词",
                      "h": "字首", "p": "介词",
                      "i": "成语", "q": "数量",
                      "j": "缩写", "r": "代词",
                      "k": "后缀", "u": "辅助的",
                      "m": "数", "v": "动词",
                      "n": "一般名词", "wp": "标点",
                      "nd": "方向名词", "ws": "外来词",
                      "nh": "人名", "x": "最小意义单位"}
        # 依存句法关系
        self._dict2 = {"SBV": "主谓关系",
                       "VOB": "动宾关系",
                       "IOB": "间宾关系",
                       "FOB": "前置宾语",
                       "DBL": "兼语",
                       "ATT": "定中关系",
                       "ADV": "状中结构",
                       "CMP": "动补结构",
                       "COO": "并列关系",
                       "POB": "介宾关系",
                       "LAD": "左附加关系",
                       "RAD": "右附加关系",
                       "IS": "独立结构",
                       "HED": "核心关系"}
        # 命名实体识别标注集
        self._idct3 = {"O": "这个词不是NE",
                       "S": "这个词单独构成一个NE",
                       "B": "这个词为一个NE的开始",
                       "I": "这个词为一个NE的中间",
                       "E": "这个词位一个NE的结尾"}
        self._dict4 = {"Nh": "人名",
                       "Ni": "机构名",
                       "Ns": "地名"}
        # 语义角色类型
        self._dict5 = {"ADV": "默认标记",
                       "BNE": "受益人",
                       "CND": "条件",
                       "DIR": "方向",
                       "DGR": "程度",
                       "EXT": "扩展",
                       "FRQ": "频率",
                       "LOC": "地点",
                       "MNR": "方式",
                       "PRP": "目的或原因",
                       "TMP": "时间",
                       "TPC": "主题",
                       "CRD": "并列参数",
                       "PRD": "谓语动词",
                       "PSR": "持有者",
                       "PSE": "被持有"}


    # 释放对象
    def colse_ltp(self):
        # 分词释放
        self.segmentor.release()
        # 词性释放
        self.postagger.release()
        # 实体释放
        self.recognizer.release()
        # 依存关系释放
        self.parser.release()
        # 语义角色释放
        self.labeller.release()


    # 分句
    def cut_split(self, msg):
        sents = SentenceSplitter.split(msg)
        return [i for i in sents]


    # 分词
    def cut_words(self, msg):
        words = self.segmentor.segment(msg)
        self.cut_list = [i for i in words]
        return self.cut_list


    # 词性标注
    def part_speech(self):
        postags = self.postagger.postag(self.cut_list)  # 词性标注
        self.part_speech_list = [i for i in postags]
        return self.part_speech_list


    # 实体识别
    def notional_words(self):
        return self.recognizer.recognize(self.cut_list, self.part_speech_list)  # 命名实体识别


    # 依存句法分析
    def interdependent(self):
        self.arcs = self.parser.parse(self.cut_list, self.part_speech_list)  # 句法分析
        return [(arc.head, arc.relation) for arc in self.arcs]


    # 语义角色标注
    def role(self):
        roles = self.labeller.label(self.cut_list, self.part_speech_list, self.arcs)  # 语义角色标注



if __name__=="__main__":
    _test = LTP_CLASS()
    _test.cut_words("")