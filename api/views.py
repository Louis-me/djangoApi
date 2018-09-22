import ast
import xlsxwriter
import requests
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from api.base.BaseElementEnmu import Element
from api.base.BaseExcel import OperateReport
from api.base.BaseFile import BaseFile
from api.base.BaseView import new_report_item, edit_report, write_excel, get_session, new_report, _check
from .models import *
from django.forms.models import model_to_dict
from .base.BaseParams import BaseParams
import json
import time
from datetime import datetime
import uuid
from .base import BaseLog
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from  mysite import settings
import os

c_check = {"passed": 0, "failed": -1, "no_check": -2}


def index(request):
    list_report = Report.objects.order_by('-id')
    template = loader.get_template('api/index.html')
    paginator = Paginator(list_report, 8, 2)  # 每页8条数据，少于2条则合并到上一页
    page = request.GET.get('page')

    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)

    context = {
        "list_report": customer
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def report_del(request):
    r_id = request.POST["rid"]
    Report.objects.get(pk=r_id).delete()
    result = {'code': 0, 'msg': '删除成功'}
    return JsonResponse(result)


# 测试模块的用例列表接口
def report_detail(request, id):
    rp = Report.objects.get(pk=id)
    template = loader.get_template('api/reportDetail.html')
    context = {'case_list': rp.reportitem_set.all()}
    return HttpResponse(template.render(context, request))


# 下载日志
@csrf_exempt
def download_log(request):
    def file_iterator(file_name, chunk_size=2612000):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    file_path = request.POST["log"]
    file_name = os.path.join(settings.BASE_DIR, "api/Log", file_path + ".log")
    http_file = "http://192.168.1.100:8001/api/Log/" + file_path + ".log"
    # 192.168.1.100:8001在apache中设置
    response = HttpResponse(file_iterator(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("report.log")
    # result = {'code': 0, 'msg': '下载成功', "path": file_name}
    result = {'code': 0, 'msg': '下载成功', "path": http_file}
    return JsonResponse(result)


# 下载excel
@csrf_exempt
def download_excel(request):
    def file_iterator(file_name, chunk_size=512):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    file_path = request.POST["excel"]
    file_name1 = os.path.join(settings.BASE_DIR, "api/Report", file_path + ".xlsx")
    http_file = "http://192.168.1.100:8001/api/Report/" + file_path + ".xlsx"

    response = HttpResponse(file_iterator(file_name1))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("report.xlsx")
    # result = {'code': 0, 'msg': '下载成功', "path": file_name1}
    result = {'code': 0, 'msg': '下载成功', "path": http_file}
    return JsonResponse(result)


# 接口测试需要登录
def login(request):
    template = loader.get_template('api/login.html')
    context = {'login': Login.objects.get(pk=1)}
    return HttpResponse(template.render(context, request))


# 编辑登录接口参数
@csrf_exempt
def login_edit(request):
    l = Login.objects.get(pk=1)
    l.url = request.POST["url"]
    l.params = request.POST["params"]
    l.save()
    result = {'code': 0, 'msg': '保存成功'}
    return JsonResponse(result)


# 模块列表
def module(request):
    template = loader.get_template('api/module.html')
    context = {'module_list': Module.objects.all()}
    return HttpResponse(template.render(context, request))


@csrf_exempt
def module_new(request):
    Module(name=request.POST["name"]).save()
    result = {'code': 0, 'msg': '保存成功'}
    return JsonResponse(result)


# 编辑模块
@csrf_exempt
def module_edit(request):
    m_id = request.POST["id"]
    name = request.POST["name"]
    m = Module.objects.get(pk=m_id)
    m.name = name
    m.save()
    result = {'code': 0, 'msg': '编辑成功'}
    return JsonResponse(result)


# 删除模块
@csrf_exempt
def module_del(request):
    m_id = request.POST["mid"]
    m = Module.objects.get(pk=m_id)
    m.delete()
    result = {'code': 0, 'msg': '删除成功'}
    return JsonResponse(result)


# 模块下的用例列表
def case(request, id):
    mo = Module.objects.get(pk=id)
    template = loader.get_template('api/case.html')
    context = {'case_list': mo.case_set.all(), "mid": id}
    return HttpResponse(template.render(context, request))


# 新建用例
@csrf_exempt
def case_new(request):
    mo = Module.objects.get(pk=request.POST["mid"])
    name = request.POST["name"]
    url = request.POST["url"]
    protocol = request.POST["protocol"]
    method = request.POST["method"]
    params = request.POST["params"]
    hope = request.POST.get("hope", "")
    mo.case_set.create(name=name, url=url, protocol=protocol, method=method, params=params, hope=hope)
    result = {'code': 0, 'msg': '保存成功'}
    return JsonResponse(result)


# 编辑用例
@csrf_exempt
def case_edit(request):
    c_id = request.POST["cid"]
    c = Case.objects.get(pk=c_id)
    name = request.POST["name"]
    url = request.POST["url"]
    protocol = request.POST["protocol"]
    method = request.POST["method"]
    params = request.POST["params"]
    hope = request.POST["hope"]
    c.name = name
    c.url = url
    c.protocol = protocol
    c.method = method
    c.params = params
    c.hope = hope
    c.save()
    result = {'code': 0, 'msg': '编辑成功'}
    return JsonResponse(result)


# 删除用例
@csrf_exempt
def case_del(request):
    c_id = request.POST["cid"]
    c = Case.objects.get(pk=c_id)
    c.delete()
    result = {'code': 0, 'msg': '删除成功'}
    return JsonResponse(result)


# 模糊用列表
def fuzz(request, id):
    c = Case.objects.get(pk=id)
    template = loader.get_template('api/fuzz.html')
    context = {'fuzz_list': c.fuzzcase_set.all(), 'cid': id}
    return HttpResponse(template.render(context, request))


# 生成模糊用例
@csrf_exempt
def batch_fuzz(request):
    bf = BaseFile()
    bf.mk_file(Element.PICT_PARAM)
    bf.mk_file(Element.PICT_PARAM_RESULT)
    c_id = request.POST["cid"]
    c = Case.objects.get(pk=c_id)
    md = model_to_dict(c)
    params = BaseParams().param_fi(md["params"])["params"]
    for i in params:
        _info = i["info"]
        i.pop("info")
        # if i.get("right", " ") != " ":
        #     hope = c.hope
        #     i.pop("right")
        # else:
        #     hope = ""
        c.fuzzcase_set.create(name="【%s】%s" % (c.name, _info), params=i, hope="")
    result = {'code': 0, 'msg': '生成模糊用例成功'}
    return JsonResponse(result)


# 新建模糊用例
@csrf_exempt
def fuzz_new(request):
    cid = request.POST["cid"]
    c = Case.objects.get(pk=cid)
    c.fuzz_set.create(name="【%s】%s" % (c.name, request.POST["name"]), params=request.POST['params'],
                      hope=request.POST.get('hope', ''))
    result = {'code': 0, 'msg': '新建模糊用例成功'}
    return JsonResponse(result)


# 编辑模糊用例
@csrf_exempt
def fuzz_edit(request):
    fid = request.POST["fid"]
    f = FuzzCase.objects.get(pk=fid)
    f.name = request.POST["name"]
    f.params = request.POST["params"]
    f.hope = request.POST.get('hope', '')
    f.save()
    result = {'code': 0, 'msg': '编辑模糊用例成功'}
    return JsonResponse(result)


# 删除模糊用例
@csrf_exempt
def fuzz_del(request):
    fid = request.POST["fid"]
    FuzzCase.objects.get(pk=fid).delete()
    result = {'code': 0, 'msg': '删除模糊用例成功'}
    return JsonResponse(result)


@csrf_exempt
def run(request):
    mid = request.POST["mid"]
    list_case = Module.objects.get(pk=mid).case_set.all()
    if not list_case:
        result = {'code': -1, 'msg': '无测试用例'}
        return JsonResponse(result)
    excel_init = {}
    excel_detail = []
    uid = str(uuid.uuid1())
    base_log = BaseLog.Log(uid + ".log")
    req = get_session()
    passed = failed = no_check = 0
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    _report = new_report({"name": Module.objects.get(pk=mid).name, "uid": uid})
    for c in list_case:
        ls_fuzz = Case.objects.get(pk=c.id).fuzzcase_set.all()

        r_time = time.time()
        if ls_fuzz:  # 如果用模糊用例
            print("=====有模糊用例====")
            for fu in ls_fuzz:
                s_time = int(round(time.time() * 1000))
                resp = ""
                if c.method == "post":
                    resp = req.post(url=c.protocol + "://" + c.url, data=json.dumps(fu.params))
                    base_log.buildStartLine("请求url=%s" % resp.url)
                    base_log.buildStartLine("请求参数=%s" % fu.params)
                if c.method == "get":
                    resp = req.get(url=c.protocol + "://" + c.url, params=ast.literal_eval(fu.params))
                    base_log.buildStartLine("请求url=%s" % resp.url)
                    base_log.buildStartLine("请求参数=%s" % fu.params)
                e_time = int(round(time.time() * 1000))
                app = {"name": fu.name, "url": resp.url, "protocol": c.protocol, "report": _report,
                       "method": c.method, "params": fu.params, "hope": fu.hope,
                       "sum_time": str(e_time - s_time) + "ms",
                       "fact": resp.text, "uid": uid, "result": c_check["no_check"], "code": resp.status_code}
                no_check += 1
                new_report_item(app)
                repo_item = {"url": resp.url, "method": c.method, "params": fu.params, "name": fu.name, "hope": fu.hope,
                             "code": resp.status_code, "fact": resp.text, "result": c_check["no_check"],
                             "sum_time": str(e_time - s_time) + "ms"}
                excel_detail.append(repo_item)

        res = ""
        ss_time = int(round(time.time() * 1000))
        if c.method == "post":
            res = req.post(url=c.protocol + "://" + c.url, data=json.dumps(c.params))
            base_log.buildStartLine("请求url=%s" % res.url)
            base_log.buildStartLine("请求参数=%s" % c.params)
        if c.method == "get":
            res = req.get(url=c.protocol + "://" + c.url, params=ast.literal_eval(c.params))
            base_log.buildStartLine("请求url=%s" % res.url)
            base_log.buildStartLine("请求参数=%s" % c.params)
        ee_time = int(round(time.time() * 1000))

        _result = _check({"hope": c.hope, "fact": res.text})
        if _result == c_check["passed"]:
            passed += 1
            base_log.buildEndLine("检查点=通过")
        elif _result == c_check["failed"]:
            failed += 1
            base_log.buildEndLine("检查点=失败")

        app = {"report": _report, "name": c.name, "url": res.url, "protocol": c.protocol, "method": c.method,
               "code": res.status_code,
               "params": c.params, "hope": c.hope, "sum_time": str(ee_time - ss_time) + "ms", "fact": res.text,
               "result": _result}
        new_report_item(app)
        r_e_time = time.time()
        edit_report({"sum_time": "%.2f" % (r_e_time - r_time) + "秒", "passed": passed, "failed": failed,
                     "no_check": no_check, "report": _report})

        # report_init
        excel_init["start_time"] = start_time
        excel_init["sum_time"] = "%.2f" % (r_e_time - r_time) + "秒"
        excel_init["sum_case"] = passed + failed + no_check
        excel_init["passed"] = passed
        excel_init["failed"] = failed
        excel_init["no_check"] = no_check

        # report_detail
        repo_item = {"url": res.url, "method": c.method, "params": c.params, "name": c.name, "hope": c.hope,
                     "code": res.status_code, "fact": res.text, "result": _result,
                     "sum_time": str(ee_time - ss_time) + "ms"}
        excel_detail.append(repo_item)

    result = {'code': 0, 'msg': '测试完成'}
    write_excel({"uid": uid, "excel_init": excel_init, "excel_detail": excel_detail})
    return JsonResponse(result)