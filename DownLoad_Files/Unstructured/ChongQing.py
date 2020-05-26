from SearchEngine.Code.Base_Function import Reuqest_Class, Down_File, file_path
import re
from django.conf import settings

folder = file_path(settings.READ_FILE, "ChongQing")

class ChongQing_Class(object):

    # 重庆院校
    @staticmethod
    def Get_School():
        titles = []
        return_dict = {}

        parent_link = "http://www.cqksy.cn/site/zk/zhukao/"
        _base_link = "http://www.cqksy.cn/site/zk/zhukao/zhuanye.htm"
        get_base_html = Reuqest_Class.get_html(_base_link)
        get_table = Reuqest_Class.get_element(get_base_html, "body>div>div>table>tr>td>div>table>tr>td>div>table>tr>td:nth-child(2)>div>table>tr:nth-child(2)>td:nth-child(2)>div:nth-child(5)>table")
        if get_table:
            use_table = get_table[0]
            items = Reuqest_Class.get_element(use_table, "p.MsoNormal>span>a")
            if items:
                for item in items:
                    # 拼接每个院校的url与名称
                    usb_link = parent_link + Reuqest_Class.change_ducode(str(item.get("href")))
                    sub_name = item.get("href").split(".")[0]
                    # print(sub_name,usb_link)

                    # 使用url获取网页信息
                    sub_html = Reuqest_Class.get_html(usb_link)
                    # print(sub_html)

                    # 过滤html中的表结构
                    sub_select = "body > div > div>table"
                    sub_items = Reuqest_Class.get_element(sub_html, sub_select)
                    # print(sub_items)

                    # 初始化字典当前学校的key与value信息
                    return_dict[sub_name] = return_dict.get(sub_name, [])
                    school_msg = return_dict[sub_name]
                    for sub_item in sub_items:
                        for _index, tr_msg in enumerate(sub_item.select("tr")):
                            if _index == 0 and not titles:
                                for td_msg in tr_msg.select("td"):
                                    titles.append(td_msg.text.replace(u"\n", ""))
                            elif _index == 0:
                                continue
                            else:
                                msg_list = {}
                                for sub_index, td_msg in enumerate(tr_msg.select("td")):
                                    msg_list[titles[sub_index]] = td_msg.text.replace(u"\n", "")

                                school_msg.append(msg_list)
                    return_dict[sub_name] = school_msg

                    print(titles)
                    print(return_dict)

    # 重庆教材
    @staticmethod
    def Get_Book():
        titles = []
        return_dict = {}

        _base_link = "http://www.cqksy.cn/site/zkList.jsp?ClassID=100&param=5"
        get_base_html = Reuqest_Class.get_html(_base_link)
        get_table = Reuqest_Class.get_element(get_base_html, "div.menu")
        # print(get_table)
        if get_table:
            use_table = get_table[0]
            items = Reuqest_Class.get_element(use_table, "div>ul>li>a")
            if items:
                for item in items:
                    if item.text == "教材信息":
                        sub_html = Reuqest_Class.get_html(item.get("href"))
                        sub_tables = Reuqest_Class.get_element(sub_html, "table.normaltable")
                        if sub_tables:
                            for sub_table in sub_tables:
                                for _index, tr_msg in enumerate(sub_table.select("tr")):
                                    if _index == 0 and not titles:
                                        for td_msg in tr_msg.select("td"):
                                            titles.append(td_msg.text.replace(u"\n", ""))
                                    elif _index == 0:
                                        continue
                                    else:
                                        msg_list = {}
                                        for sub_index, td_msg in enumerate(tr_msg.select("td")):
                                            msg_list[titles[sub_index]] = td_msg.text.replace(u"\n", "")
                                        return_dict[msg_list["课程代码"]] = msg_list

                        print(titles)
                        print(return_dict)

    # 重庆专业
    @staticmethod
    def Get_Special():
        titles = []
        return_dict = {}

        _base_link = "http://www.cqksy.cn/site/zkList.jsp?ClassID=100&param=5"
        get_base_html = Reuqest_Class.get_html(_base_link)
        get_table = Reuqest_Class.get_element(get_base_html, "div.menu")
        # print(get_table)
        if get_table:
            use_table = get_table[0]
            items = Reuqest_Class.get_element(use_table, "div>ul>li>a")
            if items:
                # print(items)
                for item in items:
                    if item.text == "专业情况":
                        parent_item = item.parent()
                        print(Reuqest_Class.find_element(parent_item,"a"))
                        sub_html = Reuqest_Class.get_html(item.get("href"))
                        sub_tables = Reuqest_Class.get_element(sub_html, "table.normaltable")
                        if sub_tables:
                            for sub_table in sub_tables:
                                for _index, tr_msg in enumerate(sub_table.select("tr")):
                                    if _index == 0 and not titles:
                                        for td_msg in tr_msg.select("td"):
                                            titles.append(td_msg.text.replace(u"\n", ""))
                                    elif _index == 0:
                                        continue
                                    else:
                                        msg_list = {}
                                        for sub_index, td_msg in enumerate(tr_msg.select("td")):
                                            msg_list[titles[sub_index]] = td_msg.text.replace(u"\n", "")
                                        return_dict[msg_list["课程代码"]] = msg_list

                        print(titles)
                        print(return_dict)

    # 重庆信息
    @staticmethod
    def Get_Msg():

        _base_url = "http://www.cqksy.cn/site/"
        _base_link = "http://www.cqksy.cn/site/zkList.jsp?ClassID=100"
        get_base_html = Reuqest_Class.get_html(_base_link)
        get_table = Reuqest_Class.get_element(get_base_html, "div.menu")

        for use_table in get_table:
            items = Reuqest_Class.get_element(use_table, "ul>li:nth-child(1)>ul>li")

            for item in items:
                for _a in Reuqest_Class.find_element(item, "a"):
                    get_href = _a.get("href")
                    if get_href and get_href.startswith("zk/bkzn/"):
                        print(get_href)
                        _filr_path = folder +  _a.text + ".txt"

                        _sub_link = _base_url + Reuqest_Class.change_ducode(get_href)

                        _pic_path = folder +_a.text + ".png"
                        _pic_folder = _base_url + Reuqest_Class.change_ducode(re.sub(r"/[\u4e00-\u9fa5]+(.htm)", "", get_href) + "/")

                        get_sub_html = Reuqest_Class.get_html(_sub_link)
                        get_div = Reuqest_Class.get_element(get_sub_html, "div.WordSection1")[0]

                        with open(_filr_path, "w") as f:

                            for _p in Reuqest_Class.find_element(get_div, "p"):

                                if _p.text:
                                    f.write(_p.text)
                                    f.write("\n")
                                else:
                                    get_img = Reuqest_Class.find_element(_p, "img")
                                    if get_img:
                                        get_img = get_img[0]
                                        img_path = _pic_folder + Reuqest_Class.change_ducode(get_img.get("src").replace("../",""))
                                        # print(img_path)
                                        Down_File.get_image(img_path, _pic_path)
                                    else:
                                        continue
                        # print(get_div)



if __name__ == "__main__":
    ChongQing_Class.Get_Msg()
    # ChongQing_Class.Get_Book()
    # ChongQing_Class.Get_School()
