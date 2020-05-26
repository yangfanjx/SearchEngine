from SearchEngine.Code.Base_Function import Base_Class


def HeBei():
    _start_url = "http://www.qhjyks.com/zxks/tzgg2/index.htm"
    _parent_url = "http://www.qhjyks.com/zxks/tzgg2/"
    _start_element = ["body>article.subPage>div>div.pageArticle>div.article.cur02>ul>li"]
    _sub_element = "div.article"
    _folder_name = "QingHai"

    use_obj = Base_Class(_start_url, _parent_url, _start_element, _sub_element, _folder_name)
    use_obj.Get_Msg()


HeBei()
