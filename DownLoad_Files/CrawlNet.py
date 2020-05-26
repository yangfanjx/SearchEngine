#!/usr/bin/python
# -*- coding: utf-8 -*-


import requests  # 导入requests包
from bs4 import BeautifulSoup
import csv
from SearchEngine.DownLoad_Files import Handle_Excel
from SearchEngine.DownLoad_Files.Handle_Word import Word_Table
import re

down_folder = "./download_file/"


# csv写入
class CSV_Class(object):
    def __init__(self, file_path):
        self.csvFile = open(file_path, "w", newline='')  # 创建csv文件  , encoding='utf-8'
        self.writer = csv.writer(self.csvFile)  # 创建写的对象


    def write_msg(self, title_list):
        self.writer.writerow(title_list)


    def stop_write(self):
        self.csvFile.close()


# 爬网
class CrawlClass(object):
    # Get形式获取网页内容
    @staticmethod
    def get_html(_url, use_type='GBK'):
        # headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        #            'Accept-Encoding': 'gzip,deflate,br',
        #            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        #            'Cache-Control': 'max-age=0',
        #            'Connection': 'keep-alive',
        #            'Cookie': 'JSESSIONID=5AA69E9392EE1DAE363949D193346BA4',
        #            'Host': 'www.ahzsks.cn',
        #            'Upgrade-Insecure-Requests': '1',
        #            "user-agent": "Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"}
        strhtml = requests.get(_url)  # Get方式获取网页数据
        strhtml.encoding = use_type
        return strhtml


    # 获取html中对象
    @staticmethod
    def get_element(thle_text, select_item):
        soup = BeautifulSoup(thle_text, 'lxml')
        data = soup.select(select_item)
        return data


    # 下载文件
    @staticmethod
    def download_file(_url, file_path):
        r = requests.get(_url)
        with open(file_path, "wb") as f:
            f.write(r.content)
        f.close()


    # 写入txt文件
    @staticmethod
    def write_txt(_txt, file_path):
        with open(file_path, "w") as f:
            _txt = _txt.replace(u'\xa0', u'')
            f.write(str(_txt))
        f.close()


