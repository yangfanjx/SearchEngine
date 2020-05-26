from SearchEngine.Code.Base_Function import Base_Class

# 江苏
def JiangSu():
    _start_url = "http://www.jseea.cn/zkyw/zkyw_channel178_1.html"
    _parent_url = ""
    _start_element = ["#right-container>table>tr:nth-child(2)>td:nth-child(2)>table>tr:nth-child(2)>td>ul>li"]
    _sub_element = "#content_div"
    _folder_name = "JiangSu"

    use_obj = Base_Class(_start_url, _parent_url, _start_element, _sub_element, _folder_name)
    use_obj.Get_Msg()


if __name__ == "__main__":
    JiangSu()
