import ast
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from ..models import Module, Case


class BaseViewCase:

    @staticmethod
    def case(request, path, id):
        mo = Module.objects.get(pk=id)
        template = loader.get_template(path)
        context = {'case_list': mo.case_set.all(), "mid": id, "name": mo.name}
        return HttpResponse(template.render(context, request))

    @staticmethod
    @csrf_exempt
    def case_new(kw):
        mo = Module.objects.get(pk=kw["mid"])
        name = kw["name"]
        url = kw["url"]
        protocol = kw["protocol"]
        method = kw["method"]
        params = kw["params"]
        hope = kw["hope"]
        mo.case_set.create(name=name, url=url, protocol=protocol, method=method, params=params, hope=hope)
        result = {'code': 0, 'msg': '保存成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def case_edit(kw):
        c = Case.objects.get(pk=kw["cid"])
        c.name = kw["name"]
        c.url = kw["url"]
        c.protocol = kw["protocol"]
        c.method = kw["method"]
        c.params = kw["params"]
        c.hope = kw["hope"]
        c.save()
        result = {'code': 0, 'msg': '编辑成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def case_del(id):
        c = Case.objects.get(pk=id)
        c.delete()
        result = {'code': 0, 'msg': '删除成功'}
        return JsonResponse(result)
