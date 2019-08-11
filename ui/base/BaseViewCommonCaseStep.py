#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2019/8/10-11:04'
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from ..models import CommonCase, CommonCaseStep

'''
公共用例下的步骤
'''


class BaseViewCommonCaseStep:

    @staticmethod
    def common_case_step(request, path, cc_id):
        ca = CommonCase.objects.get(pk=cc_id)
        template = loader.get_template(path)
        context = {'step_list': ca.commoncasestep_set.order_by("sort"), "cc_id": cc_id, "name": ca.name}
        return HttpResponse(template.render(context, request))

    @staticmethod
    @csrf_exempt
    def common_case_step_new(kw):
        ca = CommonCase.objects.get(pk=kw["cc_id"])
        name = kw["name"]
        element_info = kw["element_info"]
        find_type = kw["find_type"]
        operate_type = kw["operate_type"]
        extend = kw["extend"]
        sort = kw.get("sort", 0)

        ca.commoncasestep_set.create(name=name, element_info=element_info, find_type=find_type,
                                     operate_type=operate_type,
                                     extend=extend, sort=sort)
        result = {'code': 0, 'msg': '保存成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def common_case_step_edit(kw):
        c = CommonCaseStep.objects.get(pk=kw["ccs_id"])
        c.name = kw["name"]
        c.element_info = kw["element_info"]
        c.find_type = kw["find_type"]
        c.operate_type = kw["operate_type"]
        c.extend = kw["extend"]
        c.sort = kw["sort"]
        c.save()
        result = {'code': 0, 'msg': '编辑成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def common_case_step_del(ccs_id):
        c = CommonCaseStep.objects.get(pk=ccs_id)
        c.delete()
        result = {'code': 0, 'msg': '删除成功'}
        return JsonResponse(result)
