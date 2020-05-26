#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlrd
import xlwt
import re


# 读取html页面中的表格，转为Excel方便结构化
class Html_to_Excel(object):
    def __init__(self, file_path):
        self.path = file_path
        self.workbook = xlwt.Workbook()
        self.worksheet = self.workbook.add_sheet('My sheet')
        self.chrrent_ctart_row = 0
        self.current_start_col = 0
        # 合并第0行的第0列到第3列。
        # worksheet.write_merge(0, 0, 0, 3, 'First Merge')
        # font = xlwt.Font()
        # font.blod = True

        # pattern_top = xlwt.Pattern()
        # pattern_top.pattern = xlwt.Pattern.SOLID_PATTERN
        # pattern_top.pattern_fore_colour = 5

        # style = xlwt.XFStyle()
        # style.font = font
        # style.pattern = pattern_top

        # 合并第1行到第2行的第0列到第3列。
        # worksheet.write_merge(1, 2, 0, 3, 'Second Merge', style)

        # worksheet.write_merge(4, 6, 3, 6, 'My merge', style)

        # workbook.save('E:\\test\\xls_xlwt\Merge_cell.xls')


    def set_current_point(self, rows, cols):
        self.chrrent_ctart_row = rows
        self.current_start_col = cols


    def write_msg(self, row_start, row_end, col_start, col_end, _msg):
        self.worksheet.write_merge(row_start, row_end, col_start, col_end, _msg)


    def write_finish(self):
        self.workbook.save(self.path)


class Excel_Function(object):

    @staticmethod
    def read_excel(file_path):
        # 获取数据
        data = xlrd.open_workbook(file_path)
        # 获取所有sheet名字
        sheet_names = data.sheet_names()
        for sheet in sheet_names:
            # 获取sheet
            table = data.sheet_by_name(sheet)

            table._cell_types
            table._cell_values
            # 获取总行数
            nrows = table.nrows  # 包括标题
            # 获取总列数
            ncols = table.ncols

            # 计算出合并的单元格有哪些
            colspan = {}
            if table.merged_cells:
                for item in table.merged_cells:
                    for row in range(item[0], item[1]):
                        for col in range(item[2], item[3]):
                            # 合并单元格的首格是有值的，所以在这里进行了去重
                            if (row, col) != (item[0], item[2]):
                                colspan.update({(row, col): (item[0], item[2])})
            # 读取每行数据
            for i in range(3, nrows):
                row = []
                for j in range(ncols):
                    # 假如碰见合并的单元格坐标，取合并的首格的值即可
                    if colspan.get((i, j)):
                        row.append(table.cell_value(*colspan.get((i, j))))
                    else:
                        row.append(table.cell_value(i, j))
                print(row)

            # 读取每列数据
            for j in range(ncols):
                col = []
                for i in range(1, nrows):
                    # 假如碰见合并的单元格坐标，取合并的首格的值即可
                    if colspan.get((i, j)):
                        col.append(table.cell_value(*colspan.get((i, j))))
                    else:
                        col.append(table.cell_value(i, j))
                print(col)


    # 获取Excel中表格的起止行坐标
    def get_start_end(self, table_obj, rows, clos):
        start_row_list = []
        end_row_list = []

        number_clo = 0
        for i in range(rows):
            # 通过“序号”标定首行
            for j in range(clos):
                if table_obj.cell_value(i, j) == "序号":
                    start_row_list.append(i)
                    number_clo = j

            if table_obj.cell_value(i, 0) == "序号":
                start_row_list.append(i)
            elif table_obj.cell_value(i, 0):
                try:
                    int(table_obj.cell_value(i, 0))
                except:
                    if len(start_row_list) != len(end_row_list):
                        end_row_list.append(i - 1)
                    continue
            else:
                all_empty = True
                for j in range(clos):
                    if table_obj.cell_value(i, j):
                        all_empty = False
                if all_empty:
                    end_row_list.append(i - 1)
        pass



