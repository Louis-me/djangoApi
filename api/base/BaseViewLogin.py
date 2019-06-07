# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2019/6/7-13:07'
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from ..models import Login

class BaseViewLogin:

    @staticmethod
    def login(request, path):
        template = loader.get_template(path)
        context = {'login': Login.objects.get(pk=1)}
        return HttpResponse(template.render(context, request))

    @staticmethod
    @csrf_exempt
    def login_edit(kw):
        l = Login.objects.get(pk=1)
        l.url = kw["url"]
        l.params = kw["params"]
        l.save()
        result = {'code': 0, 'msg': '保存成功'}
        return JsonResponse(result)


