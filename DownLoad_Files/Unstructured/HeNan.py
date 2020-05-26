from SearchEngine.Code.Base_Function import Base_Class


def HeNan():
    _start_url = "http://www.heao.com.cn/main/html/InfoList.aspx?ExamId=4"
    _parent_url = "http://www.heao.com.cn"
    _start_element = ["div.list_con"]
    _sub_element = "div.show_con"
    _folder_name = "HeNan"

    use_obj = Base_Class(_start_url, _parent_url, _start_element, _sub_element, _folder_name)
    use_obj.Get_Msg()


if __name__ == "__main__":
    HeNan()
