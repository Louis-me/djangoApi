#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2019/8/10-11:04'
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from ..models import Case, CaseCommonCase, CommonCase

'''
用例关联公共用例
'''


class BaseViewCaseCommonCase:

    @staticmethod
    def case_common_case(request, path, mid, cid):
        template = loader.get_template(path)
        ca = Case.objects.get(pk=cid)
        context = {"cid": cid, "common_case_list": ca.casecommoncase_set.order_by("sort"),
                   "name": ca.name, "mid": mid, "common_case": CommonCase.objects.all()}
        return HttpResponse(template.render(context, request))

    @staticmethod
    @csrf_exempt
    def case_common_case_new(kw):
        ta = Case.objects.get(pk=kw["cid"])
        ta.casecommoncase_set.create(name=kw["name"], cc_id=kw["cc_id"], sort=kw["sort"])
        result = {'code': 0, 'msg': '保存成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def case_common_case_edit(kw):
        tm = CaseCommonCase.objects.get(pk=kw["ccc_id"])
        tm.name = kw["name"]
        tm.cc_id = kw["cc_id"]
        tm.sort = kw["sort"]
        tm.save()
        result = {'code': 0, 'msg': '编辑成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def case_common_case_del(ccs_id):
        tm = CaseCommonCase.objects.get(pk=ccs_id)
        tm.delete()
        result = {'code': 0, 'msg': '删除成功'}
        return JsonResponse(result)
