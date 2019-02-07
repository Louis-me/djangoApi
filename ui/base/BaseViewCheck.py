import ast
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from ..models import Checks, Case


class BaseViewCheck:

    @staticmethod
    def check(request, path, mid, cid):
        ca = Case.objects.get(pk=cid)
        template = loader.get_template(path)
        context = {'check_list': ca.checks_set.all(), "cid": cid, "name": ca.name, "mid": mid}
        return HttpResponse(template.render(context, request))

    @staticmethod
    @csrf_exempt
    def check_new(kw):
        ca = Case.objects.get(pk=kw["cid"])
        name = kw["name"]
        element_info = kw["element_info"]
        find_type = kw["find_type"]
        operate_type = kw["operate_type"]
        extend = kw["extend"]
        ca.checks_set.create(name=name, element_info=element_info, find_type=find_type, operate_type=operate_type,
                             extend=extend)
        result = {'code': 0, 'msg': '保存成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def check_edit(kw):
        c = Checks.objects.get(pk=kw["chid"])
        c.name = kw["name"]
        c.element_info = kw["element_info"]
        c.find_type = kw["find_type"]
        c.operate_type = kw["operate_type"]
        c.extend = kw["extend"]
        c.save()
        result = {'code': 0, 'msg': '编辑成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def check_del(chid):
        c = Case.objects.get(pk=chid)
        c.delete()
        result = {'code': 0, 'msg': '删除成功'}
        return JsonResponse(result)
