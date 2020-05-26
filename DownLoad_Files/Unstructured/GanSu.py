from SearchEngine.Code.Base_Function import Base_Class


# 甘肃
def GanSu():
    _start_url = "http://www.ganseea.cn/html/zxks/"
    _parent_url = "http://www.ganseea.cn"
    _start_element = ["div.partR>div:nth-child(1)>ul>li", "div.partR>div:nth-child(2)>ul>li"]
    _sub_element = "div.detailcontent>div"
    _folder_name = "GanSu"

    use_obj = Base_Class(_start_url, _parent_url, _start_element, _sub_element, _folder_name)
    use_obj.Get_Msg()


if __name__ == "__main__":
    GanSu()