# 北京
class BeiJing(object):
    '''
    北京进入二级页面以后获取<h1>同级别与子标签中的信息
    '''


    def __init__(self):
        self.start_url = 'https://www.bjeea.cn/html/selfstudy/'
        self.father_url = 'https://www.bjeea.cn'
        # 全年考试安排
        # self.QNKSAP = "div.main>div:nth-child(2)>div>div:nth-child(2)>div.top2>div:nth-child(1)>div>div> ul >li:nth-child(1)>a"
        # 自考重要日程安排
        # self.ZKZYRCAP = "div.main>div:nth-child(2)>div>div:nth-child(2)>div.top2>div:nth-child(1)>div>div> ul >li:nth-child(2)>a"
        # “快速通道”中链接
        self.all_links = "div.main>div:nth-child(2)>div>div:nth-child(2)>div.top2>div:nth-child(1)>div>div>ul>li>a"


    '''
    def get_msg(self):
        html_obj = CrawlClass.get_html(self.start_url)
        get_obj = CrawlClass.get_element(html_obj.text, self.QNKSAP)
        del html_obj
        if get_obj:
            sub_url = self.father_url + get_obj[0].get('href')
            sub_html = CrawlClass.get_html(sub_url)
            h1_obj = CrawlClass.get_element(sub_html.text, "h1")
            if h1_obj:
                parent_obj = h1_obj[0].parent
                # 将页面中的文字写入txt文件
                CrawlClass.write_txt(parent_obj.text, "./download_file/text.txt")
                # 遍历所有链接，将使用带有<u>的下载文件
                for i in parent_obj.select("div>p.MsoNormal>a"):
                    # all_span = i.find_all("span")
                    # if all_span:
                    #     for _s in all_span:
                    #         if _s.find_all("href"):
                    #             print(_s)
                    #         elif _s.text.split():
                    #             continue
                    #             print("".join(_s.text.split()))
                    children = i.find('u')
                    if children:
                        file_name = "./download_file/" + children.text.split(".")[1] + "." + i.get("href").split(".")[1]
                        CrawlClass.download_file(self.father_url + i.get("href"), file_name)
                        print("download file:{}".format(file_name))


    def test(self):
        html_obj = CrawlClass.get_html(self.start_url)
        get_obj = CrawlClass.get_element(html_obj.text, self.ZKZYRCAP)
        del html_obj
        if get_obj:
            sub_url = self.father_url + get_obj[0].get('href')
            sub_html = CrawlClass.get_html(sub_url)
            h1_obj = CrawlClass.get_element(sub_html.text, "h1")[0]

            table_obj = CrawlClass.get_element(sub_html.text, "table")[0]
            csv_obj = CSV_Class("./download_file/{}.csv".format(h1_obj.text))
            for _item in table_obj.select("tr"):
                write_list = []
                for _i in _item.select("td"):
                    write_list.append(str(_i.text.replace(u'\xa0', u'')))
                csv_obj.write_msg(write_list)

            csv_obj.stop_write()
    '''


    def handle_msg(self, text_obj):
        h1_obj = CrawlClass.get_element(text_obj, "h1")
        if h1_obj:
            # 有表格的只取表格信息
            if CrawlClass.get_element(text_obj, "table"):
                table_obj = CrawlClass.get_element(text_obj, "table")[0]
                csv_obj = CSV_Class("./download_file/{}.csv".format(h1_obj[0].text))
                max_len = 0
                for _index, _item in enumerate(table_obj.select("tr")):

                    write_list = []
                    for _i in _item.select("td"):
                        write_list.append(str(_i.text.replace(u'\xa0', u'')))
                    if _index and len(write_list) < max_len:
                        for _ in range(max_len - len(write_list)):
                            write_list.insert(0, "")
                    csv_obj.write_msg(write_list)
                    if _index == 0:
                        max_len = len(write_list)

                csv_obj.stop_write()
            else:
                parent_obj = h1_obj[0].parent
                # 将页面中的文字写入txt文件
                CrawlClass.write_txt(parent_obj.text, "{}/{}.txt".format(down_folder, h1_obj[0].text))
                # 遍历所有链接，将使用带有<u>的下载文件
                for i in parent_obj.select("div>p.MsoNormal>a"):
                    children = i.find('u')
                    if children:
                        file_name = down_folder + children.text.split(".")[1] + "." + i.get("href").split(".")[1]
                        CrawlClass.download_file(self.father_url + i.get("href"), file_name)
                        print("download file:{}".format(file_name))


    def all_page(self):
        html_obj = CrawlClass.get_html(self.start_url)
        get_obj = CrawlClass.get_element(html_obj.text, self.all_links)

        for _index, i in enumerate(get_obj):
            if _index == 4:
                break
            sub_url = self.father_url + i.get("href")
            sub_html = CrawlClass.get_html(sub_url)
            self.handle_msg(sub_html.text)


