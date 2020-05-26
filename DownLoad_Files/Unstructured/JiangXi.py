from SearchEngine.Code.Base_Function import Base_Class


# 江西
def JiangXi():
    _start_url = "http://www.jxeea.cn/index/zxks/ksap.htm"
    _parent_url = "http://www.jxeea.cn"
    _start_element = ["table.winstyle152488>tr"]
    _sub_element = "#NewsContent>div"
    _folder_name = "JiangXi"
    use_obj = Base_Class(_start_url, _parent_url, _start_element, _sub_element, _folder_name)
    use_obj.Get_Msg()

    _start_url = "http://www.jxeea.cn/index/zxks/ksdt.htm"
    use_obj = Base_Class(_start_url, _parent_url, _start_element, _sub_element, _folder_name)
    use_obj.Get_Msg()


if __name__ == "__main__":
    JiangXi()
