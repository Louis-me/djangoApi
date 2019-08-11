#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2019/8/10-11:04'

from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from ..models import CommonCase

'''
公共用例
'''


class BaseViewCommonCase:
    @staticmethod
    def common_case(request, path):
        template = loader.get_template(path)
        context = {'case_list': CommonCase.objects.all()}
        return HttpResponse(template.render(context, request))

    @staticmethod
    @csrf_exempt
    def common_case_new(name):
        CommonCase(name=name).save()
        result = {'code': 0, 'msg': '保存成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def common_case_edit(kw):
        id = kw["id"]
        name = kw["name"]
        ta = CommonCase.objects.get(pk=id)
        ta.name = name
        ta.save()
        result = {'code': 0, 'msg': '编辑成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def common_case_del(id):
        ta = CommonCase.objects.get(pk=id)
        ta.delete()
        result = {'code': 0, 'msg': '删除成功'}
        return JsonResponse(result)
