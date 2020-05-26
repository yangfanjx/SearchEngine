from SearchEngine.Code.Base_Function import Base_Class


def GuangXi():
    _start_url = "https://www.gxeea.cn/zxks/tzgg.htm"
    _parent_url = "https://www.gxeea.cn"
    _start_element = ["div.list-content>ul>li"]
    _sub_element = "div.info-box"
    _folder_name = "GuangXi"

    use_obj = Base_Class(_start_url, _parent_url, _start_element, _sub_element, _folder_name)
    use_obj.Get_Msg()


GuangXi()
