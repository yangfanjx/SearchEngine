from SearchEngine.Code.Base_Function import Base_Class


def HeBei():
    _start_url = "http://www.lnzsks.com/listinfo/zxks_1.html"
    _parent_url = "http://www.lnzsks.com"
    _start_element = ["body>div.main.clearfix>ul>li"]
    _sub_element = "body>div.main.clearfix>div.info>div.content"
    _folder_name = "LiaoNing"

    use_obj = Base_Class(_start_url, _parent_url, _start_element, _sub_element, _folder_name)
    use_obj.Get_Msg()


HeBei()
