from SearchEngine.Code.Base_Function import Base_Class


def JiLin():
    _start_url = "http://www.jleea.com.cn/zxks/ywdt/"
    _parent_url = "http://www.jleea.com.cn/"
    _start_element = ["div.main >ul>table:nth-child(1)"]
    _sub_element = "#rightbox"
    _folder_name = "JiLin"
    # rightbox
    use_obj = Base_Class(_start_url, _parent_url, _start_element, _sub_element, _folder_name, "span")
    use_obj.Get_Msg()


if __name__ == "__main__":
    JiLin()