# 上海
class ShangHai(object):
    def __init__(self):
        self.start_url = "http://www.shzkw.org/"
        # 考试安排
        self.ksap = "http://www.shzkw.org/shksap/"
        self.all_links = "body > div.main.list-page > div.col-left > ul > li > a"


    # 网页抓取上海“自学考试各专业课程考试日程”网页table转Excel保存
    def handle_msg(self, text_obj):
        h1_obj = CrawlClass.get_element(text_obj, "h1")
        if h1_obj:
            # 有表格的只取表格信息

            if CrawlClass.get_element(text_obj, "table"):
                table_obj = CrawlClass.get_element(text_obj, "table")[0]
                # 中间环节转换为Excel保存路径
                xls_obj = Handle_Excel.Html_to_Excel("./download_file/{}.xls".format(h1_obj[0].text))
                try:
                    # 循环添加信息的起始行
                    current_row = 0
                    # 循环添加信息的起始列
                    current_col = 0
                    first_college = {}
                    for row_index, _item in enumerate(table_obj.select("tr")):
                        current_row = row_index - 1
                        # 第一行为名称，无用。
                        if row_index == 0:
                            continue
                        # 前两行特殊处理
                        elif row_index == 1:
                            # 第一行添加title与日期信息
                            # 表格没有划分“院校”title，添加
                            xls_obj.write_msg(0, 1, 0, 0, "院校")
                            # “专业”为固定项，直接添加
                            xls_obj.write_msg(0, 1, 1, 1, "专业")
                            current_col = 2
                            for col_index, _i in enumerate(_item.select("td")):
                                if col_index == 0:
                                    first_college["name"] = _i.text
                                    first_college["col"] = int(_i.get("rowspan", 0)) - 2
                                    continue
                                elif col_index < 2:
                                    continue
                                xls_obj.write_msg(current_row, current_row + int(_i.get("rowspan", 0)), current_col,
                                                  current_col + int(_i.get("colspan", 0)) - 1, _i.text)
                                current_col += int(_i.get("colspan", 1))
                            continue
                        elif row_index == 2:
                            # 第二行只有时间信息，切从第二列开始添加信息
                            current_col = 2
                            for col_index, _i in enumerate(_item.select("td")):
                                xls_obj.write_msg(current_row, current_row + int(_i.get("rowspan", 0)), current_col,
                                                  current_col + int(_i.get("colspan", 0)), _i.text)
                                current_col += int(_i.get("colspan", 1))
                            continue
                        elif row_index == 3:
                            # 第三行开始时，需要将第一个学校名称填入表格第一列
                            xls_obj.write_msg(2, 2 + first_college["col"] - 1, 0, 0, first_college["name"])
                        current_col = 1
                        for col_index, _i in enumerate(_item.select("td")):
                            # 学校列宽度为72，使用此条件过滤学校名称列
                            if _i.get("width") == "72":
                                current_col = 0
                                get_row = int(_i.get("rowspan", 0))
                                # 当个别学校只有一行信息时，不能减1
                                xls_obj.write_msg(current_row, current_row + (get_row - 1 if get_row else 0),
                                                  current_col,
                                                  current_col + int(_i.get("colspan", 0)), _i.text)
                                current_col += int(_i.get("colspan", 1))
                                continue
                            xls_obj.write_msg(current_row, current_row + int(_i.get("rowspan", 0)), current_col,
                                              current_col + int(_i.get("colspan", 0)), _i.text)
                            current_col += int(_i.get("colspan", 1))
                except:
                    print(current_row, current_row + int(_i.get("rowspan", 0)), current_col,
                          current_col + int(_i.get("colspan", 0)), _i.text)

                finally:
                    xls_obj.write_finish()

                    # write_list.append(str(_i.text.replace(u'\xa0', u'')))


    def all_page(self):
        html_obj = CrawlClass.get_html(self.ksap)
        get_obj = CrawlClass.get_element(html_obj.text, self.all_links)

        for _index, i in enumerate(get_obj):
            if _index == 1:
                break
            if "【" not in i.text and "2020年" in i.text:
                sub_url = i.get("href")
                sub_html = CrawlClass.get_html(sub_url)
                self.handle_msg(sub_html.text)


# 广东
class GuangDong(object):
    def __init__(self):
        self.start_url = "http://eea.gd.gov.cn/zxks/index.html"
        self.all_links = "body > div.main > div.content > ul > li > a"


    def all_page(self):
        html_obj = CrawlClass.get_html(self.start_url)
        get_obj = CrawlClass.get_element(html_obj.text, self.all_links)
        for _index, i in enumerate(get_obj):
            if "2020" in i.text and "考试时间" in i.text:
                _href = i.get('href')
                print(_href)
                sub_html = CrawlClass.get_html(_href)
                h1_obj = CrawlClass.get_element(sub_html.text, "h3")
                if h1_obj:
                    parent_obj = h1_obj[0].parent
                    p_list = parent_obj.select("p > a")
                    for i in p_list:
                        if i.get("href") and "时间安排" in i.text:
                            # _name = i.text.replace(".doc",".docx")
                            CrawlClass.download_file(i.get("href"), down_folder + i.text)
                            Word_Table.GuangDong_table("./download_file/" + i.text)


