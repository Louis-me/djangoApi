# -*- coding=utf-8 -*-
__author__ = 'shikun'
__CreateAt__ = '2019/6/7-13:07'
from django.forms import model_to_dict
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from api.base.BaseElementEnmu import Element
# from api.base.BaseParams import BaseParams
from ..models import Case, FuzzCase
from ..base.BaseFile import BaseFile as bf
from ..base.BaseFuzzParams import BaseFuzzParams
import ast
class BaseViewFuzz:

    @staticmethod
    def fuzz(request, path, mid, cid):
        c = Case.objects.get(pk=cid)
        template = loader.get_template(path)
        context = {'fuzz_list': c.fuzzcase_set.all(), "mid": mid, "case": c}
        return HttpResponse(template.render(context, request))

    @staticmethod
    @csrf_exempt
    def batch_fuzz(id):
        # bf.mk_file(Element.PICT_PARAM)
        # bf.mk_file(Element.PICT_PARAM_RESULT)
        c = Case.objects.get(pk=id)
        # md = model_to_dict(c)
        # params = BaseParams().param_fi(md["params"])["params"]
        params = BaseFuzzParams().param_fi(ast.literal_eval(c.params))
        for i in params:
            _info = i["info"]
            i.pop("info")
            c.fuzzcase_set.create(name="【%s】%s" % (c.name, _info), params=i, hope="",  protocol=c.protocol, method=c.method, url=c.url)
        result = {'code': 0, 'msg': '生成模糊用例成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def fuzz_new(kw):
        cid = kw["cid"]
        c = Case.objects.get(pk=cid)
        name = kw["name"]
        url = kw["url"]
        protocol = kw["protocol"]
        method = kw["method"]
        params = kw["params"]
        hope = kw["hope"]
        c.fuzzcase_set.create(name=name, url=url, protocol=protocol, method=method, params=params, hope=hope)
        result = {'code': 0, 'msg': '新建模糊用例成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def fuzz_edit(kw):
        fid = kw["fid"]
        f = FuzzCase.objects.get(pk=fid)
        f.name = kw["name"]
        f.url = kw["url"]
        f.protocol = kw["protocol"]
        f.method = kw["method"]
        f.params = kw["params"]
        f.hope = kw["hope"]
        f.save()
        result = {'code': 0, 'msg': '编辑成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def fuzz_del(fid):
        FuzzCase.objects.get(pk=fid).delete()
        result = {'code': 0, 'msg': '删除模糊用例成功'}
        return JsonResponse(result)
