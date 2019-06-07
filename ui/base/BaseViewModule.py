# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2019/6/7-13:07'
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from ..models import Module, Case


class BaseViewModule:

    @staticmethod
    def module(request, path):
        template = loader.get_template(path)
        context = {'module_list': Module.objects.all()}
        return HttpResponse(template.render(context, request))

    @staticmethod
    @csrf_exempt
    def module_new(name):
        Module(name=name).save()
        result = {'code': 0, 'msg': '保存成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def module_edit(kw):
        m_id = kw["id"]
        name = kw["name"]
        m = Module.objects.get(pk=m_id)
        m.name = name
        m.save()
        result = {'code': 0, 'msg': '编辑成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def module_del(id):
        m = Module.objects.get(pk=id)
        m.delete()
        result = {'code': 0, 'msg': '删除成功'}
        return JsonResponse(result)