# 安徽
class AnHui(object):
    def __init__(self):
        self.start_url = "https://www.ahzsks.cn/gdjyzxks/"
        self.parent = "https://www.ahzsks.cn"
        self.all_links = "body > div.zk-main > div.container > div > div > div > h3"


    def all_page(self):
        html_obj = CrawlClass.get_html(self.start_url)
        get_obj = CrawlClass.get_element(html_obj.text, self.all_links)
        for _index, i in enumerate(get_obj):
            if i.select("font")[0].text == "考试安排":
                continue
                parent_obj = i.parent
                a_list = parent_obj.select("ul > li > a")
                for _i in a_list:
                    _title = _i.get("title")

                    if "2020" in _title and "自学考试" in _title and "安排" in _title:
                        _href = self.start_url + _i.get("href")
                        sub_html = CrawlClass.get_html(_href)
                        h1_obj = CrawlClass.get_element(sub_html.text, "h3")
                        if h1_obj:
                            parent_obj = h1_obj[0].parent
                            # print(parent_obj)
                            p_list = parent_obj.select("div > p > span > a")
                            for _a in p_list:
                                if "2020" in _a.text and "自学考试" in _a.text and "安排" in _a.text:
                                    down_link = self.parent + _a.get("href")
                                    print("Download url:{},local path:{}".format(down_link, down_folder + _a.text))
                                    # CrawlClass.download_file(down_link, down_folder + _a.text)
                                    print("Download file finish")
                                    gd_obj = Handle_Excel.GuangDong_Excel(down_folder + _a.text)
                                    gd_obj.handle()

            elif i.select("font")[0].text == "自考动态":
                parent_obj = i.parent
                a_list = parent_obj.select("ul > li > a")

                for _i in a_list:
                    _title = _i.get("title")

                    if "2020" in _title and "自学考试" in _title:
                        _href = self.start_url + _i.get("href")
                        sub_html = CrawlClass.get_html(_href)
                        h1_obj = CrawlClass.get_element(sub_html.text, "h3")

                        if h1_obj:
                            parent_obj = h1_obj[0].parent
                            # print(parent_obj)
                            p_list = parent_obj.select("div.content")
                            print(p_list[0].text.replace(u"\n", "").replace(" ", ""))


# 广西
class GuangXi(object):
    def __init__(self):
        self.start_url = "https://www.gxeea.cn/zxks/tzgg.htm"
        self.parent = "https://www.gxeea.cn"
        self.all_links = "body > div.g-doc.m-artcle-list > div.right-list.fr > div > ul > li > a"
        self.sub_links = "body > div.g-doc.m-detail > div.artcle-detail > p > a"


    def all_page(self):
        html_obj = CrawlClass.get_html(self.start_url)
        get_obj = CrawlClass.get_element(html_obj.text, self.all_links)
        for _index, i in enumerate(get_obj):

            if "2020" in i.text and "自学考试" in i.text and "安排" in i.text:
                _href = self.parent + str(i.get("href")).replace("..", "")
                sub_html = CrawlClass.get_html(_href)
                links_obj = CrawlClass.get_element(sub_html.text, self.sub_links)
                if links_obj:
                    for _i in links_obj:
                        if "2020" in _i.text and "课程考试" in _i.text and "安排" in _i.text:
                            print(_i.get("href"))
                            file_path = down_folder + _i.text + "." + _i.get("href").split(".")[-1]
                            CrawlClass.download_file(_i.get("href"), file_path)

                            gc_obj = Handle_Excel.GuangXi_Excel(file_path)
                            gc_obj.handle()


