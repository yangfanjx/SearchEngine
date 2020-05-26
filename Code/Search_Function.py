#!/usr/bin/python
# -*- coding:utf-8 -*-
import copy
from SearchEngine.Code.Base_Function import jieba_cut


# 搜索功能
class Search_Function(object):

    def __init__(self, _use_set):
        self.use_dct, self.msg_list, self.file_path, self.word_nums = _use_set


    def __topic_word(self):
        # print(self.word_nums)
        for i in self.word_nums.keys():
            print(self.word_nums[i])
            break

    # test_msg = "学生考试"
    def search_function(self, _msg):

        self.__topic_word()
        # test_msg = input("输入查询信息")

        use_list = [i for i in jieba_cut(_msg) if len(i) > 1]

        use_search_dict = {}
        for _index, i in enumerate(use_list):
            use_copy = copy.deepcopy(use_list)
            use_copy.pop(_index)
            use_search_dict[i] = use_copy
        print(use_search_dict)

        append_list = []
        for _k, _v in use_search_dict.items():
            for m_v in _v:
                try:
                    append_list.append(self.use_dct[_k][m_v])
                except:
                    append_list.append(self.use_dct[_k])

            # print(global_print_dict[i])

        print(append_list)

        _use_list = append_list[0]
        for i in append_list:
            _use_list = [m_i for m_i in i if m_i in _use_list]

        print(_use_list)
        for i in _use_list:
            print(i[0])
            print(self.msg_list[i[0]])
        return [self.msg_list[i[0]] for i in _use_list]
