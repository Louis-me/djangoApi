# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2019/6/7-13:07'
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from ..models import Task, TaskModule, Module


class BaseViewTaskModule:

    @staticmethod
    def task_module(request, path, id):
        template = loader.get_template(path)
        ta = Task.objects.get(pk=id)
        context = {'ta_module_list': ta.taskmodule_set.all(), "tid": id, "module_list": Module.objects.all(), "name": ta.name}
        return HttpResponse(template.render(context, request))

    @staticmethod
    @csrf_exempt
    def task_module_new(tid, name, mid):
        ta = Task.objects.get(pk=tid)
        ta.taskmodule_set.create(name=name, mid=mid)
        result = {'code': 0, 'msg': '保存成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def task_module_edit(kw):
        tm = TaskModule.objects.get(pk=kw["tmid"])
        tm.name = kw["name"]
        tm.mid = kw["mid"]
        tm.save()
        result = {'code': 0, 'msg': '编辑成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def task_module_del(tmid):
        tm = TaskModule.objects.get(pk=tmid)
        tm.delete()
        result = {'code': 0, 'msg': '删除成功'}
        return JsonResponse(result)
