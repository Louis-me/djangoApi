import ast
import json
import time
import uuid
from datetime import datetime

from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from api.base import BaseLog
from api.base.BaseElementEnmu import Element
from api.base.BaseView import get_session, new_report, _check, new_report_item, edit_report, write_excel
from ..models import Task, Module, Case


class BaseViewTask:

    @staticmethod
    def task(request, path):
        template = loader.get_template(path)
        context = {'task_list': Task.objects.all()}
        return HttpResponse(template.render(context, request))

    @staticmethod
    @csrf_exempt
    def task_new(name):
        Task(name=name).save()
        result = {'code': 0, 'msg': '保存成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def task_edit(kw):
        id = kw["id"]
        name = kw["name"]
        ta = Task.objects.get(pk=id)
        ta.name = name
        ta.save()
        result = {'code': 0, 'msg': '编辑成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def task_del(id):
        ta = Task.objects.get(pk=id)
        ta.delete()
        result = {'code': 0, 'msg': '删除成功'}
        return JsonResponse(result)

    @staticmethod
    @csrf_exempt
    def task_run(tid):
        ta = Task.objects.get(id=tid)  # 单个任务
        mo = ta.taskmodule_set.all()  # 任务下的模块
        excel_init = {}
        excel_detail = []
        uid = str(uuid.uuid1())
        base_log = BaseLog.Log(uid + ".log")
        req = get_session()
        passed = failed = no_check = 0
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        r_time = time.time()
        _report = new_report({"name": ta.name, "uid": uid})
        for i in mo:
            list_case = Module.objects.get(pk=i.mid).case_set.all()
            if not list_case:
                result = {'code': -1, 'msg': '无测试用例'}
                return JsonResponse(result)

            for c in list_case:
                ls_fuzz = Case.objects.get(pk=c.id).fuzzcase_set.all()
                if ls_fuzz:  # 如果用模糊用例
                    print("=====有模糊用例====")
                    for fu in ls_fuzz:
                        s_time = int(round(time.time() * 1000))
                        resp = base_req(
                            {"base_log": base_log, "req": req, "method": fu.method, "protocol": fu.protocol,
                             "params": fu.params, "url": fu.url, "name": fu.name})
                        e_time = int(round(time.time() * 1000))
                        f_result = _check({"hope": fu.hope, "fact": resp.text})
                        if f_result == Element.C_CHECK["passed"]:
                            passed += 1
                            base_log.build_end_line("检查点=通过")
                        elif f_result == Element.C_CHECK["failed"]:
                            failed += 1
                            base_log.build_end_line("检查点=失败")
                        else:
                            no_check += 1
                            base_log.build_end_line("未检测")

                        app = {"name": fu.name, "url": resp.url, "protocol": fu.protocol, "report": _report,
                               "method": fu.method, "params": fu.params, "hope": fu.hope,
                               "sum_time": str(e_time - s_time) + "ms",
                               "fact": resp.text, "uid": uid, "result": f_result, "code": resp.status_code}
                        no_check += 1
                        new_report_item(app)
                        repo_item = {"url": resp.url, "method": fu.method, "params": fu.params, "name": fu.name,
                                     "hope": fu.hope,
                                     "code": resp.status_code, "fact": resp.text, "result": f_result,
                                     "sum_time": str(e_time - s_time) + "ms"}
                        excel_detail.append(repo_item)

                ss_time = int(round(time.time() * 1000))
                res = base_req(
                    {"base_log": base_log, "req": req, "method": c.method, "protocol": c.protocol,
                     "params": c.params,"url": c.url, "name": c.name})

                ee_time = int(round(time.time() * 1000))
                _result = _check({"hope": c.hope, "fact": res.text})
                if _result == Element.C_CHECK["passed"]:
                    passed += 1
                    base_log.build_end_line("检查点=通过")
                elif _result == Element.C_CHECK["failed"]:
                    failed += 1
                    base_log.build_end_line("检查点=失败")
                else:
                    no_check += 1
                    base_log.build_end_line("未检测")

                app = {"report": _report, "name": c.name, "url": res.url, "protocol": c.protocol, "method": c.method,
                       "code": res.status_code,
                       "params": c.params, "hope": c.hope, "sum_time": str(ee_time - ss_time) + "ms", "fact": res.text,
                       "result": _result}
                new_report_item(app)

                # report_detail
                repo_item = {"url": res.url, "method": c.method, "params": c.params, "name": c.name, "hope": c.hope,
                             "code": res.status_code, "fact": res.text, "result": _result,
                             "sum_time": str(ee_time - ss_time) + "ms"}
                excel_detail.append(repo_item)

        r_e_time = time.time()
        excel_init["start_time"] = start_time
        excel_init["sum_time"] = "%.2f" % (r_e_time - r_time) + "秒"
        excel_init["sum_case"] = passed + failed + no_check
        excel_init["passed"] = passed
        excel_init["failed"] = failed
        excel_init["no_check"] = no_check
        edit_report({"sum_time": "%.2f" % (r_e_time - r_time) + "秒", "passed": passed, "failed": failed,
                     "no_check": no_check, "report": _report})
        write_excel({"uid": uid, "excel_init": excel_init, "excel_detail": excel_detail})
        result = {'code': 0, 'msg': '测试完成'}
        return JsonResponse(result)


def base_req(kw):
    resp = ""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',"Content-Type": "application/json"}
    if kw["method"] == "post":
        data = ast.literal_eval((kw["params"]))
        resp = kw["req"].post(url=kw["protocol"] + "://" + kw["url"], data=data, headers=headers)
        kw["base_log"].build_start_line("请求接口=%s" % kw["name"])
        kw["base_log"].build_start_line("请求协议=%s" % kw["protocol"])
        kw["base_log"].build_start_line("请求url=%s" % kw["url"])
        kw["base_log"].build_start_line("请求方法=%s" % kw["method"])
        kw["base_log"].build_start_line("请求参数=%s" % kw["params"])
    if kw["method"] == "get":
        data = ast.literal_eval(kw["params"])
        resp = kw["req"].get(url=kw["protocol"] + "://" + kw["url"], params=data, headers=headers)
        kw["base_log"].build_start_line("请求接口=%s" % kw["name"])
        kw["base_log"].build_start_line("请求协议=%s" % kw["protocol"])
        kw["base_log"].build_start_line("请求url=%s" % kw["url"])
        kw["base_log"].build_start_line("请求方法=%s" % kw["method"])
        kw["base_log"].build_start_line("请求参数=%s" % kw["params"])
    return resp
