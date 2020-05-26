from SearchEngine.Code.Base_Function import Base_Class

# 浙江
def ZheJiang():
    _start_url = "https://www.zjzs.net/moban/index/2c9081f061d15b160161d1661f040016_list.html"
    _parent_url = "https://www.zjzs.net/moban/index/"
    _start_element = ["#content>ul>li"]
    _sub_element = "#content"
    # newsbody_class
    _folder_name = "ZheJiang"

    use_obj = Base_Class(_start_url, _parent_url, _start_element, _sub_element, _folder_name, "span", False)
    use_obj.Get_Msg(False)


ZheJiang()
