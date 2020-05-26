from SearchEngine.Code.Base_Function import Base_Class


def SiChuan():
    _start_url = "https://www.sceea.cn/List/NewsList_33_1.html"
    _parent_url = "https://www.sceea.cn"

    _start_element = ["#list>li"]
    _sub_element = "div.news"
    _folder_name = "SiChuan"

    use_obj = Base_Class(_start_url, _parent_url, _start_element, _sub_element, _folder_name)
    use_obj.Get_Msg(False)


SiChuan()
