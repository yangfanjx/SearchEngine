import requests
import json
# from SearchEngine.Code.Base_Function import Reuqest_Class
import re
# from SearchEngine.Code.File_Read_write import Read_excel
import time
from bs4 import BeautifulSoup
from urllib import parse
import xlrd

'''
# 因反爬虫修改不再使用
class ZhiHu_Class_old(object):

    def __init__(self):

        # 知乎有反爬虫，加入http headers伪装浏览器
        # self.headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        #     "Connection": "keep-alive",
        #     "Accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        #     "Accept-Language": "zh-CN,zh;q=0.8"}

        # self.headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        #                 "accept":"* / *",
        #                 "accept-encoding":"gzip, deflate, br",
        #                 "accept-language":"zh-CN,zh;q=0.9",
        #                 "cookie":'_zap=e24e66c1-dd48-41c2-badc-fd4c0db75987; _xsrf=8bfd0a59-c671-48fe-b761-f996d80b6b77; d_c0="AIAXv0deARGPTndHOeUaUNJyv814qc0zTX0=|1584929600"; _ga=GA1.2.292069052.1584929602; _gid=GA1.2.550227809.1586053905; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1585643566,1585809823,1586053905,1586054155; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1586054189; KLBRSID=4843ceb2c0de43091e0ff7c22eadca8c|1586054189|1586053348; capsion_ticket="2|1:0|10:1586054189|14:capsion_ticket|44:OWJhODgzYTg0MWM5NGRjODkxYmI3ZmQzNTMyMWExMGY=|3868f85f732e81429a1103a53e7274c6a899121135d66cbd37b4b16aecc90a4f"'
        # }
        # self.cookies = {
        #     "d_c0": "AECA7v-aPwqPTiIbemmIQ8abhJy7bdD2VgE=|1468847182",
        #     "login": "NzM5ZDc2M2JkYzYwNDZlOGJlYWQ1YmI4OTg5NDhmMTY=|1480901173|9c296f424b32f241d1471203244eaf30729420f0",
        #     "n_c": "1",
        #     "q_c1": "395b12e529e541cbb400e9718395e346|1479808003000|1468847182000",
        #     "l_cap_id": "NzI0MTQwZGY2NjQyNDQ1NThmYTY0MjJhYmU2NmExMGY=|1480901160|2e7a7faee3b3e8d0afb550e8e7b38d86c15a31bc",
        #     "d_c0": "AECA7v-aPwqPTiIbemmIQ8abhJy7bdD2VgE=|1468847182",
        #     "cap_id": "N2U1NmQwODQ1NjFiNGI2Yzg2YTE2NzJkOTU5N2E0NjI=|1480901160|fd59e2ed79faacc2be1010687d27dd559ec1552a"
        # }2

        self.headers = {'accept': '*/*', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'zh-CN,zh;q=0.9',
                        'cookie': '_zap=e24e66c1-dd48-41c2-badc-fd4c0db75987; _xsrf=8bfd0a59-c671-48fe-b761-f996d80b6b77; d_c0="AIAXv0deARGPTndHOeUaUNJyv814qc0zTX0=|1584929600"; _ga=GA1.2.292069052.1584929602; _gid=GA1.2.402994359.1586940627; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1586850720,1586940625,1586940892,1586941029; capsion_ticket="2|1:0|10:1586941034|14:capsion_ticket|44:NjI0NWM5MDE0ZjgxNGUwZGIxNmI0YjNmZGVhYmNkYjc=|fc5be15b719d5705e7cbbc2a93b7dee27c592d24508928027b8c2422bcea3c81"; SESSIONID=35GjqfOVrrWaKE478PvKzEZmTJo1yDTyuNSeilGmyOE; JOID=UFoWAU-NWKQfALsXLI0e9-pM7A48vmzic3fdWXv5KvJ_TfgjGueUNUEGuhcrXBmDafWyehnOGxJH30UnPjpsWhI=; osd=U1AcCk-OUq4UALgdJoYe9OBG5w4_tGbpc3TXU3D5Kfh1RvggEO2fNUIMsBwrXxOJYvWxcBPFGxFN1U4nPTBmURI=; z_c0="2|1:0|10:1586941054|4:z_c0|92:Mi4xTHhBT0dRQUFBQUFBZ0JlX1IxNEJFU1lBQUFCZ0FsVk5maHFFWHdCVnlvZTJrOUREbHItSVVZdTJBM3R4cERRcGNn|ac3a87773effded98a44417e472b1f8c89775b39eae1e3e33737ff2e01dfc02c"; unlock_ticket="AFAcaiWbyxAmAAAAYAJVTYbTll4Ih_89jA0zns5nlnRkHDFskmjQlQ=="; tst=r; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1586941073; KLBRSID=81978cf28cf03c58e07f705c156aa833|1586941073|1586940622',
                        'referer': 'https://www.zhihu.com/search?type=content&q=%E5%B0%9A%E5%BE%B7',
                        'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin',
                        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                        'x-api-version': '3.0.91', 'x-app-za': 'OS=Web', 'x-requested-with': 'fetch',
                        'x-zse-83': '3_2.0', 'x-zse-86': '1.0_aXx0QAHqo_Sxr0NqyCFB6er0cMtfUuY8YLO8HUU0oLFX',
                        'x-zst-81': '3_2.0ae3TnRUTEvOOUCNMTQnTSHUZo02p-HNMZBO8YDQ0SXtuo7YyB6P0Eiuy-LS9-hp1DufI-we8gGHPgJO1xuPZ0GxCTJHR7820XM20cLRGDJXfgGCBxupMuD_I24cpr4w0mRPO7HoY70SfquPmz93mhDQyiqV9ebO1hwOYiiR0ELYuUrxmtDomqU7ynXtOnAoTh_PhRDSTFAexj9tG6hOMZcuB09S_89OmM4LBSXxmzbXsACC9qJN_2RSftG2LNgS07USTv0NLCcx1LugmKLC0yrxKpBHKPqxKvBVOICxK8hVVPqVYFCgYNUrYwGOYShC0PBSfc6S0CUgs20xMTGXGsbrGcMX1zgYB2vNfHcXYuCgprCcYpAS_FJO0Cqkw67oCBrx9_JCLQ02mPUN9jbNLgcC1_wNmrUxOpgw1crOYwvXsgCS9PCwLLC39_JHxkUcCzUgmNuHKVBouqwcq3rOBb6oGhresWhx9zwgqVDofwwLsWrOC'}

        # self.headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        #     "Connection": "keep-alive",
        #     "Accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        #     "Accept-Language": "zh-CN,zh;q=0.8"}

        # 关键词搜索URL

        self.key_word = "https://www.zhihu.com/api/v4/search_v3?t=general&q={}&correction=1&offset=0&limit={}&lc_idx=0&show_all_topics=0&search_hash_id=2a17c1150416d5c224299652c376d322&vertical_info=0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1"
        # 获取问题答案URL
        self.answers = "https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit={}&offset=0&platform=desktop&sort_by=default"
        # 获取关键词url
        self.get_key = "https://www.zhihu.com/question/{}/answer/{}"

        # 检验专栏URL匹配正则
        self.article_re = "zhuanlan.zhihu.com/p/\d+"
        # 检验问题答案URL匹配正则
        self.answer_re = 'zhihu.com/question/\d+/answer/\d+'
        # 检验问题不带答案URL正则
        self.question_re = 'zhihu.com/question/\d+'

        self.all_ids = []
        # 答案信息
        self.answer_dict = {}
        self.key_search_dict = {}

        self.all_answers = []


    # 检查url是否匹配
    def check_url(self, _url, type):
        if type == "answer":
            if re.match(self.answer_re, _url):
                return True
            else:
                return False
        elif type == "article":
            if re.match(self.article_re, _url):
                return True
            else:
                return False


    # 使用关键词搜索结果
    def keyword_search(self, _key_word, search_count=20):
        # 讲中文转换为encode
        url = Reuqest_Class.change_ducode(_key_word)
        use_url = self.key_word.format(url, search_count)
        print(use_url)
        # self.headers["referer"] = 'https://www.zhihu.com/search?type=content&q='+url
        print(self.headers["referer"])
        # 获取请求数据
        # print(Reuqest_Class.have_cookie(use_url))
        html = requests.get(use_url, headers=self.headers).text
        # html = requests.get(use_url, cookies=self.cookies, headers=self.headers).text
        # 架构化返回json信息
        _data = json.loads(html)["data"]

        num = 1

        for i in _data:
            msg_dict = {"get_url": "", "get_type": ""}
            try:
                if i["type"] == "search_result":
                    msg_dict["get_type"] = i["object"]["type"]
                    msg_dict["key_word"] = _key_word
                    if msg_dict["get_type"] == "answer":
                        # 当前问题在关键词排序中的位置
                        msg_dict["index"] = num
                        # 获取点赞数信息
                        msg_dict["voteup_count"] = i["object"]["voteup_count"]
                        # 获取评论数信息
                        msg_dict["comment_count"] = i["object"]["comment_count"]
                        # 获取作者信息
                        msg_dict["author_name"] = i["object"]["author"]["name"]

                        get_url = i["object"]["question"]["url"]
                        # 将api形式的url转为可以浏览信息的url形式
                        msg_dict["get_url"] = get_url.replace("api.zhihu", "zhihu").replace("questions", "question")
                        # 问题id
                        msg_dict["question_id"] = i["object"]["question"]["id"]

                        self.key_search_dict[msg_dict["question_id"]] = msg_dict

                        print("搜索问题（{}）答案".format(msg_dict["get_url"]))

                        answer_url = self.answers.format(msg_dict["question_id"], 5)

                        # 根据关键词结果中问题类进行答案的获取
                        answer_html = requests.get(answer_url, headers=self.headers).text
                        # 架构化返回json信息
                        answer_data = json.loads(answer_html)["data"]

                        for _index, _item in enumerate(answer_data):
                            use_dict = {}
                            use_dict["index"] = _index
                            use_dict["answer_id"] = _item["id"]
                            use_dict["question_id"] = _item["question"]["id"]
                            use_dict["author_name"] = _item["author"]["name"]
                            use_dict["voteup_count"] = _item["voteup_count"]
                            # 获取评论数信息
                            use_dict["comment_count"] = _item["comment_count"]
                            use_dict["url"] = self.get_key.format(use_dict["question_id"], use_dict["answer_id"])

                            self.answer_dict[use_dict["answer_id"]] = use_dict
                            self.all_ids.append(use_dict["answer_id"])

                            self.all_answers.append(_item["id"])
                        num += 1

                    elif msg_dict["get_type"] == "article":
                        # 当前问题在关键词排序中的位置
                        msg_dict["index"] = num
                        # 获取点赞数信息
                        msg_dict["voteup_count"] = i["object"]["voteup_count"]
                        # 获取评论数信息
                        msg_dict["comment_count"] = i["object"]["comment_count"]
                        # 获取作者信息
                        msg_dict["author_name"] = i["object"]["author"]["name"]
                        # id
                        msg_dict["id"] = i["object"]["id"]
                        get_url = i["object"]["url"]
                        # 将api形式的url转为可以浏览信息的url形式
                        msg_dict["get_url"] = get_url.replace("api.zhihu", "zhuanlan.zhihu").replace("articles", "p")

                        print("搜索文章（{}）".format(msg_dict["get_url"]))

                        self.key_search_dict[msg_dict["id"]] = msg_dict

                        self.all_ids.append(msg_dict["id"])
                        num += 1
                    else:
                        continue
                else:
                    continue
            except:
                print("ERROR")
                break


    def print_all(self):
        return self.all_ids


# 因反爬虫修改不再使用
class ZhiHu_Class_4_16(object):

    def __init__(self):

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Connection": "keep-alive",
            "Accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8"}

        # 关键词搜索URL
        self.key_word = "https://www.zhihu.com/search?type=content&q={}"
        # 检验专栏URL匹配正则
        self.article_re = "zhuanlan.zhihu.com/p/\d+"
        # 检验问题答案URL匹配正则
        self.answer_re = 'zhihu.com/question/\d+/answer/\d+'
        # 检验问题不带答案URL正则
        self.question_re = 'zhihu.com/question/\d+'

        self.all_ids = []

        # 所有问题数据
        self.question_dict = {}
        # 所有文章数据
        self.artical_list = []


    # 检查url是否匹配
    def check_url(self, _url, type):
        if type == "answer":
            if re.match(self.answer_re, _url):
                return True
            else:
                return False
        elif type == "article":
            if re.match(self.article_re, _url):
                return True
            else:
                return False


    def get_html_msg(self, _url):
        # 获取html返回信息
        html = requests.get(_url, headers=self.headers).text
        time.sleep(1)
        soup = BeautifulSoup(html, 'html.parser')
        _body = soup.find("body")
        print(_body)
        # 获取指定位置元素信息
        get_obj = Reuqest_Class.get_element(_body, "script")[3]
        get_msg = str(get_obj.string)
        return json.loads(get_msg)["initialState"]["entities"]


    # 使用关键词搜索结果
    def keyword_search(self, _key_word):
        # 讲中文转换为encode
        url = Reuqest_Class.change_ducode(_key_word)
        use_url = self.key_word.format(url)
        print(use_url)

        # 临时所有answer ID信息
        answer_list = []
        get_dict = self.get_html_msg(use_url)
        get_ele = get_dict["searchAdvancedGeneral"]
        for _key in get_ele.keys():
            # 答案数据
            if "search_search_result_answer" in _key:
                answer_list.append(_key.split("_")[-1:])
            # 文章数据
            elif "search_search_result_article" in _key:
                self.artical_list.append(_key.split("_")[-1:])
            else:
                continue

        answer_dict = {}
        # 根据答案获取问题数据，并获取问题top5答案
        for i in answer_list:
            get_question_dict = get_dict["answers"][str(i[0])]["question"]
            question_url = "https://www.zhihu.com/question/{}".format(get_question_dict["id"])
            answer_list = self.question_dict.get(get_question_dict["id"], [])

            print("获取问题：{}答案信息".format(question_url))
            get_question_html = self.get_html_msg(question_url)
            # print(get_question_html)
            for _index, i in enumerate(get_question_html["answers"]):
                use_dict = get_question_html["answers"][i]
                answer_msg_dict = {"name": use_dict["author"]["name"], "index": _index + 1,
                                   "questionid": use_dict["question"]["id"],
                                   "voteupCount": use_dict["voteupCount"], "commentCount": use_dict["commentCount"]}
                answer_list.append(i)
                self.all_ids.append(i)
                answer_dict[i] = answer_msg_dict

            self.question_dict[get_question_dict["id"]] = answer_list
        print(answer_dict)
        print(self.question_dict)


    def print_all(self):
        return self.all_ids, self.artical_list
'''


