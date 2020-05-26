#!/usr/bin/python
# -*- coding: utf-8 -*-

'''公共常用方法'''
import requests  # 导入requests包
# import jieba
from SearchEngine.Code.LTP import LTP_CLASS
import os
from django.conf import settings
import pandas as pd
from http import cookiejar
from urllib import request, parse
from io import BytesIO
import gzip
from bs4 import BeautifulSoup
import re
import chardet
import ssl


# import Levenshtein


# 拼接文件路径
def file_path(_folder, _file):
    result = os.path.join(_folder, _file)
    use = result.split("\\")
    print(use)
    result = ""
    for i in use:
        result += i + "\\"
    print(result)
    result = result[:-1]
    print(result)
    return result


# 为减少jieba加载次数，统一在此处使用
def jieba_cut(msg):
    ltp_obj = LTP_CLASS()
    return ltp_obj.cut_words(msg)


# 遍历文件夹及子文件夹中的所有文件
def traversal_folder(folder_path, add_list, file_type):
    print(folder_path)
    if os.path.isfile(folder_path) and folder_path.endswith(file_type):
        add_list.append(folder_path)
    elif os.path.isdir(folder_path):
        for _folder in os.listdir(folder_path):
            traversal_folder(os.path.join(folder_path, _folder), add_list, file_type)
    return add_list


# 读取过滤规则
def get_del_filter():
    df = pd.read_csv(settings.USE_FILE + "ai_filter_rule.csv", encoding='utf-8')
    return df


# 爬网类
class Reuqest_Class(object):

    @staticmethod
    def have_cookie(_url, _header=None):

        # 通过cookieJar（）类构建一个cookieJar（）对象，用来保存cookie的值

        cookie = cookiejar.CookieJar()

        # 通过HTTPCookieProcessor（）处理器类构建一个处理器对象，用来处理cookie
        # 参数就是构建的CookieJar（）对象
        cookie_handler = request.HTTPCookieProcessor(cookie)

        # 构建一个自定义的opener
        opener = request.build_opener(cookie_handler)

        # 通过自定义opener的addheaders的参数，可以添加HTTP报头参数
        if not _header:
            opener.addhandlers = [("User-Agent", "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50")]
        else:
            opener.addhandlers = [(_key,_value) for _key,_value in _header.items()]
        # 需要登陆的账户密码
        # data = {"email": "xxxxxx", "password": "xxxxx"}
        # 通过URL encode（）编码转换
        # data = urllib.parse.urlencode(data).encode("utf-8")

        _request = request.Request(_url)  # , data=data

        response = opener.open(_request)

        html = response.read()
        buff = BytesIO(html)

        f = gzip.GzipFile(fileobj=buff)

        res = f.read().decode('utf-8')

        soup = BeautifulSoup(res, 'lxml')
        return soup.find("body")


    # 转换html编码格式，防止乱码
    @staticmethod
    def get_code(_url,
                 headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}):
        page = requests.get(_url)
        encoder = "utf-8"
        try:
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}
            req = request.Request(url=_url, headers=headers)
            html = request.urlopen(req).read()
            # html = urllib.request.urlopen(url).read()
            # print(html.decode('utf-8'))
            encoder = chardet.detect(html)['encoding']
        except Exception as e:
            print("ERROR : {}".format(e))

        if encoder == 'utf-8' or encoder == 'UTF-8' or 'utf-8' in encoder or 'UTF-8' in encoder:
            pass
        elif encoder == 'GBK' or encoder == 'gbk':
            page.encoding = 'GBK'
        elif encoder == 'GB2312' or encoder == 'gb2312':
            page.encoding = 'GB2312'
        else:
            print('请手动查看', page.encoding)
        # return
        return html.decode(encoder)


    # 获取指定url信息
    @staticmethod
    def get_html(url, headers=None):
        if headers != None:
            html = Reuqest_Class.get_code(url, headers)
        else:
            html = Reuqest_Class.get_code(url, headers)
        soup = BeautifulSoup(html, 'lxml')
        return soup.find("body")


    # 获取https的网页信息
    @staticmethod
    def get_https(url,_headers=None):
        context = ssl._create_unverified_context()

        if _headers:
            req = request.Request(url=url, headers=_headers)
            res = request.urlopen(req, context=context)
        else:

            res = request.urlopen(url, context=context)
        html = res.read()
        html = html.decode("utf-8")
        soup = BeautifulSoup(html, 'lxml')
        return soup.find("body")


    # 获取指定元素
    @staticmethod
    def find_element(find_obj, ele_name):
        return find_obj.find_all(ele_name)


    # 获取指定元素中的指定子元素
    @staticmethod
    def get_element(find_obj, ele_name):
        return find_obj.select(ele_name)


    @staticmethod
    def change_ducode(msg):
        return parse.quote(msg)
        # return urllib.request.quote(msg)


