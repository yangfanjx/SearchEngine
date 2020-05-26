#!/usr/bin/python
# -*- coding:utf-8 -*-
from SearchEngine.Code.Topic import Get_Topic
from SearchEngine.Code.Handle_msg import File_Del_Class
from SearchEngine.Code.Base_Function import traversal_folder, file_path
import json
import time
import os
from SearchEngine.Code.Wapper import wapper
import traceback
import xlrd

save_file_list = ["词语", "句子", "文章", "计数"]


@wapper
class Write_Read(object):
    def __init__(self, _debug=False):
        # debug调试文件夹路径设置
        if not _debug:
            from django.conf import settings
            self._folder = settings.READ_FILE
            self.save_file = dict(zip(save_file_list,
                                      [settings.SAVE_FILE+ i+".json" for i in
                                       save_file_list]))
        else:
            self._folder = "./Files/"
            self.save_file = dict(zip(save_file_list, ["{}{}.json".format(i) for i in save_file_list]))

        # 文章主题及分值与文件路径
        self.file_path = []
        # 句子列表，使用索引获取信息，避免重复加载，减少内存使用
        self.msg_list = []
        # 词所属的句子与文章信息
        self.use_dct = {}
        # 记录每个词在每篇文章中的数量
        self.word_nums = {}
        # 主题词提取方法实例
        self.get_topic = Get_Topic()
        # 过滤方法实例
        self.del_class = File_Del_Class()


    # 启动时检测是否需要重新处理数据
    def start_check(self):
        need_config = False
        for i in self.save_file.values():
            if not os.path.exists(i):
                need_config = True
                break

        # 需要重新加载数据时执行，不需要则直接读取、加载
        if need_config:
            print("Need write file")
            self.write_file()

        print("Have file,start read file")
        self.read_file()
        return (self.use_dct, self.msg_list, self.file_path, self.word_nums)


    # 将预处理的信息写入文件，避免每次启动重新预处理
    def write_file(self):
        # 计时
        tt = time.time()
        print(self._folder)
        # 遍历文件夹获取所有txt文件
        file_list = traversal_folder(self._folder, [], ".txt")
        print(file_list)
        # 文件路径添加到list中，获取源文件使用
        self.file_path = [{"topic": self.get_topic.topic_words(i), "file_path": i} for i in file_list]

        try:
            for _file_path in self.file_path:
                with open(_file_path["file_path"], encoding="utf-8") as f:
                    str = f.read()
                    str = str.replace(u'\u3000', u'').replace(u'\xa0', u'').replace(u"\t", u"")
                    msglist = str.splitlines()

                    for msg_line in msglist:
                        for msgs in msg_line.split("。"):

                            # 添加句子list
                            if msgs:
                                self.msg_list.append(msgs)
                                msgs = self.del_class.filter_del(msgs)

                                get_list = self.del_class.del_stop_words(msgs)
                                # 现记录所属句子与文章
                                for i in range(len(get_list) - 1):
                                    key_dict = self.use_dct.get(get_list[i], {})

                                    for j in range(i + 1, len(get_list)):
                                        if get_list[i] == get_list[j]:
                                            continue
                                        if j == i + 1:
                                            _dict = self.word_nums.get(get_list[i], {})
                                            _dict[get_list[j]] = _dict.get(get_list[j], 0) + 1
                                            self.word_nums[get_list[i]] = _dict
                                        value_list = key_dict.get(get_list[j], [])

                                        num_set = (len(self.msg_list) - 1, len(self.file_path) - 1)
                                        if num_set not in value_list:
                                            value_list.append(num_set)

                                        key_dict[get_list[j]] = value_list
                                    self.use_dct[get_list[i]] = key_dict
        except:
            print(traceback.print_exc())
            # print(_file_path,i, j)

        print('Handle file used: {} sec'.format(time.time() - tt))

        with open(self.save_file[save_file_list[0]], "w") as f:
            json.dump(self.use_dct, f)
            print("Write {} finish...".format(self.save_file[save_file_list[0]]))

        with open(self.save_file[save_file_list[1]], "w") as f:
            json.dump(self.msg_list, f)
            print("Write {} finish...".format(self.save_file[save_file_list[1]]))

        with open(self.save_file[save_file_list[2]], "w") as f:
            json.dump(self.file_path, f)
            print("Write {} finish...".format(self.save_file[save_file_list[2]]))

        with open(self.save_file[save_file_list[3]], "w") as f:
            json.dump(self.word_nums, f)
            print("Write {} finish...".format(self.save_file[save_file_list[3]]))


    def read_file(self):
        # 读取词语数据
        with open(self.save_file[save_file_list[0]], 'r') as load_f:
            self.use_dct = json.load(load_f)

        # 读取句子数据
        with open(self.save_file[save_file_list[1]], 'r') as load_f:
            self.msg_list = json.load(load_f)

        print(self.msg_list[:3])
        # 读取文章数据
        with open(self.save_file[save_file_list[2]], 'r') as load_f:
            self.file_path = json.load(load_f)

        print(self.file_path[:3])
        # 读取计数
        with open(self.save_file[save_file_list[3]], 'r') as load_f:
            self.word_nums = json.load(load_f)


    '''
    def read_file(self):
        global_print_dict = {}


        with open(self.save_file[save_file_list[0]], 'r') as load_f:
            self.use_dct = json.load(load_f)

            tt = time.time()
            for _k, _v in self.use_dct.items():
                if _k in self.del_class.stop_list:
                    continue
                add_value = {}
                for m_k, m_v in _v.items():
                    if m_k in self.del_class.stop_list:
                        continue
                    # if m_v > 3:
                    add_value[m_k] = m_v
                if add_value:
                    global_print_dict[_k] = add_value

                # if len(_v) > 2:
                #     add_value = {}
                #     for m_k, m_v in _v.items():
                #         if m_v > 5:
                #             add_value[m_k] = m_v
                #     if add_value:
                #         global_print_dict[_k] = add_value

            print('Read file used: {} sec'.format(time.time() - tt))
    '''


class Read_excel(object):
    def __init__(self, file_path):
        # 打开文件
        data = xlrd.open_workbook(file_path)

        # 查看工作表
        # data.sheet_names()
        # print("sheets：" + str(data.sheet_names()))
        #
        # # 通过文件名获得工作表,获取工作表1
        # table = data.sheet_by_name('工作表1')

        # 打印data.sheet_names()可发现，返回的值为一个列表，通过对列表索引操作获得工作表1
        self.table = data.sheet_by_index(0)

        # 获取行数和列数
        # 行数：table.nrows
        # 列数：table.ncols
        # print("总行数：" + str(table.nrows))
        # print("总列数：" + str(table.ncols))
        self.nrows = self.table.nrows
        self.ncols = self.table.ncols

        # 获取整行的值 和整列的值，返回的结果为数组
        # 整行值：table.row_values(start,end)
        # 整列值：table.col_values(start,end)
        # 参数 start 为从第几个开始打印，
        # end为打印到那个位置结束，默认为none
        # print("整行值：" + str(table.row_values(0)))
        # print("整列值：" + str(table.col_values(1)))


    def get_msg(self, row_num, clo_num):
        # 获取某个单元格的值，例如获取B3单元格值
        return self.table.cell(row_num, clo_num).value


    def get_row(self, row_num):
        return self.table.row_values(row_num)


if __name__ == "__main__":
    # msg_list = traversal_folder("./Files/", [])
    # print(msg_list)
    pass
