# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2019/6/7-13:07'
import ast
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from ..models import Login


class BaseViewLogin:

    @staticmethod
    def login(request, path):
        template = loader.get_template(path)
        context = {'login_list': Login.objects.order_by("sort")}
        return HttpResponse(template.render(context, request))

    @staticmethod
    @csrf_exempt
    def login_edit(kw):
        print(kw)
        l = Login.objects.get(pk=kw["id"])
        l.find_type = kw["find_type"]
        l.name = kw["name"]
        l.element_info = kw["element_info"]
        l.operate_type = kw["operate_type"]
        l.extend = kw["extend"]
        l.sort = kw["sort"]
        l.save()
        result = {'code': 0, 'msg': '保存成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def login_new(kw):
        name = kw["name"]
        find_type = kw["find_type"]
        element_info = kw["element_info"]
        operate_type = kw["operate_type"]
        extend = kw["extend"]
        sort = kw["sort"]
        Login(find_type=find_type, element_info=element_info, operate_type=operate_type, extend=extend, sort=sort,
              name=name).save()
        result = {'code': 0, 'msg': '保存成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def login_del(lid):
        Login(pk=lid).delete()
        result = {'code': 0, 'msg': '删除成功'}
        return JsonResponse(result)