class Read_excel(object):
    def __init__(self, file_path):
        # 打开文件
        data = xlrd.open_workbook(file_path)

        # 查看工作表
        # data.sheet_names()
        # print("sheets：" + str(data.sheet_names()))
        #
        # # 通过文件名获得工作表,获取工作表1
        # table = data.sheet_by_name('工作表1')

        # 打印data.sheet_names()可发现，返回的值为一个列表，通过对列表索引操作获得工作表1
        self.table = data.sheet_by_index(0)

        # 获取行数和列数
        # 行数：table.nrows
        # 列数：table.ncols
        # print("总行数：" + str(table.nrows))
        # print("总列数：" + str(table.ncols))
        self.nrows = self.table.nrows
        self.ncols = self.table.ncols

        # 获取整行的值 和整列的值，返回的结果为数组
        # 整行值：table.row_values(start,end)
        # 整列值：table.col_values(start,end)
        # 参数 start 为从第几个开始打印，
        # end为打印到那个位置结束，默认为none
        # print("整行值：" + str(table.row_values(0)))
        # print("整列值：" + str(table.col_values(1)))


    def get_msg(self, row_num, clo_num):
        # 获取某个单元格的值，例如获取B3单元格值
        return self.table.cell(row_num, clo_num).value


    def get_row(self, row_num):
        return self.table.row_values(row_num)