# 河北
class HeBei(object):
    def __init__(self):
        # body > table > tbody > tr > td > div > div.sub_right

        self.start_url = "http://www.hebeea.edu.cn/html/zxks/list.html"
        self.parent = "http://www.hebeea.edu.cn"
        self.all_links = "body>div>ul>li>div>a"
        self.sub_links = "body>div.sub_main2>table.con_content>tr>td>div>p>span>a"


    def all_page(self):
        html_obj = CrawlClass.get_html(self.start_url, "utf-8")
        # print(html_obj.text)
        get_obj = CrawlClass.get_element(html_obj.text, self.all_links)
        # print(get_obj)
        for _index, i in enumerate(get_obj):
            if "2020" in i.text and "自学考试" in i.text and "报考简章" in i.text:
                _href = self.parent + i.get("href")
                sub_html = CrawlClass.get_html(_href, "utf-8")
                links_obj = CrawlClass.get_element(sub_html.text, self.sub_links)
                if links_obj:
                    for _i in links_obj:
                        if _i.get("href"):

                            if "2020" in _i.text and "专业理论" in _i.text:
                                print(_i.get("href"))
                                file_path = down_folder + _i.text + "." + _i.get("href").split(".")[-1]
                                CrawlClass.download_file(_i.get("href"), file_path)

                                hb_obj = Handle_Excel.HeBei_Excel(file_path)
                                hb_obj.handle()


# 湖北
class HuBei(object):
    def __init__(self):
        self.start_url = "http://www.hbea.edu.cn/html/zxks/index.shtml"
        self.parent = "http://www.hbea.edu.cn"
        self.all_links = "#c01>table>table>tr>td>li>a"
        self.sub_links_10 = "#news>ul>div>div:nth-child(3) > p > a"
        self.sub_links_4 = "#news>ul>div>div:nth-child(3) > p > strong >a"


    def all_page(self):
        html_obj = CrawlClass.get_html(self.start_url, "utf-8")
        get_obj = CrawlClass.get_element(html_obj.text, self.all_links)
        for _index, i in enumerate(get_obj):
            if "2020" in i.text and "自学考试" in i.text and "报考" in i.text:
                _href = i.get("href")
                print(_href, i.get("title"))
                sub_html = CrawlClass.get_html(_href, "utf-8")
                if "4月" in i.text:
                    links_obj = CrawlClass.get_element(sub_html.text, self.sub_links_4)
                if "10月" in i.text:
                    links_obj = CrawlClass.get_element(sub_html.text, self.sub_links_10)
                if links_obj:
                    for _i in links_obj:
                        if "2020" in _i.text and "自学考试" in _i.text and "考试安排" in _i.text:
                            _href = self.parent + _i.get("href")
                            print(_i)
                        elif "请点击此处下载" in _i.text:
                            _href = self.parent + _i.get("href")
                            print(_i)
                        else:
                            continue

                        _name = down_folder + _href.split("/")[-1]
                        CrawlClass.download_file(_href, _name)


# 吉林
class JiLin(object):
    def __init__(self):
        self.start_url = "http://www.jleea.com.cn/zxks/"
        self.parent = "http://www.jleea.com.cn/"
        self.all_links = "body>div:nth-child(6)>div:nth-child(4)>div.border1.mbottom>div.main>ul>table >tr>td>a"
        self.sub_links = "#rightbox>div>span>a"


    def all_page(self):
        html_obj = CrawlClass.get_html(self.start_url, "GBK")
        get_obj = CrawlClass.get_element(html_obj.text, self.all_links)
        for _index, i in enumerate(get_obj):
            if "2020" in i.text and "自学考试" in i.text and "课程安排" in i.text:
                _href = self.parent + i.get("href")
                sub_html = CrawlClass.get_html(_href, "GBK")
                links_obj = CrawlClass.get_element(sub_html.text, self.sub_links)

                if links_obj:
                    for _i in links_obj:
                        if _i.get("href"):
                            if "2020" in _i.text and "自学考试" in _i.text and "课程安排" in _i.text:
                                _href = self.parent + _i.get("href")
                                print(_i)
                                _name = down_folder + _i.text
                                # CrawlClass.download_file(_href, _name)
                                # 需要将doc转为docx
                                _name = _name.replace(".doc", ".docx")
                                Word_Table.JiLin_table(_name)
                        else:
                            continue


