# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2019/6/7-13:07'
from django.http import JsonResponse, HttpResponse
from django.template import loader

from ..models import *


class BaseViewDashBoard:

    @staticmethod
    def dashBoard(request, path):
        template = loader.get_template(path)
        return HttpResponse(template.render({}, request))

    # 模块下用例统计
    @staticmethod
    def dashBoard_module_case(request):
        mo = Module.objects.all()
        data = []
        for i in mo:
            list_case = Module.objects.get(pk=i.id).case_set.all()
            if not list_case:
                result = {'code': -1, 'msg': '无测试用例'}
                return JsonResponse(result)
            num = 0
            temp = []
            for c in list_case:
                # ls_fuzz = Case.objects.get(pk=c.id).fuzzcase_set.all()
                # if ls_fuzz:  # 如果用模糊用例
                #     for fu in ls_fuzz:
                #         num += 1
                num += 1
            temp.append(i.name)
            temp.append(num)
            data.append(temp)
        result = {'code': 0, "data": data}
        return JsonResponse(result)

    '''
    前十个task的用例执行情况
    '''

    @staticmethod
    def dashBoard_top10_task(request):
        rp = Report.objects.order_by("-id")[1:10]
        data = []
        categories = []
        # [{name: '读请求',data:rtps
        passed = {"data": [], "name": "通过"}
        # no_check = {"data": [], "name": "未检测"}
        failed = {"data": [], "name": "失败", "color": "red"}
        for i in rp:
            print(i.id)
            passed["data"].append(i.passed)
            failed["data"].append(i.failed)
            # no_check["data"].append(i.no_check)
            categories.append(i.name)
        data.append(passed)
        data.append(failed)
        # data.append(no_check)
        result = {'code': 0, "data": data}
        return JsonResponse(result)

    '''
    前100个case的耗时情况
    '''

    @staticmethod
    def dashBoard_top100_case_time(request):
        data = []
        rps = ReportItem.objects.order_by()[1:100]
        for i in rps:
            sum_time = float(i.sum_time.split("秒")[0])
            data.append(sum_time)
        result = {'code': 0, "data": [{"name":"耗时", "data":data}]}
        return JsonResponse(result)