# 字符串处理类
class Str_Class(object):

    # 提取有用字符
    @staticmethod
    def get_msg(_str):
        return (re.sub(r"[\u4e00-\u9fa5A-Za-z0-9()]", "", _str))


    # 提取标题
    @staticmethod
    def get_title(_str):
        return (re.sub(r"[^\u4e00-\u9fa5A-Za-z0-9()《》]", "", _str))


    @staticmethod
    # 只提取汉子
    def get_word(_str):
        return (re.sub(r"[^\u4e00-\u9fa5]", "", _str))


    # 删除字符串中的占位符
    @staticmethod
    def get_str(_str):
        return (re.sub(r"[\r\t\n]", "", _str))


    # 拆分字符串中有名字与编码
    @staticmethod
    def name_code(_str):
        try:
            _code = re.findall(r"[(（](.*?)[)）]", _str)[0]
            _name = re.sub(r"[(（](.*?)[)）]", "", _str)

        except:
            return None
        return {"code": _code, "name": _name}

    # 编辑距离计算文本差距
    # @staticmethod
    # def diff(_strA, _strB):
    #     _len = len(_strA)
    #     _dis = Levenshtein.distance(_strA, _strB)
    #     return _dis, (_dis / _len)


# 下载文件
class Down_File(object):
    # 下载文件
    @staticmethod
    def downloadfiles(url, filename):
        f = requests.get(url)
        with open(filename, "wb") as code:
            code.write(f.content)


    # 下载图片
    @staticmethod
    def download_picture(img_url, save_path):
        img = requests.get(img_url)
        f = open(save_path, 'ab')  # 存储图片，多媒体文件需要参数b（二进制文件）
        f.write(img.content)  # 多媒体存储content
        f.close()


    # 保存图片到本地
    @staticmethod
    def get_image(url, save_path):
        response = requests.get(url)
        with open(save_path, "wb") as fp:
            for data in response.iter_content(128):
                fp.write(data)


