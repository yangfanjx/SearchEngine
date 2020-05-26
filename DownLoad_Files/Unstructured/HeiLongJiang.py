from SearchEngine.Code.Base_Function import Base_Class


def HeilongJiang():
    _start_url = "http://www.lzk.hl.cn/zk/zkxx/"
    _parent_url = "http://www.lzk.hl.cn/zk/zkxx/"
    _start_element = [
        "body>table:nth-child(4)>tr>td>table>tr>td>table>tr>td>table>tr>td:nth-child(2)>table:nth-child(3)"]
    _sub_element = "body>table:nth-child(3)>tr>td>table>tr>td>table>tr>td>table:nth-child(3)>tr:nth-child(4)>td:nth-child(2)>div"
    _folder_name = "HeilongJiang"

    use_obj = Base_Class(_start_url, _parent_url, _start_element, _sub_element, _folder_name)
    use_obj.Get_Msg()


if __name__ == "__main__":
    HeilongJiang()
