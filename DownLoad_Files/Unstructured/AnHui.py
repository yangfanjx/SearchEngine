from SearchEngine.Code.Base_Function import Reuqest_Class, Str_Class, file_path
from django.conf import settings

folder = file_path(settings.READ_FILE, "AnHui")


class AnHui_Class(object):
    def __init__(self):
        self._base_link = "https://www.ahzsks.cn/gdjyzxks/"


    # 安徽教材
    def Get_Book(self):
        titles = []
        return_dict = {}

        # parent_link = "https://www.ahzsks.cn/gdjyzxks/"
        get_base_html = Reuqest_Class.get_https(self._base_link)
        get_div = Reuqest_Class.get_element(get_base_html, "body>div.zk-main>div.container>div>div>div:nth-child(3)")
        if get_div:
            use_div = get_div[0]
            # body > div.zk - main > div.container > div > div > div: nth - child(3) > ul > li > a
            items = Reuqest_Class.get_element(use_div, "ul > li > a")
            if items:
                for item in items:
                    # 拼接每个院校的url与名称

                    if "2020年" in item.get("title") and "教材版本目录" in item.get("title"):
                        usb_link = self._base_link + str(item.get("href"))

                        # 使用url获取网页信息
                        sub_html = Reuqest_Class.get_https(usb_link)
                        # print(sub_html)
                        # 过滤html中的表结构
                        sub_select = "div.arthtml > div > div.content > table"
                        sub_items = Reuqest_Class.get_element(sub_html, sub_select)

                        for sub_item in sub_items:
                            special_dict = {}
                            for _index, tr_msg in enumerate(sub_item.select("tr")):
                                if _index in (0, 1):
                                    continue

                                elif _index == 2:
                                    for td_msg in tr_msg.select("td"):
                                        # 删除字符中的\r\n\t以后添加list
                                        titles.append(Str_Class.get_str(str(td_msg.text)))

                                else:
                                    current_td_list = tr_msg.select("td")
                                    add_dict = {}
                                    if len(current_td_list) == len(titles):
                                        for sub_index, td_msg in enumerate(current_td_list):
                                            if sub_index == 0:
                                                special_msg = Str_Class.get_str(td_msg.text)
                                                special_dict = Str_Class.name_code(special_msg)
                                                if special_dict:
                                                    return_dict[special_dict["code"]] = []
                                                else:
                                                    break
                                            else:
                                                add_dict[titles[sub_index]] = Str_Class.get_str(td_msg.text)
                                        if special_dict:
                                            # print(special_dict)
                                            # print(return_dict.get(special_dict["code"], []))
                                            add_list = return_dict.get(special_dict["code"], [])
                                            add_dict.update(special_dict)
                                            add_list.append(add_dict)
                                            return_dict[special_dict["code"]] = add_list
                                        else:
                                            continue


                                    elif len(current_td_list) == len(titles) - 1:
                                        add_dict = {}
                                        for sub_index, td_msg in enumerate(current_td_list):
                                            add_dict[titles[sub_index + 1]] = Str_Class.get_str(td_msg.text)

                                        add_list = return_dict.get(special_dict["code"], [])
                                        add_dict.update(special_dict)
                                        add_list.append(add_dict)
                                        return_dict[special_dict["code"]] = add_list


                                    else:
                                        continue

                        print(titles)
                        print(return_dict)


    # 安徽网页信息
    def Get_Msg(self):
        get_base_html = Reuqest_Class.get_https(self._base_link)
        get_h3 = Reuqest_Class.get_element(get_base_html, "div.list-news")
        # body > div.zk - main > div.container > div > div > div: nth - child(1)
        for _h3 in get_h3:
            if Reuqest_Class.get_element(_h3, "h3>font")[0].text == "自考动态":
                use_list = Reuqest_Class.get_element(_h3, "ul>li>a")
                for i in use_list:
                    _url = self._base_link + i.get("href")
                    _file = folder + i.get("title") + ".txt"

                    sub_html = Reuqest_Class.get_https(_url)
                    get_content = Reuqest_Class.get_element(sub_html, "div.content")

                    with open(_file, "w") as f:
                        for i in get_content[0].text:
                            if i:
                                f.write(i)
            else:
                continue


if __name__ == "__main__":
    ah = AnHui_Class()
    # ah.Get_Book()
    ah.Get_Msg()
