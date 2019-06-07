# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2019/6/7-13:07'
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from ..models import Module, Case


class BaseViewCase:

    @staticmethod
    def case(request, path, mid):
        mo = Module.objects.get(pk=mid)
        template = loader.get_template(path)
        context = {'case_list': mo.case_set.all(), "mid": mid, "name": mo.name}
        return HttpResponse(template.render(context, request))

    @staticmethod
    @csrf_exempt
    def case_new(kw):
        mo = Module.objects.get(pk=kw["mid"])
        name = kw["name"]
        mo.case_set.create(name=name)
        result = {'code': 0, 'msg': '保存成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def case_edit(kw):
        c = Case.objects.get(pk=kw["cid"])
        c.name = kw["name"]
        c.save()
        result = {'code': 0, 'msg': '编辑成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def case_del(cid):
        c = Case.objects.get(pk=cid)
        c.delete()
        result = {'code': 0, 'msg': '删除成功'}
        return JsonResponse(result)