# 北京
class BeiJing_Excel(object):
    # 考试安排
    @staticmethod
    def bj_time(file_path):
        # 获取数据
        data = xlrd.open_workbook(file_path)

        # 获取sheet
        table = data.sheet_by_index(0)

        # table._cell_types
        # table._cell_values
        # 获取总行数
        nrows = table.nrows  # 包括标题
        # 获取总列数
        ncols = table.ncols

        day_list = []  # 日期
        time_list = []  # 时间
        group_list = []  # 单元序号
        title_list = []  # 项名称

        for j in range(3, ncols):
            _day = table.cell_value(3, j)
            if _day:
                day_list.append(_day)
        # print(day_list)

        for j in range(3, ncols):
            _group = table.cell_value(4, j)
            if _group and _group not in group_list:
                group_list.append(_group)
        # print(group_list)

        for j in range(3, ncols):
            _time = table.cell_value(5, j)
            if _time and _time not in time_list:
                time_list.append(_time)
        # print(time_list)

        for j in range(1, ncols):
            _title = table.cell_value(6, j)
            if _title and _title not in title_list:
                title_list.append(_title)
        # print(title_list)

        structured_dict = {}  # 结构化返回对象

        # 正式开始遍历表格中的信息
        _current_code = _current_name = ""  # 由于合并单元格，只有第一格有信息，需要记录合并单元格中的信息添加但所有所属格中
        for i in range(7, nrows):
            try:
                # 序号列为数字，表格最下方备注为非数字，使用强转数字判断考试信息是否已经遍历完。
                if table.cell_value(i, 0):
                    int(table.cell_value(i, 0))
            except:
                continue

            class_code = ""
            for j in range(ncols):
                if j == 0:
                    continue
                if j == 1:
                    # 获取当前专业代码，如遇到合并单元格导致信息为空，则使用合并的信息
                    _current_code = table.cell_value(i, j) if table.cell_value(i, j) else _current_code
                    continue
                elif j == 2:
                    # 专业名称，同上专业代码
                    _current_name = table.cell_value(i, j) if table.cell_value(i, j) else _current_name

                    if not structured_dict.get(_current_code):
                        structured_dict[_current_code] = {title_list[1]: _current_name, "包含": []}
                    continue
                _msg = table.cell_value(i, j)
                if _msg:
                    date_index = (j - 3) // 4  # 由于日期从第四列单元格起，覆盖4列信息。使用index查找科目所属的时间
                    time_index = ((j - 3) // 2) % 2  # 同日期

                    if (j - 3) % 2 == 0:
                        class_code = _msg
                        continue
                    if (j - 3) % 2 == 1:
                        structured_dict[_current_code]["包含"].append({
                            title_list[2]: class_code,
                            title_list[3]: _msg, "日期": day_list[
                                date_index], "时间": time_list[time_index]})
                else:
                    continue

        print(structured_dict)


    @staticmethod
    def bj_others(file_path):
        # 获取数据
        data = xlrd.open_workbook(file_path)

        # 获取sheet
        table = data.sheet_by_index(0)
        nrows = table.nrows  # 包括标题
        # 获取总列数
        ncols = table.ncols

        # 当一个Excel中存在多个表格时，需要找到多个表格的起止行
        start_row_list = []
        end_row_list = []
        for i in range(nrows):
            # 通过“序号”标定首行
            if table.cell_value(i, 0) == "序号":
                start_row_list.append(i)
            elif table.cell_value(i, 0):
                try:
                    int(table.cell_value(i, 0))
                except:
                    if len(start_row_list) != len(end_row_list):
                        end_row_list.append(i - 1)
                    continue
            else:
                all_empty = True
                for j in range(ncols):
                    if table.cell_value(i, j):
                        all_empty = False
                if all_empty:
                    end_row_list.append(i - 1)

        start_end = zip(start_row_list, end_row_list)
        # print([i for i in start_end])

        for _item in start_end:
            title_list = []
            for j in range(ncols):
                get_msg = table.cell_value(_item[0], j)
                if get_msg:
                    title_list.append(get_msg)

            structured_dict = {}
            for i in range(_item[0] + 1, _item[1]):
                msg_dict = {}
                multi_lines = {}
                for j in range(1, ncols):

                    if isinstance(table.cell_value(i, j), str) and len(table.cell_value(i, j).split()) > 1:
                        multi_lines[title_list[j]] = (table.cell_value(i, j).split())
                    else:
                        msg_dict[title_list[j]] = table.cell_value(i, j)

                if multi_lines:
                    all_len = len(multi_lines.values()[0])
                    for i in range(all_len):
                        for _k, _v in multi_lines:
                            msg_dict[_k] = _v[i]
                        structured_dict[table.cell_value(i, 1)] = msg_dict

                else:
                    structured_dict[table.cell_value(i, 1)] = msg_dict
            print(structured_dict)


    @staticmethod
    def bj_others_bak(file_path):
        # 获取数据
        data = xlrd.open_workbook(file_path)

        # 获取sheet
        table = data.sheet_by_index(0)
        nrows = table.nrows  # 包括标题
        # 获取总列数
        ncols = table.ncols

        start_row_list = []
        end_row_list = []
        for i in range(nrows):
            if table.cell_value(i, 0) == "序号":
                start_row_list.append(i)
            elif table.cell_value(i, 0):
                try:
                    int(table.cell_value(i, 0))
                except:
                    if len(start_row_list) != len(end_row_list):
                        end_row_list.append(i - 1)
                    continue
            else:
                all_empty = True
                for j in range(ncols):
                    if table.cell_value(i, j):
                        all_empty = False
                if all_empty:
                    end_row_list.append(i - 1)

        start_end = zip(start_row_list, end_row_list)
        # print([i for i in start_end])

        for _item in start_end:
            title_list = []
            for j in range(ncols):
                get_msg = table.cell_value(_item[0], j)
                if get_msg:
                    title_list.append(get_msg)

            structured_dict = {}
            for i in range(_item[0] + 1, _item[1]):
                msg_dict = {}
                multi_lines = {}
                for j in range(1, ncols):

                    if isinstance(table.cell_value(i, j), str) and len(table.cell_value(i, j).split()) > 1:
                        multi_lines[title_list[j]] = (table.cell_value(i, j).split())
                    else:
                        msg_dict[title_list[j]] = table.cell_value(i, j)

                if multi_lines:
                    all_len = len(multi_lines.values()[0])
                    for i in range(all_len):
                        for _k, _v in multi_lines:
                            msg_dict[_k] = _v[i]
                        structured_dict[table.cell_value(i, 1)] = msg_dict

                else:
                    structured_dict[table.cell_value(i, 1)] = msg_dict
            print(structured_dict)


# 上海
class ShangHai_Excel(object):
    # 上海专业
    def re_msg_speciality(self, _msg):
        get_msg = ''.join(re.findall(r'[\u4E00-\u9FFFA-Za-z0-9(（）)]', str(_msg)))
        get_code = re.findall('[A-Za-z0-9]+', get_msg)[0]
        get_name = re.sub('[A-Za-z0-9]+', "", get_msg)
        return {"code": get_code, "name": get_name}


    def re_msg_class(self, _msg):
        re_msg = ''.join(re.findall(r'[\u4E00-\u9FFFA-Za-z0-9(（）)*]', str(_msg)))
        return_dict = dict(zip([(re.findall(r'[(](.*?)[)]', i))[0] for i in re_msg.split("*") if i],
                               [(re.sub('\([A-Za-z0-9]+\)', "", i)) for i in re_msg.split("*") if i]))
        return return_dict


    def handle(self, file_path):
        # 获取数据
        data = xlrd.open_workbook(file_path)

        # 获取sheet
        table = data.sheet_by_index(0)

        # table._cell_types
        # table._cell_values
        # 获取总行数
        nrows = table.nrows  # 包括标题
        # 获取总列数
        ncols = table.ncols

        structured_dict = {}
        day_list = []
        time_list = []
        college_list = []
        college_rows = []
        for i in range(1, nrows):
            college = table.cell_value(i, 0)
            if college:
                college_rows.append(i)
                college_list.append(college)
        print(college_rows, college_list)

        for j in range(2, ncols):
            _day = table.cell_value(0, j)
            if _day:
                day_list.append(str(_day.replace(u'\xa0', u'')))

        for j in range(2, ncols):
            _time = table.cell_value(1, j)
            _time = str(_time.replace(u'\xa0', u''))
            if _time and _time not in time_list:
                time_list.append(_time)

        for i in range(2, nrows):
            speciality_dict = {}
            for j in range(1, ncols):
                if j == 1:
                    a = self.re_msg_speciality(table.cell_value(i, j))
                    # print(a)
                else:
                    self.re_msg_class(table.cell_value(i, j))


# 广东
class GuangDong_Excel(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.day_row = 2  # 日期行的行坐标
        self.time_row = 3  # 时间行的行坐标
        self.speciality_col = 2  # 专业列的列坐标
        self.skip_row = [0, 1]  # 跳过行坐标，如空行或标题行
        self.skip_col = [0, 1]  # 跳过列坐标，如空列或序号列
        self.day_list = []  # 日期信息保存列表
        self.time_list = []  # 时间信息保存列表


    def handle(self):
        # 获取数据
        data = xlrd.open_workbook(self.file_path)

        # 获取sheet
        table = data.sheet_by_index(0)

        # table._cell_types
        # table._cell_values
        # 获取总行数
        nrows = table.nrows  # 包括标题
        # 获取总列数
        ncols = table.ncols

        for j in range(ncols):
            if j in self.skip_col:
                continue
            if j == self.speciality_col:
                continue
            _day = table.cell_value(self.day_row, j)
            if _day:
                self.day_list.append(str(_day.replace(u'\xa0', u'')))

        for j in range(ncols):
            if j in self.skip_col:
                continue
            if j == self.speciality_col:
                continue
            _time = table.cell_value(self.time_row, j)
            _time = str(_time.replace(u'\xa0', u''))
            if _time:  # and _time not in self.time_list
                self.time_list.append(_time)

        structured_dict = {}

        for i in range(self.time_row + 1, nrows):
            msg_list = []
            _special_code = ""
            for j in range(self.speciality_col, ncols):
                if j == self.speciality_col:
                    if "（" in table.cell_value(i, j):
                        _special_name, _special_code = table.cell_value(i, j).split("（")
                    elif "(" in table.cell_value(i, j):
                        _special_name, _special_code = table.cell_value(i, j).split("(")
                    else:
                        break
                    _special_code = _special_code[:-1]
                else:
                    for _item in table.cell_value(i, j).split():
                        m_dict = {}
                        m_dict["special_code"] = _special_code
                        m_dict["special_name"] = _special_name
                        m_dict["class_name"], _class_code = _item.split("（")
                        m_dict["class_code"] = _class_code[:-1]

                        m_dict["date"] = self.day_list[(j - self.speciality_col - 1) // 2 % 2]
                        m_dict["time"] = self.time_list[(j - self.speciality_col - 1)]

                        msg_list.append(m_dict)
            structured_dict[_special_code] = msg_list
        print(structured_dict)


# 广西
class GuangXi_Excel(object):
    def __init__(self, file_path):
        self.file_path = file_path
        if "4月" in file_path:
            self.day_row = 3  # 日期行的行坐标
            self.time_row = 4  # 时间行的行坐标
            self.skip_row = [0, 1, 2]  # 跳过行坐标，如空行或标题行
        else:
            self.day_row = 2  # 日期行的行坐标
            self.time_row = 3  # 时间行的行坐标
            self.skip_row = [0, 1]  # 跳过行坐标，如空行或标题行
        self.speciality_col = 0  # 专业列的列坐标
        self.skip_col = []  # 跳过列坐标，如空列或序号列
        self.day_list = []  # 日期信息保存列表
        self.time_list = []  # 时间信息保存列表


    def handle(self):

        def handle_msg(_msg):
            _code, _name = _msg.split("-")
            return _code, _name


        # 获取数据
        data = xlrd.open_workbook(self.file_path)

        # 获取sheet
        table = data.sheet_by_index(0)

        # table._cell_types
        # table._cell_values
        # 获取总行数
        nrows = table.nrows  # 包括标题
        # 获取总列数
        ncols = table.ncols
        self.skip_col.append(ncols - 1)

        for i in range(self.day_row, nrows):
            if table.cell_value(i, 0) == "专业名称" and table.cell_value(i, ncols - 1) == "备注":
                self.skip_row.append(i)
                self.skip_row.append(i + 1)

            # elif not table.cell_value(i, ncols - 1) and "课程考试时间安排表" in table.cell_value(i, 0):
            #     self.skip_row.append(i)
            elif not table.cell_value(i, ncols - 1) and table.cell_value(i, 0):
                self.skip_row.append(i)
            else:
                have_msg = False
                for j in range(ncols):
                    if table.cell_value(i, j):
                        have_msg = True
                        break
                if not have_msg:
                    self.skip_row.append(i)

        print(self.skip_row)
        for j in range(1, ncols):
            if j == ncols - 1:
                continue
            _day = table.cell_value(self.day_row, j)
            if _day:
                self.day_list.append(_day)

        for j in range(1, ncols):
            if j == ncols - 1:
                continue
            _time = table.cell_value(self.time_row, j)
            if _time:
                self.time_list.append(_time)

        structured_dict = {}
        current_special = ""
        _code = ""
        msg_list = []
        for i in range(self.time_row + 1, nrows):
            if i in self.skip_row:
                continue
            for j in range(self.speciality_col, ncols):
                if j in self.skip_col:
                    continue
                if j == self.speciality_col and table.cell_value(i, j):
                    if msg_list:
                        _code, _ = handle_msg(current_special)
                        get_list = structured_dict.get(_code, [])
                        get_list += msg_list
                        structured_dict[_code] = get_list
                    current_special = table.cell_value(i, j)

                    msg_list = []

                elif table.cell_value(i, j):
                    if not current_special:
                        print("row:{},col:{},current_special:{},msg:{}".format(i, j, current_special,
                                                                               table.cell_value(i, j)))
                    m_dict = {}
                    m_dict["special_code"], m_dict["special_name"] = handle_msg(current_special)
                    m_dict["class_code"], m_dict["class_name"] = handle_msg(table.cell_value(i, j))
                    m_dict["date"] = self.day_list[(j - self.speciality_col - 1) // 2 % 2]
                    m_dict["time"] = self.time_list[(j - self.speciality_col - 1)]
                    msg_list.append(m_dict)
                else:
                    continue

        structured_dict[_code] = msg_list
        print(structured_dict)


# 河北
class HeBei_Excel(object):
    def __init__(self, file_path):
        self.file_path = file_path
        if "4月" in file_path:
            self.day_row = 0  # 日期行的行坐标
        else:
            self.day_row = 0  # 日期行的行坐标
        self.speciality_col = [1, 2]  # 专业列的列坐标
        self.day_list = []  # 日期信息保存列表


    def handle(self):

        # 获取数据
        data = xlrd.open_workbook(self.file_path)

        structured_dict = {}
        # 获取sheet
        for _item in data.sheet_names():
            table = data.sheet_by_name(_item)
            # 获取总行数
            nrows = table.nrows  # 包括标题
            # 获取总列数
            ncols = table.ncols

            for j in range(3, ncols):
                _day = table.cell_value(self.day_row, j)
                if _day:
                    self.day_list.append(_day)

            current_special = []
            msg_list = []
            for i in range(self.day_row + 2, nrows):
                for j in range(self.speciality_col[0], ncols):
                    current_msg = table.cell_value(i, j)
                    if j in self.speciality_col and current_msg:
                        if not current_special:
                            msg_list = []
                            current_special.append(current_msg)
                        elif current_msg not in current_special and len(current_special) == 2:
                            # 此行专业变动
                            get_list = structured_dict.get(current_special[0], [])
                            get_list += msg_list
                            structured_dict[current_special[0]] = get_list
                            current_special = []
                            current_special.append(current_msg)
                            continue
                        elif current_msg not in current_special:
                            current_special.append(current_msg)
                        else:
                            continue

                    elif current_msg:
                        if (j - 2) % 2 == 1:
                            m_dict = {}
                            m_dict["class_code"] = current_msg
                        else:
                            m_dict["class_name"] = current_msg
                            m_dict["special_code"], m_dict["special_name"] = current_special
                            m_dict["date"] = self.day_list[((j - 2) // 2) - 1]
                            msg_list.append(m_dict)
                    else:
                        continue

        print(structured_dict)


# 江西
class JiangXi_Excel(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.day_row = 0  # 日期行的行坐标
        self.time_row = 1
        self.speciality_col = [0]  # 专业列的列坐标
        self.day_list = []  # 日期信息保存列表
        self.time_list = []


    def handle(self):

        # 获取数据
        data = xlrd.open_workbook(self.file_path)

        structured_dict = {}
        # 获取sheet
        for _item in data.sheet_names():
            table = data.sheet_by_name(_item)
            # 获取总行数
            nrows = table.nrows  # 包括标题
            # 获取总列数
            ncols = table.ncols

            for j in range(3, ncols):
                _day = table.cell_value(self.day_row, j)
                if _day:
                    self.day_list.append(_day)

            current_special = []
            msg_list = []
            for i in range(self.day_row + 2, nrows):
                for j in range(self.speciality_col[0], ncols):
                    current_msg = table.cell_value(i, j)
                    if j in self.speciality_col and current_msg:
                        if not current_special:
                            msg_list = []
                            current_special.append(current_msg)
                        elif current_msg not in current_special and len(current_special) == 2:
                            # 此行专业变动
                            get_list = structured_dict.get(current_special[0], [])
                            get_list += msg_list
                            structured_dict[current_special[0]] = get_list
                            current_special = []
                            current_special.append(current_msg)
                            continue
                        elif current_msg not in current_special:
                            current_special.append(current_msg)
                        else:
                            continue

                    elif current_msg:
                        if (j - 2) % 2 == 1:
                            m_dict = {}
                            m_dict["class_code"] = current_msg
                        else:
                            m_dict["class_name"] = current_msg
                            m_dict["special_code"], m_dict["special_name"] = current_special
                            m_dict["date"] = self.day_list[((j - 2) // 2) - 1]
                            msg_list.append(m_dict)
                    else:
                        continue

        print(structured_dict)


if __name__ == "__main__":
    _obj = GuangXi_Excel("F:\GitHub\爬虫\DownLoad\download_file\\广西2020年高等教育自学考试10月课程考试时间安排表.xls")
    _obj.handle()