# 江西
class JiangXi(object):
    def __init__(self):
        self.start_url = "http://www.jxeea.cn/index/zxks/ksap.htm"
        self.parent = "http://www.jxeea.cn/"
        self.all_links = "#line152488_3 > td > a"
        self.sub_links_list = ["#vsb_content > table:nth-child(22)", "#vsb_content > table:nth-child(25)"]


    def all_page(self):
        html_obj = CrawlClass.get_html(self.start_url, "utf-8")
        get_obj = CrawlClass.get_element(html_obj.text, self.all_links)
        for _index, i in enumerate(get_obj):
            if "2020" in i.text and "自学考试" in i.text and "课程安排" in i.text:
                _href = self.parent + i.get("href").replace("../", "")
                sub_html = CrawlClass.get_html(_href, "utf-8")

                for table_index, _table in enumerate(self.sub_links_list):
                    table_obj = CrawlClass.get_element(sub_html.text, _table)[0]
                    # 中间环节转换为Excel保存路径
                    xls_obj = Handle_Excel.Html_to_Excel(
                        "./download_file/{}.xls".format("JiangXi" + str(table_index)))

                    try:
                        # 循环添加信息的起始行
                        current_row = 0
                        # 循环添加信息的起始列
                        current_col = 0
                        for row_index, _item in enumerate(table_obj.select("tr")):
                            # 第一行为日期
                            if row_index == 0:
                                for col_index, _i in enumerate(_item.select("td")):
                                    if col_index == 0:
                                        xls_obj.write_msg(row_index, row_index, col_index, col_index, _i.text)
                                        current_col += 1
                                    else:
                                        _weight = int(_i.get("colspan")) - 1 if int(_i.get("colspan")) else 0
                                        xls_obj.write_msg(0, 0, current_col, current_col + _weight, _i.text)
                                        current_col += _weight + 1
                            elif row_index == 1:
                                for col_index, _i in enumerate(_item.select("td")):
                                    xls_obj.write_msg(row_index, row_index, col_index, col_index, _i.text)
                                    current_col += 1
                            elif row_index == 2:
                                current_row = 2
                                current_col = 0
                                continue
                            else:
                                use_col = 0
                                for col_index, _i in enumerate(_item.select("td")):
                                    _height = int(_i.get("rowspan", 0))
                                    if col_index == 0 and _height > 2:
                                        use_col = -1
                                        continue
                                    elif col_index == 0:
                                        use_col = 0

                                    current_col = col_index + use_col
                                    _height = 1 if _height == 2 else 0
                                    print(current_row, current_row + _height, current_col, current_col)
                                    xls_obj.write_msg(current_row, current_row + _height, current_col, current_col,
                                                      _i.text)

                                current_row += 1

                            '''
                            # 前两行特殊处理
                            elif row_index == 1:
                                # 第一行添加title与日期信息
                                # 表格没有划分“院校”title，添加
                                xls_obj.write_msg(0, 1, 0, 0, "院校")
                                # “专业”为固定项，直接添加
                                xls_obj.write_msg(0, 1, 1, 1, "专业")
                                current_col = 2
                                for col_index, _i in enumerate(_item.select("td")):
                                    if col_index == 0:
                                        first_college["name"] = _i.text
                                        first_college["col"] = int(_i.get("rowspan", 0)) - 2
                                        continue
                                    elif col_index < 2:
                                        continue
                                    xls_obj.write_msg(current_row,
                                                      current_row + int(_i.get("rowspan", 0)),
                                                      current_col,
                                                      current_col + int(_i.get("colspan", 0)) - 1,
                                                      _i.text)
                                    current_col += int(_i.get("colspan", 1))
                                continue
                            elif row_index == 2:
                                # 第二行只有时间信息，切从第二列开始添加信息
                                current_col = 2
                                for col_index, _i in enumerate(_item.select("td")):
                                    xls_obj.write_msg(current_row,
                                                      current_row + int(_i.get("rowspan", 0)),
                                                      current_col,
                                                      current_col + int(_i.get("colspan", 0)), _i.text)
                                    current_col += int(_i.get("colspan", 1))
                                continue
                            elif row_index == 3:
                                # 第三行开始时，需要将第一个学校名称填入表格第一列
                                xls_obj.write_msg(2, 2 + first_college["col"] - 1, 0, 0,
                                                  first_college["name"])
                            current_col = 1
                            for col_index, _i in enumerate(_item.select("td")):
                                # 学校列宽度为72，使用此条件过滤学校名称列
                                if _i.get("width") == "72":
                                    current_col = 0
                                    get_row = int(_i.get("rowspan", 0))
                                    # 当个别学校只有一行信息时，不能减1
                                    xls_obj.write_msg(current_row,
                                                      current_row + (get_row - 1 if get_row else 0),
                                                      current_col,
                                                      current_col + int(_i.get("colspan", 0)), _i.text)
                                    current_col += int(_i.get("colspan", 1))
                                    continue
                                xls_obj.write_msg(current_row, current_row + int(_i.get("rowspan", 0)),
                                                  current_col,
                                                  current_col + int(_i.get("colspan", 0)), _i.text)
                                current_col += int(_i.get("colspan", 1))
                        '''
                    except:
                        print("ERROR:", current_row, current_row + int(_i.get("rowspan", 0)), current_col,
                              current_col + int(_i.get("colspan", 0)), _i.text)

                    finally:
                        xls_obj.write_finish()

                        # write_list.append(str(_i.text.replace(u'\xa0', u'')))
                    Handle_Excel.JiangXi_Excel(xls_obj)