# 爬网公共方法类
class Base_Class(object):

    def __init__(self, _start_url, _parent_url, _start_element, _sub_element, _folder_name, _sub_item="p",
                 use_special=True):
        # 子页面url拼接时使用前缀
        self.parent_url = _parent_url
        # 开始主页面url
        self.start_url = _start_url
        # 主页面获取元素位置
        self.start_element_list = _start_element
        # 子页面获取元素位置
        self.sub_element = _sub_element
        # 文件夹位置
        _folder = settings.READ_FILE + _folder_name
        if not os.path.exists(_folder):
            os.makedirs(_folder)
        self.folder = _folder + "/"

        self.sub_find_item = _sub_item
        # 使用特殊图片url处理方法
        self.img_url = use_special


    def special_img_url(self, page_url):
        return page_url[:page_url.rindex("/")]


    # 针对href信息中的url为相对路径，使用当前页面url与相对路径拼接真是url
    def config_item_url(self, html_url, item_url):
        url_list = html_url.split("/")[:-1]
        item_url_list = len(re.findall(r"\.\./", item_url))
        if item_url_list:
            use_list = url_list[:-item_url_list]
        else:
            use_list = url_list
        return "/".join(use_list) + "/" + re.sub(r"\.\./", "", item_url)


    def Get_Msg(self, sub_url_type=True, html_type=0):
        # 两种网络获取信息方式
        if html_type == 0:
            get_base_html = Reuqest_Class.get_html(self.start_url)
        else:
            get_base_html = Reuqest_Class.have_cookie(self.start_url)

        # print(get_base_html)
        # 有可能有多个标签需要获取，遍历list
        for start_element in self.start_element_list:
            get_div = Reuqest_Class.get_element(get_base_html, start_element)
            # print(get_div)
            # 当标题含有"2019"时停止获取之后的信息
            break_flag = True
            # 遍历获取的元素内容
            for use_div in get_div:
                items = Reuqest_Class.find_element(use_div, "a")
                # print(items)
                if len(items) > 0 and break_flag:
                    for _a in items:
                        get_href = _a.get("href")
                        if _a.get("title"):
                            use_text = _a.get("title")
                        else:
                            use_text = Str_Class.get_title(_a.text)
                        if get_href and get_href.endswith(".pdf"):
                            # 当连接以"pdf"结尾时进行如下操作
                            use_url = self.config_item_url(self.start_url, get_href)
                            print(use_url)
                            _pic_path = self.folder + use_text + ".pdf"
                            Down_File.get_image(use_url, _pic_path)
                        else:
                            # if get_href and (get_href.endswith(".htm") or get_href.endswith(".html")):
                            # 当链接以"htm"或者"html"结尾时进行如下操作
                            if use_text.startswith("转发："):
                                continue
                            print(use_text)
                            if "2019" in use_text:
                                break_flag = False
                                break
                            else:
                                # 本地文本保存路径
                                _filr_path = self.folder + use_text + ".txt"
                                # 子页面url
                                if sub_url_type:
                                    get_href = self.config_item_url(self.start_url, get_href)
                                else:
                                    get_href = self.parent_url + get_href
                                # 图片保存路径
                                _pic_path = self.folder + use_text + "{}.png"

                                _pic_folder = self.parent_url
                                print(get_href)

                                if html_type == 0:
                                    get_sub_html = Reuqest_Class.get_html(get_href)
                                else:
                                    get_sub_html = Reuqest_Class.have_cookie(get_href)

                                # print(get_sub_html)
                                try:
                                    get_div = Reuqest_Class.get_element(get_sub_html, self.sub_element)[0]
                                    with open(_filr_path, "w") as f:
                                        # 一个页面多图片时，防止命名相同
                                        _pic_index = 0
                                        for _p in Reuqest_Class.find_element(get_div, self.sub_find_item):
                                            # print(_p.text)
                                            f.write(_p.text)
                                            f.write("\n")
                                            get_imgs = Reuqest_Class.find_element(_p, "img")
                                            for get_img in get_imgs:
                                                print(get_img.get("src"))
                                                img_path = self.config_item_url(get_sub_html,
                                                                                Reuqest_Class.change_ducode(
                                                                                    get_img.get("src")))

                                                print(img_path)
                                                use_pic_path = _pic_path.format(_pic_index)
                                                _pic_index += 1
                                                print(img_path, use_pic_path)
                                                Down_File.get_image(img_path, use_pic_path)

                                            # if _p.text:
                                            #     print(_p.text)
                                            #     f.write(_p.text)
                                            #     f.write("\n")
                                            # else:
                                            #     get_imgs = Reuqest_Class.find_element(_p, "img")
                                            #     if get_imgs:
                                            #         for get_img in get_imgs:
                                            #             img_path = _pic_folder + Reuqest_Class.change_ducode(
                                            #                 get_img.get("src").replace("../", "/"))
                                            #             use_pic_path = _pic_path.format(_pic_index)
                                            #             _pic_index += 1
                                            #             print(img_path, use_pic_path)
                                            #             Down_File.get_image(img_path, use_pic_path)
                                            #     else:
                                            #         continue
                                except:
                                    continue


# #从csv读取内容
# def readfile(path):
# 	with open(path,'r',encoding='utf-8') as csvfile:
# 		read = csv.reader(csvfile)
# 		i=0
# 		for one in read:
# 			downloadfiles(one[0],i)
# 			i = i+1
# 			print(one[0])
# readfile("d:\\baoxian_pdf.csv")
# 测试各公共方法类
class Test_Class(object):
    @staticmethod
    def test_Base_Class():
        _start_url = "http://www.xjzkzx.com/index.html"
        _parent_url = "https://www.zjzs.net/moban/index/"
        _start_element = ["#content>ul>li"]
        _sub_element = "#content"
        # newsbody_class
        _folder_name = "XinJiang"

        use_obj = Base_Class(_start_url, _parent_url, _start_element, _sub_element, _folder_name, "p", False)
        use_obj.Get_Msg(False)
        # _start_url = "http://www.sdzk.cn/NewsList.aspx?BCID=5"
        # _parent_url = "http://www.sdzk.cn/"
        # _start_element = ["#ctl00_ContentPlaceHolder1_RadAjaxPanel1>ul"]
        # _sub_element = "div.txt"
        # _folder_name = "ShanDong"
        # use_obj = Base_Class(_start_url, _parent_url, _start_element, _sub_element, _folder_name, "p", False)
        # use_obj.Get_Msg(False)


if __name__ == "__main__":
    msg = "尚德机构怎么样！想去考个本科证！有人在那学过吗？"
    aa = "https://www.zhihu.com/search?type=content&q=%E5%B0%9A%E5%BE%B7%E6%9C%BA%E6%9E%84"
    url = Reuqest_Class.change_ducode(msg)
    print(url)
    # html = Reuqest_Class.get_code(aa)
    # soup = BeautifulSoup(html, 'lxml')
    # print(soup.text)
    # print(Reuqest_Class.get_html("http://www.cqksy.cn/site/zk/zhukao/重庆师范大学.htm"))
