#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from SearchEngine.Code.File_Read_write import Write_Read
from SearchEngine.Code.Search_Function import Search_Function
from SearchEngine.Code.Wapper import wapper
from SearchEngine.ZhiHu.ZhiHu import RunZhiHu

# import logging
# logger = logging.getLogger("django")

global_search = None


# 搜索
def Search_msg(request):
    response_data = {"code": 500, "msg": ""}
    if request.method == "POST":
        response_data = {}
        try:
            req = json.loads(request.body.decode("utf-8"))
            search_words = req["words"]
            # logger.info("NotionalWords start question: {}".format(search_words))

            return_dict = global_search.search_function(search_words)

        except Exception as e:
            # logger.error("views.question eval error:%s" % str(e))
            response_data["code"] = 500
            response_data["msg"] = str(e)
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data["msg"] = "request type must be POST"
    return HttpResponse(json.dumps(return_dict, ensure_ascii=False), content_type="application/json, charset=utf-8")


def test(request):
    from SearchEngine.DownLoad_Files.Unstructured.BeiJing import BeiJing_Class
    BeiJing_Class.Get_Msg()
    return HttpResponse(json.dumps("ok"), content_type="application/json")


def zhihu(request):
    print("zhihu")
    RunZhiHu()
    return HttpResponse(json.dumps("ok"), content_type="application/json")


@wapper
class new_start(object):
    def __init__(self):
        global global_search
        new_start = Write_Read()
        global_search = Search_Function(new_start.start_check())


_new = new_start()