# 辽宁
class LiaoNing(object):
    def __init__(self):
        self.start_url = "http://www.lnzsks.com/listinfo/zxks_1.html"
        self.parent = "http://www.lnzsks.com/"
        self.all_links = "body>div.main.clearfix>ul>li>a"
        self.sub_links = "body>div.main.clearfix>div.info>div.content>p>a"
        self.table_header = "body>div>div>table>thead>tr>td"
        self.table_body = "body > div > div > table > tr"


    def all_page(self):
        def handle_special(m_msg):
            _code = re.findall(r"\d{3}/\d{6}", m_msg)[0]
            _name = re.sub(r"\d{3}/\d{6}", "", m_msg)
            return [_code, _name]


        def handle_calss(m_msg_list):
            return_list = []
            for i in zip(re.findall(r"\d{5}", m_msg_list), [i for i in re.split(r"\d{5}", m_msg_list) if i]):
                return_list.append({"calss_code": i[0], "class_name": i[1]})
            return return_list


        html_obj = CrawlClass.get_html(self.start_url, "utf-8")
        get_obj = CrawlClass.get_element(html_obj.text, self.all_links)
        for _index, i in enumerate(get_obj):
            if "2020" in i.text and "自学考试" in i.text and "报考简章" in i.text:
                _href = self.parent + i.get("href").replace("../", "")
                # print(_href)
                sub_html = CrawlClass.get_html(_href, "utf-8")
                links_obj = CrawlClass.get_element(sub_html.text, self.sub_links)
                if links_obj:
                    for _i in links_obj:
                        if _i.get("href"):
                            if "2020" in _i.text and "月考试课程安排表" in _i.text:

                                _href = _i.get("href")
                                table_html = CrawlClass.get_html(_href, "GBK")
                                heater_obj = CrawlClass.get_element(table_html.text, self.table_header)
                                date_time_list = []
                                for _msg in heater_obj:
                                    date_time_list.append(
                                        [i.replace(" ", "").replace(u"\r", "") for i in _msg.text.split(u"\n") if i])
                                print(date_time_list)

                                structured_dict = {}
                                _special_code = ""

                                body_obj = CrawlClass.get_element(table_html.text, self.table_body)
                                for _tr in body_obj:
                                    msg_list = []
                                    for _index, _td in enumerate(_tr.select("td")):
                                        if _td.text:
                                            if _index == 0:
                                                special_msg = _td.text.replace(u"\n", "")
                                                _special_code, _special_name = handle_special(special_msg)
                                            else:
                                                dict_list = handle_calss(
                                                    _td.text.replace(" ", "").replace(u"\r", "").replace(u"\n", ""))
                                                for __dict in dict_list:
                                                    __dict["date"] = date_time_list[_index][0]
                                                    __dict["time"] = date_time_list[_index][1]
                                                    __dict["special_code"] = _special_code
                                                    __dict["special_name"] = _special_name
                                                    msg_list.append(__dict)
                                        else:
                                            continue
                                    structured_dict[_special_code] = msg_list
                                print(structured_dict)
                        else:
                            continue


