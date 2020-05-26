from SearchEngine.Code.Base_Function import Reuqest_Class, file_path
from django.conf import settings

folder = settings.READ_FILE+ "BeiJing/"


class BeiJing_Class(object):

    # 北京消息
    @staticmethod
    def Get_Msg():
        _base_link = "https://www.bjeea.cn"
        _use_link = "https://www.bjeea.cn/html/selfstudy/"

        get_base_html = Reuqest_Class.get_html(_use_link)
        get_li = Reuqest_Class.get_element(get_base_html, "li.clearfix")
        try:
            for li_item in get_li:
                get_a = Reuqest_Class.get_element(li_item, "div:nth-child(2)>p>a")
                if get_a:
                    use_a = get_a[0]
                else:
                    continue
                print("url:{}\ntitle:{}".format(_base_link + use_a.get("href"), use_a.get("title")))
                save_title = use_a.get("title")
                sub_link = _base_link + use_a.get("href")

                # 子页面获取
                get_sub_html = Reuqest_Class.get_html(sub_link)
                get_sub_div = Reuqest_Class.get_element(get_sub_html, "div.sidNavText")
                if get_sub_div:
                    get_sub_div = get_sub_div[0]
                else:
                    continue


                print(folder)

                _path = folder+ save_title + ".txt"
                print(_path)
                with open(_path, encoding="utf-8", mode="w") as f:
                    for i in get_sub_div.text:
                        if i:
                            f.write(i)
                    # f.write(get_sub_div)  # 这句话自带文件关闭功能，不需要再写f.close()
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    BeiJing_Class.Get_Msg()
