from SearchEngine.Code.Base_Function import Base_Class


def Shan3Xi():
    _start_url = "http://124.114.203.117/ZK_NET/net/page_index.do"
    _parent_url = "http://124.114.203.117/ZK_NET/net/"
    _start_element = ["#con_five_1>div>dl>dt"]
    _sub_element = "#news_main"

    _folder_name = "Shan3Xi"

    use_obj = Base_Net.Base_Class(_start_url, _parent_url, _start_element, _sub_element, _folder_name)
    use_obj.Get_Msg(False)


Shan3Xi()
