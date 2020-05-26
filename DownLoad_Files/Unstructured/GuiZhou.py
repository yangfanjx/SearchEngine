from SearchEngine.Code.Base_Function import Reuqest_Class, Down_File
from SearchEngine.Code.Base_Function import Base_Class
from SearchEngine.Code.File_Read_write import Read_excel
import re
from django.conf import settings


class Handel_msg(object):
    @staticmethod
    def handle_special(_msg):
        re_code = re.match("\d+[a-zA-Z]?", _msg)
        if re_code:
            _code = re_code.group()
            _name = _msg.replace(_code, "")[:-4]
            return (_code, _name)
        else:
            return None
        # print(_code.string )


class GuiZhou_Class(object):

    # 贵州教材
    @staticmethod
    def Get_Book():
        titles = ['序号', '课程代码', '课程名称', '分类', '学分', '教材']
        return_dict = {}

        _base_link = "http://www.eaagz.org.cn/zxks/ksjh/index.html"
        get_base_html = Reuqest_Class.get_html(_base_link)
        get_div = Reuqest_Class.get_element(get_base_html, "div.column-news-con")
        if get_div:
            use_div = get_div[0]
            a_list = Reuqest_Class.get_element(use_div, "div>div>ul>li>span.news_title>a")
            for _a in a_list:
                if _a.get("title") == "自学考试各专业计划及教材信息":
                    use_url = _a.get("href")

                    base_url = "/".join(use_url.split("/")[:-1])
                    print(base_url)
                    sub_html = Reuqest_Class.get_html(use_url)
                    file_link = Reuqest_Class.get_element(sub_html, "p.insertfileTag > a")
                    if file_link:
                        use_link = file_link[0]
                        _title = use_link.get("title")
                        _link = base_url + "/" + use_link.get("href").split("/")[-1]
                        Down_File.downloadfiles(_link, settings.READ_FILE + _title)

                        # 开始读取Excel信息
                        read_msg = Read_excel(settings.READ_FILE + _title)
                        _special_dict = {}
                        add_list = []
                        for _row in range(read_msg.nrows - 1):
                            current_len = [i for i in read_msg.get_row(_row) if i]
                            if len(current_len) == 1:
                                _special = Handel_msg.handle_special(current_len[0])
                                if _special:
                                    _code, _name = _special
                                    _special_dict['专业代码'] = _code
                                    _special_dict['专业名称'] = _name
                                    # return_dict[_code] = return_dict.get(_code, [])
                                    # print(_code, _name)
                            elif len(current_len) == 6 and current_len == titles:
                                continue
                            elif len(current_len) == 0:
                                continue
                            else:
                                for i in range(1, len(titles) - 1):
                                    _special_dict[titles[i]] = current_len[i]
                                add_list.append(_special_dict)

                            return_dict[_code] = add_list

                            # print([i for i in read_msg.get_row(_row) if i])
                        print(return_dict)

                    # print(_link)
                    # print(_a)
        # if get_div:
        #     use_div = get_div[0]
        #     # body > div.zk - main > div.container > div > div > div: nth - child(3) > ul > li > a
        #     items = Reuqest_Class.get_element(use_div, "ul > li > a")
        #     if items:
        #         for item in items:
        #             # 拼接每个院校的url与名称
        #
        #             if "2020年" in item.get("title") and "教材版本目录" in item.get("title"):
        #                 usb_link = _base_link + str(item.get("href"))
        #
        #                 # 使用url获取网页信息
        #                 sub_html = Reuqest_Class.get_https(usb_link)
        #                 # print(sub_html)
        #                 # 过滤html中的表结构
        #                 sub_select = "div.arthtml > div > div.content > table"
        #                 sub_items = Reuqest_Class.get_element(sub_html, sub_select)
        #
        #                 for sub_item in sub_items:
        #                     special_dict = {}
        #                     for _index, tr_msg in enumerate(sub_item.select("tr")):
        #                         if _index in (0, 1):
        #                             continue
        #
        #                         elif _index == 2:
        #                             for td_msg in tr_msg.select("td"):
        #                                 # 删除字符中的\r\n\t以后添加list
        #                                 titles.append(Str_Class.get_str(str(td_msg.text)))
        #
        #                         else:
        #                             current_td_list = tr_msg.select("td")
        #                             add_dict = {}
        #                             if len(current_td_list) == len(titles):
        #                                 for sub_index, td_msg in enumerate(current_td_list):
        #                                     if sub_index == 0:
        #                                         special_msg = Str_Class.get_str(td_msg.text)
        #                                         special_dict = Str_Class.name_code(special_msg)
        #                                         if special_dict:
        #                                             return_dict[special_dict["code"]] = []
        #                                         else:
        #                                             break
        #                                     else:
        #                                         add_dict[titles[sub_index]] = Str_Class.get_str(td_msg.text)
        #                                 if special_dict:
        #                                     # print(special_dict)
        #                                     # print(return_dict.get(special_dict["code"], []))
        #                                     add_list = return_dict.get(special_dict["code"], [])
        #                                     add_dict.update(special_dict)
        #                                     add_list.append(add_dict)
        #                                     return_dict[special_dict["code"]] = add_list
        #                                 else:
        #                                     continue
        #
        #
        #                             elif len(current_td_list) == len(titles) - 1:
        #                                 add_dict = {}
        #                                 for sub_index, td_msg in enumerate(current_td_list):
        #                                     add_dict[titles[sub_index + 1]] = Str_Class.get_str(td_msg.text)
        #
        #                                 add_list = return_dict.get(special_dict["code"], [])
        #                                 add_dict.update(special_dict)
        #                                 add_list.append(add_dict)
        #                                 return_dict[special_dict["code"]] = add_list
        #
        #
        #                             else:
        #                                 continue
        #
        #                 print(titles)
        #                 print(return_dict)


    # 非结构化网页数据爬取
    @staticmethod
    def GuiZhou():
        _start_url = "http://www.eaagz.org.cn/zxks/ksjh/index.html"
        _parent_url = ""
        _start_element = ["div.con>ul>li"]
        _sub_element = "div.article>div"
        _folder_name = "GuiZhou"

        use_obj = Base_Class(_start_url, _parent_url, _start_element, _sub_element, _folder_name)
        use_obj.Get_Msg()


if __name__ == "__main__":
    GuiZhou_Class.Get_Book()
