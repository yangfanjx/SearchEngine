from SearchEngine.Code.Base_Function import Base_Class

# 上海
def ShangHai():
    _start_url = "http://www.shzkw.org/"
    _parent_url = ""
    _start_element = ["div.news-list>ul>li"]
    _sub_element = "#Article > div.content.table"

    _folder_name = "ShangHai"
    use_obj = Base_Class(_start_url, _parent_url, _start_element, _sub_element, _folder_name, "p", False)
    use_obj.Get_Msg(False, 1)


ShangHai()