# 山西
class ShanXi(object):
    def __init__(self):
        self.start_url = "http://www.sxkszx.cn/ksfwpt.html"
        self.parent = "http://www.sxkszx.cn/"
        self.all_links = "#nav > ul > li:nth-child(4) > div > div > dl:nth-child(2) > dd > a"
        self.sub_links = ["#newsbody_class > div:nth-child(4) > table", "#newsbody_class > div:nth-child(8) > table"]


    def all_page(self):
        def handle_special(m_msg):
            _code = re.findall(r"\d{3}/\d{6}", m_msg)[0]
            _name = re.sub(r"\d{3}/\d{6}", "", m_msg)
            return [_code, _name]


        def handle_calss(m_msg_list):
            print(m_msg_list)
            return_list = []
            for i in zip(re.findall(r"[（](\d{5})[）]", m_msg_list),
                         [i for i in re.split(r"[（](\d{5})[）]", m_msg_list) if i]):
                return_list.append({"calss_code": i[0], "class_name": i[1]})
            return return_list


        html_obj = CrawlClass.get_html(self.start_url, "utf-8")
        get_obj = CrawlClass.get_element(html_obj.text, self.all_links)
        for _index, i in enumerate(get_obj):
            if "2020" in i.text and "考试课程" in i.text and "时间" in i.text:
                _href = self.parent + i.get("href").replace("../", "")
                print(_href)
                sub_html = CrawlClass.get_html(_href, "utf-8")
                h1_obj = CrawlClass.get_element(sub_html.text, "#newsbody_class>div>table>tbody")

                date_list = []
                time_list = []
                max_col = 7
                for table_obj in h1_obj:
                    for _num, _tr in enumerate(table_obj.select("tr")):
                        if _num == 0:
                            continue
                        if _num == 1:
                            for _td in _tr.select("td"):
                                add_msg = _td.text.replace(u"\n", "")
                                if add_msg in date_list:
                                    continue
                                else:
                                    date_list.append(add_msg)
                        elif _num == 2:
                            for _td in _tr.select("td"):
                                add_msg = _td.text.replace(u"\n", "")
                                if add_msg in time_list:
                                    continue
                                else:
                                    time_list.append(add_msg)
                        else:
                            special_code = ""
                            special_name = ""
                            for _ind, _td in enumerate(_tr.select("td")):
                                if _ind in (0, max_col):
                                    continue
                                elif _ind == 1:
                                    special_code = _td.text.replace(u"\n", "")
                                elif _ind == 2:
                                    special_name = _td.text.replace(u"\n", "")
                                else:
                                    print(_td)
                                    print(CrawlClass.get_element(_td.text, "div>span"))
                                    # print(_td.select("span"))
                                    # print(handle_calss(_td.select("div>span")))

                        # print(_tr)
                    # print(tabls_obj)
                # for _table in self.sub_links:
                #     links_obj = CrawlClass.get_element(sub_html.text, _table)
                #     print(links_obj)
                #     # for _tr in body_obj:
                #     #     msg_list = []
                #     #     for _index, _td in enumerate(_tr.select("td")):
                #     #         if _td.text:
                #     #             if _index == 0:
                #     #                 special_msg = _td.text.replace(u"\n", "")
                #     #                 _special_code, _special_name = handle_special(special_msg)
                #     #             else:
                #     #                 dict_list = handle_calss(
                #     #                     _td.text.replace(" ", "").replace(u"\r", "").replace(u"\n", ""))
                #     #                 for __dict in dict_list:
                #     #                     __dict["date"] = date_time_list[_index][0]
                #     #                     __dict["time"] = date_time_list[_index][1]
                #     #                     __dict["special_code"] = _special_code
                #     #                     __dict["special_name"] = _special_name
                #     #                     msg_list.append(__dict)
                #     #         else:
                #     #             continue
                #     #     structured_dict[_special_code] = msg_list
                #     # print(structured_dict)
                break


# 浙江：PDF，云南：图片，新疆：图片

if __name__ == "__main__":
    # bj = BeiJing()
    # bj.all_page()
    test = AnHui()
    test.all_page()
