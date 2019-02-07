import ast
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from ..models import Module

from api.base.BaseElementEnmu import Element
from api.base.BaseView import new_report_item, edit_report, write_excel, get_session, new_report, _check
from ..models import Module, Case
import json
import time
from datetime import datetime
import uuid
from ..base import BaseLog
import sys
import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

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