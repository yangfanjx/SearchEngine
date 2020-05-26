from SearchEngine.Code.Base_Function import Base_Class


def HeBei():
    _start_url = "http://www.hebeea.edu.cn/html/zxks/list.html"
    _parent_url = "http://www.hebeea.edu.cn/"
    _start_element = ["body>div>ul>li"]
    _sub_element = "div.sub_main2>table.con_content"
    _folder_name = "HeBei"

    use_obj = Base_Class(_start_url, _parent_url, _start_element, _sub_element, _folder_name)
    use_obj.Get_Msg()


HeBei()
