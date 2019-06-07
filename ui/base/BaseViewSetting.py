# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2019/6/7-13:07'
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from ..models import Setting


class BaseViewSetting:

    @staticmethod
    def setting(request, path):
        template = loader.get_template(path)
        context = {'setting': Setting.objects.get(pk=1)}
        return HttpResponse(template.render(context, request))

    @staticmethod
    @csrf_exempt
    def setting_edit(kw):
        try:
            l = Setting.objects.get(pk=1)
            l.home_url = kw["home_url"]
            l.login_url = kw["login_url"]
            l.save()
            result = {'code': 0, 'msg': '保存成功'}
        except :
            result = {'code': -1, 'msg': '保存失败'}
        return JsonResponse(result)