class Reuqest_Class(object):

    # 获取指定元素中的指定子元素
    @staticmethod
    def get_element(find_obj, ele_name):
        return find_obj.select(ele_name)


    @staticmethod
    def change_ducode(msg):
        return parse.quote(msg)
        # return urllib.request.quote(msg)

# 现在使用
class ZhiHu_Class(object):

    def __init__(self):

        self.headers_sdjg = {'accept': '*/*', 'accept-language': 'zh-CN,zh;q=0.9',
                             'cookie': '_zap=c1ab8bbd-ffc7-4c49-892d-a7823194c57e; d_c0="ACATUdNWIBGPTtzG3d4wxjLmqHlAAYZVO3E=|1587008020"; _ga=GA1.2.401375569.1587008023; _gid=GA1.2.141163472.1587008023; _xsrf=f39c021b-fdfe-4865-9768-db10af88d5aa; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1587008190,1587008275,1587008675,1587020380; l_n_c=1; l_cap_id="NDBhNGY3M2U3OTgxNDlmMDk2NDExOTU3ZDgyN2Y4YjE=|1587040369|12b0d9031184f57dfebd953dccecd60e5e4f58db"; r_cap_id="NDkxZGVhZDU2YTJhNGY2OThlMjkzMjZmYjYzNTZkNWQ=|1587040369|4d56e2de90ddf5888a01ab74fe3e749cb4610256"; cap_id="NDU4YTBhZTc3Yzk0NDNmOTk0YmFkN2RhZWZlNzI5NWI=|1587040369|c5de995a9de07a91998c6c69b927ea9f2fd748e5"; n_c=1; SESSIONID=fzqbMAKbje9dccCarCkcPFCT0BKgVkd7DPvQr4ssNog; JOID=U1oWA0NMQDxcMYWgYU0Kq1JVeYtyKTtONnXH6gAvJgQ7Wu_gAZrArgM7h6Jq1-Ec58Oummjo7QQqhf6_F53NJBI=; osd=W14SC01ERDhUP42kZUUEo1ZRcYV6LT9GOH3D7gghLgA_UuHoBZ7IoAs_g6pk3-UY782mnmzg4wwugfaxH5nJLBw=; _gat_gtag_UA_149949619_1=1; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1587119453; capsion_ticket="2|1:0|10:1587119453|14:capsion_ticket|44:ZjJlYjViZDAzZmZlNDk2ZDkyNGYwMTRhODU2MzVlZTc=|99c77a667ed9d3ee6fbb32ded30aab0a9c042b32f3fc26b38d019431017cfc57"; KLBRSID=4843ceb2c0de43091e0ff7c22eadca8c|1587119491|1587118801',
                             'referer': 'https://www.zhihu.com/search?q=%E5%B0%9A%E5%BE%B7%E6%9C%BA%E6%9E%84&type=content',
                             'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                             'x-zse-83': '3_2.0', 'x-zse-86': '1.0_a7FBHD90cTYpFBFq0wtqb4e8Q0FYFBt0ZqSqHUr8UhtY'}

        self.headers_zkbk = {'accept': '*/*', 'accept-language': 'zh-CN,zh;q=0.9',
                             'cookie': '_zap=c1ab8bbd-ffc7-4c49-892d-a7823194c57e; d_c0="ACATUdNWIBGPTtzG3d4wxjLmqHlAAYZVO3E=|1587008020"; _ga=GA1.2.401375569.1587008023; _gid=GA1.2.141163472.1587008023; _xsrf=f39c021b-fdfe-4865-9768-db10af88d5aa; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1587008190,1587008275,1587008675,1587020380; l_n_c=1; l_cap_id="NDBhNGY3M2U3OTgxNDlmMDk2NDExOTU3ZDgyN2Y4YjE=|1587040369|12b0d9031184f57dfebd953dccecd60e5e4f58db"; r_cap_id="NDkxZGVhZDU2YTJhNGY2OThlMjkzMjZmYjYzNTZkNWQ=|1587040369|4d56e2de90ddf5888a01ab74fe3e749cb4610256"; cap_id="NDU4YTBhZTc3Yzk0NDNmOTk0YmFkN2RhZWZlNzI5NWI=|1587040369|c5de995a9de07a91998c6c69b927ea9f2fd748e5"; n_c=1; SESSIONID=fzqbMAKbje9dccCarCkcPFCT0BKgVkd7DPvQr4ssNog; JOID=U1oWA0NMQDxcMYWgYU0Kq1JVeYtyKTtONnXH6gAvJgQ7Wu_gAZrArgM7h6Jq1-Ec58Oummjo7QQqhf6_F53NJBI=; osd=W14SC01ERDhUP42kZUUEo1ZRcYV6LT9GOH3D7gghLgA_UuHoBZ7IoAs_g6pk3-UY782mnmzg4wwugfaxH5nJLBw=; _gat_gtag_UA_149949619_1=1; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1587124324; capsion_ticket="2|1:0|10:1587124324|14:capsion_ticket|44:ODBhNDU3ODU5NjI4NDk3OThlY2M0ZTJiMTAxMzk2YjA=|c44542e344eaaa2ca69770dc2e2786d354842bbeeb23b4e3ab3629b9346202e1"; KLBRSID=4843ceb2c0de43091e0ff7c22eadca8c|1587124361|1587118801',
                             'referer': 'https://www.zhihu.com/search?q=%E8%87%AA%E8%80%83%E6%9C%AC%E7%A7%91&type=content',
                             'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                             'x-zse-83': '3_2.0', 'x-zse-86': '1.0_a7Y8Ng9qb8NXnwO0Zw2qHv90ggYfUCOBM0NqQT9yoRFY'}

        self.headers_sd = {'accept': '*/*', 'accept-language': 'zh-CN,zh;q=0.9',
                           'cookie': '_zap=c1ab8bbd-ffc7-4c49-892d-a7823194c57e; d_c0="ACATUdNWIBGPTtzG3d4wxjLmqHlAAYZVO3E=|1587008020"; _ga=GA1.2.401375569.1587008023; _gid=GA1.2.141163472.1587008023; _xsrf=f39c021b-fdfe-4865-9768-db10af88d5aa; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1587008190,1587008275,1587008675,1587020380; l_n_c=1; l_cap_id="NDBhNGY3M2U3OTgxNDlmMDk2NDExOTU3ZDgyN2Y4YjE=|1587040369|12b0d9031184f57dfebd953dccecd60e5e4f58db"; r_cap_id="NDkxZGVhZDU2YTJhNGY2OThlMjkzMjZmYjYzNTZkNWQ=|1587040369|4d56e2de90ddf5888a01ab74fe3e749cb4610256"; cap_id="NDU4YTBhZTc3Yzk0NDNmOTk0YmFkN2RhZWZlNzI5NWI=|1587040369|c5de995a9de07a91998c6c69b927ea9f2fd748e5"; n_c=1; SESSIONID=fzqbMAKbje9dccCarCkcPFCT0BKgVkd7DPvQr4ssNog; JOID=U1oWA0NMQDxcMYWgYU0Kq1JVeYtyKTtONnXH6gAvJgQ7Wu_gAZrArgM7h6Jq1-Ec58Oummjo7QQqhf6_F53NJBI=; osd=W14SC01ERDhUP42kZUUEo1ZRcYV6LT9GOH3D7gghLgA_UuHoBZ7IoAs_g6pk3-UY782mnmzg4wwugfaxH5nJLBw=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1587124805; capsion_ticket="2|1:0|10:1587124805|14:capsion_ticket|44:YWFmOTEyZjlkM2NiNGQxN2FiODJhY2JkNDJlN2FkNjU=|5dc1221ea8802059dbc4605196a867c3e7d0147bc8ac6562600881ece0f30e18"; KLBRSID=4843ceb2c0de43091e0ff7c22eadca8c|1587124937|1587118801',
                           'referer': 'https://www.zhihu.com/search?q=%E5%B0%9A%E5%BE%B7&type=content',
                           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                           'x-zse-83': '3_2.0', 'x-zse-86': '1.0_a0FBnUU06RtfoRFB8XYyke9yr0FxS0N8y9O0r4XBbLNx'}

        self.headers_zk = {'accept': '*/*', 'accept-language': 'zh-CN,zh;q=0.9',
                           'cookie': '_zap=c1ab8bbd-ffc7-4c49-892d-a7823194c57e; d_c0="ACATUdNWIBGPTtzG3d4wxjLmqHlAAYZVO3E=|1587008020"; _ga=GA1.2.401375569.1587008023; _gid=GA1.2.141163472.1587008023; _xsrf=f39c021b-fdfe-4865-9768-db10af88d5aa; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1587008190,1587008275,1587008675,1587020380; l_n_c=1; l_cap_id="NDBhNGY3M2U3OTgxNDlmMDk2NDExOTU3ZDgyN2Y4YjE=|1587040369|12b0d9031184f57dfebd953dccecd60e5e4f58db"; r_cap_id="NDkxZGVhZDU2YTJhNGY2OThlMjkzMjZmYjYzNTZkNWQ=|1587040369|4d56e2de90ddf5888a01ab74fe3e749cb4610256"; cap_id="NDU4YTBhZTc3Yzk0NDNmOTk0YmFkN2RhZWZlNzI5NWI=|1587040369|c5de995a9de07a91998c6c69b927ea9f2fd748e5"; n_c=1; SESSIONID=fzqbMAKbje9dccCarCkcPFCT0BKgVkd7DPvQr4ssNog; JOID=U1oWA0NMQDxcMYWgYU0Kq1JVeYtyKTtONnXH6gAvJgQ7Wu_gAZrArgM7h6Jq1-Ec58Oummjo7QQqhf6_F53NJBI=; osd=W14SC01ERDhUP42kZUUEo1ZRcYV6LT9GOH3D7gghLgA_UuHoBZ7IoAs_g6pk3-UY782mnmzg4wwugfaxH5nJLBw=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1587124362; capsion_ticket="2|1:0|10:1587124363|14:capsion_ticket|44:YWEyN2EzZDliZWQyNDM2ZmI5OGFmODNhNTljYWYxOTY=|f6f8981a5d66d5650fe2e74148ebf3085f23a2e94241c0e3f0fe783751602ab3"; KLBRSID=4843ceb2c0de43091e0ff7c22eadca8c|1587124803|1587118801',
                           'referer': 'https://www.zhihu.com/search?q=%E8%87%AA%E8%80%83&type=content',
                           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
                           'x-zse-83': '3_2.0', 'x-zse-86': '1.0_a82827eqQT2XH9OqTqYyNgX0gBtpo0FqfXOyS6HqFBNY'}

        # 关键词搜索URL
        # 关键词搜索
        self.key_word = "https://www.zhihu.com/api/v4/search_v3?t=general&q={}&correction=1&offset=0&limit=20&lc_idx=0&show_all_topics=0"
        # 专栏URL拼接
        self.zhuanlan = "https://zhuanlan.zhihu.com/p/{}"
        # 问题URL拼接
        self.question = "https://www.zhihu.com/question/{}"
        # 答案URL拼接
        self.answer = "https://www.zhihu.com/question/{}/answer/{}"

        # 检验专栏URL匹配正则
        self.article_re = "zhuanlan.zhihu.com/p/\d+"
        # 检验问题答案URL匹配正则
        self.answer_re = 'zhihu.com/question/\d+/answer/\d+'
        # 检验问题不带答案URL正则
        self.question_re = 'zhihu.com/question/\d+'

        self.all_ids = []
        # 答案信息
        self.answer_dict = {}
        self.key_search_dict = {}


    # 检查url是否匹配
    def check_url(self, _url, type):
        if type == "answer":
            if re.match(self.answer_re, _url):
                return True
            else:
                return False
        elif type == "article":
            if re.match(self.article_re, _url):
                return True
            else:
                return False


    range(1)


    # 获取答案信息
    def get_html_msg(self, _url, use_headers):
        # 获取html返回信息
        html = requests.get(_url, headers=use_headers).text
        time.sleep(1)
        soup = BeautifulSoup(html, 'html.parser')
        _body = soup.find("body")
        # 获取指定位置元素信息
        get_obj = Reuqest_Class.get_element(_body, "script")[3]
        get_msg = json.loads(str(get_obj.string))["initialState"]
        return get_msg


    # 使用关键词搜索结果
    def keyword_search(self, _key_word):
        # 讲中文转换为encode
        url = Reuqest_Class.change_ducode(_key_word)
        use_url = self.key_word.format(url)
        print(use_url)
        # 获取请求数据
        header_key = {"尚德机构": self.headers_sdjg, "自考本科": self.headers_zkbk, "自考": self.headers_zk,
                      "尚德": self.headers_sd}
        html = requests.get(use_url, headers=header_key[_key_word]).text

        # 架构化返回json信息
        _data = json.loads(html)["data"]

        num = 1

        for i in _data:
            msg_dict = {"get_url": "", "get_type": ""}
            try:
                if i["type"] == "search_result":
                    msg_dict["get_type"] = i["object"]["type"]
                    msg_dict["key_word"] = _key_word
                    if msg_dict["get_type"] == "answer":
                        # 当前问题在关键词排序中的位置
                        msg_dict["index"] = num
                        # 获取点赞数信息
                        msg_dict["voteup_count"] = i["object"]["voteup_count"]
                        # 获取评论数信息
                        msg_dict["comment_count"] = i["object"]["comment_count"]
                        # 获取作者信息
                        msg_dict["author_name"] = i["object"]["author"]["name"]

                        get_url = i["object"]["question"]["url"]
                        # 将api形式的url转为可以浏览信息的url形式
                        msg_dict["get_url"] = get_url.replace("api.zhihu", "zhihu").replace("questions", "question")
                        # 问题id
                        msg_dict["question_id"] = i["object"]["question"]["id"]

                        # self.key_search_dict[msg_dict["question_id"]] = msg_dict

                        print("搜索问题（{}）答案".format(msg_dict["get_url"]))

                        answer_url = self.question.format(msg_dict["question_id"])
                        get_answer_dict = self.get_html_msg(answer_url, header_key[_key_word])

                        answerids = get_answer_dict["question"]["answers"][msg_dict["question_id"]]["ids"]
                        for _index, _item in enumerate(answerids):
                            get_answer = get_answer_dict["entities"]["answers"][str(_item)]
                            use_dict = {}
                            use_dict["question_index"] = num
                            use_dict["answer_index"] = _index + 1
                            use_dict["answer_id"] = _item
                            use_dict["question_id"] = msg_dict["question_id"]
                            use_dict["author_name"] = get_answer["author"]["name"]
                            use_dict["voteup_count"] = get_answer["voteupCount"]
                            use_dict["key_word"] = _key_word
                            # 获取评论数信息
                            use_dict["comment_count"] = get_answer["commentCount"]
                            use_dict["url"] = self.answer.format(use_dict["question_id"], use_dict["answer_id"])

                            self.answer_dict[use_dict["answer_id"]] = use_dict
                            self.all_ids.append(use_dict["answer_id"])
                        num += 1

                    elif msg_dict["get_type"] == "article":
                        # 当前问题在关键词排序中的位置
                        msg_dict["index"] = num
                        # 获取点赞数信息
                        msg_dict["voteup_count"] = i["object"]["voteup_count"]
                        # 获取评论数信息
                        msg_dict["comment_count"] = i["object"]["comment_count"]
                        # 获取作者信息
                        msg_dict["author_name"] = i["object"]["author"]["name"]
                        # id
                        msg_dict["id"] = i["object"]["id"]
                        get_url = i["object"]["url"]
                        # 将api形式的url转为可以浏览信息的url形式
                        msg_dict["get_url"] = get_url.replace("api.zhihu", "zhuanlan.zhihu").replace("articles", "p")

                        print("搜索文章（{}）".format(msg_dict["get_url"]))

                        self.key_search_dict[msg_dict["id"]] = msg_dict

                        self.all_ids.append(msg_dict["id"])
                        num += 1
                    else:
                        continue
                else:
                    continue

            except:
                print("ERROR")
                break


    def print_all(self):
        return self.all_ids


def RunZhiHu():
    # 知乎需要搜索的关键词
    word_list = ["尚德机构", "自考本科", "自考", "尚德"]
    # 读取需要对比的数据
    read_msg = Read_excel("./优质UGC汇总.xlsx")

    answer_ids = []
    zhunalan_ids = []

    for i in range(2, read_msg.nrows - 1):
        sub_dict = {}

        get_msg = read_msg.get_msg(i, 7)

        # text_msg = Str_Class.get_word(read_msg.get_msg(i, 8))
        # sub_dict["text"] = text_msg
        sub_dict["type"] = "zhuanlan"
        sub_dict["name"] = read_msg.get_msg(i, 5)

        if "zhuanlan.zhihu.com" in get_msg:
            sub_dict["type"] = "zhuanlan"
            sub_dict["get_id"] = get_msg.split("?")[0].split("/")[-1]

            zhunalan_ids.append(sub_dict["get_id"])

        elif "zhihu.com/question" in get_msg:
            use_cut = get_msg.split("?")[0]
            sub_dict["type"] = "question"
            sub_dict["question_id"] = use_cut.split("/")[-3]
            sub_dict["answer_id"] = use_cut.split("/")[-1]

            answer_ids.append(sub_dict["answer_id"])

        elif "zhihu.com/answer" in get_msg:
            use_cut = get_msg.split("?")[0]
            sub_dict["type"] = "question"
            sub_dict["answer_id"] = use_cut.split("/")[-1]

            answer_ids.append(sub_dict["answer_id"])

        else:
            continue

    # word_list = ["尚德机构"]
    new_obj = ZhiHu_Class()
    current_key_word = ""
    for _word in word_list:
        current_key_word = _word
        print("当前搜索关键词：{}".format(_word))
        new_obj.keyword_search(_word)

    answer_ids = [int(i) for i in answer_ids]
    zhunalan_ids = [int(i) for i in zhunalan_ids]

    intersection_answer = set(answer_ids) & set(new_obj.print_all())
    intersection_atriacl = set(zhunalan_ids) & set(new_obj.print_all())
    print("get_all_ids:{}".format(new_obj.print_all()))
    print("answer_ids:{}".format(answer_ids))
    print("zhunalan_ids:{}".format(zhunalan_ids))
    print(intersection_answer, intersection_atriacl)


    # 以下输出结果为提供给老师的信息
    for get_id in intersection_atriacl:
        _msg = new_obj.key_search_dict[get_id]
        print("文章\n链接:{}\n关键词:{}\n排序:{}\n点赞数:{}\n评论数:{}\n作者:{}\n".format(_msg["get_url"], _msg["key_word"],
                                                                         _msg["index"], _msg["voteup_count"],
                                                                         _msg["comment_count"],
                                                                         _msg["author_name"]))

    for get_id in intersection_answer:
        _msg = new_obj.answer_dict[get_id]
        print("问题\n链接:{}\n关键词:{}\n问题排序:{}\n答案排序:{}\n点赞数:{}\n评论数:{}\n作者:{}\n".format(_msg["url"], _msg["key_word"],
                                                                                    _msg["question_index"],
                                                                                    _msg["answer_index"],
                                                                                    _msg["voteup_count"],
                                                                                    _msg["comment_count"],
                                                                                    _msg["author_name"]))


if __name__ == "__main__":
    RunZhiHu()
