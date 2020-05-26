from SearchEngine.Code.Base_Function import Base_Class


def HeBei():
    _start_url = "https://www.nm.zsks.cn/zxks/ggl/"
    _parent_url = "https://www.nm.zsks.cn/zxks/ggl"
    _start_element = ["body >table:nth-child(4)>tbody>tr>td:nth-child(2)>table:nth-child(2)>tbody>tr>td:nth-child(2)>table:nth-child(2)>tbody>tr>td>table>tbody>tr>td"]
    _sub_element = "div.TRS_Editor"
    _folder_name = "NeiMengGu"

    use_obj = Base_Class(_start_url, _parent_url, _start_element, _sub_element, _folder_name)
    use_obj.Get_Msg()


HeBei()
