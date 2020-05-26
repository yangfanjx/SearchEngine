from SearchEngine.Code.Base_Function import Base_Class


def SiChuan():
    _start_url = "http://www.sxkszx.cn/news/zxks/index.html"
    _parent_url = "http://www.sxkszx.cn"
    _start_element = ["#main_class>#table1>tr:nth-child(2)>td>table"]
    _sub_element = "#newsbody_class"
    # newsbody_class
    _folder_name = "ShanXi"

    use_obj = Base_Class(_start_url, _parent_url, _start_element, _sub_element, _folder_name, "span", False)
    use_obj.Get_Msg(False)


SiChuan()
