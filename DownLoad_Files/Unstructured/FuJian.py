from SearchEngine.Code.Base_Function import Reuqest_Class, file_path
from django.conf import settings

folder = file_path(settings.READ_FILE, "FuJian")


class FuJian_Class(object):

    # 福建信息
    @staticmethod
    def Get_Msg():

        _base_url = "http://www.cqksy.cn/site/"
        _base_link = "http://www.eeafj.cn/zxks/"
        get_base_html = Reuqest_Class.get_html(_base_link)
        get_table = Reuqest_Class.get_element(get_base_html, "div.info_box")

        for use_table in get_table:
            items = Reuqest_Class.get_element(use_table, "div.info_box_cont>ul>li>a")
            for _a in items:
                # print(_a)
                get_href = _a.get("href")
                if get_href:
                    print(_a)
                    _filr_path = folder + _a.text + ".txt"

                    # _pic_path = folder +_a.text + ".png"
                    # _pic_folder = _base_url + Reuqest_Class.change_ducode(re.sub(r"/[\u4e00-\u9fa5]+(.htm)", "", get_href) + "/")

                    get_sub_html = Reuqest_Class.get_html(get_href)
                    get_div = Reuqest_Class.get_element(get_sub_html, "div.article")[0]

                    with open(_filr_path, "w") as f:

                        for _p in Reuqest_Class.find_element(get_div, "p"):

                            if _p.text:
                                f.write(_p.text)
                                f.write("\n")
                            else:
                                '''
                                get_img = Reuqest_Class.find_element(_p, "img")
                                if get_img:
                                    get_img = get_img[0]
                                    img_path = _pic_folder + Reuqest_Class.change_ducode(get_img.get("src").replace("../",""))
                                    # print(img_path)
                                    Down_File.get_image(img_path, _pic_path)
                                else:
                                    continue
                                '''
                                continue


if __name__ == "__main__":
    FuJian_Class.Get_Msg()
    # ChongQing_Class.Get_Book()
    # ChongQing_Class.Get_School()
#
